import json
import sqlite3
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path


class ServicioBibliotecaAbierta:
    """Consulta Open Library y conserva resultados en caché local."""
    def __init__(self) -> None:
        database_dir = Path(__file__).resolve().parents[2] / "data"
        database_dir.mkdir(exist_ok=True)
        self.database_path = database_dir / "bibliologos.db"
        self._initialize_database()

    def _initialize_database(self) -> None:
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS publications_cache (
                    isbn TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    pages INTEGER NOT NULL,
                    rating REAL NOT NULL,
                    type TEXT NOT NULL,
                    format TEXT,
                    cover_url TEXT,
                    open_url TEXT,
                    description TEXT,
                    subjects TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def buscar(self, consulta: str, genero: str = "", limite: int = 20) -> list[dict]:
        consulta_normalizada = consulta.strip()
        genero_normalizado = genero.strip()

        if genero_normalizado and genero_normalizado.lower() != "todos":
            consulta_normalizada = (
                f"{consulta_normalizada} {genero_normalizado}".strip()
            )

        almacenados = self._buscar_en_cache(consulta_normalizada, limite)
        if almacenados:
            return almacenados

        remotos = self._buscar_remoto(consulta_normalizada or "open literature", limite)
        if remotos:
            self._guardar_remotos(remotos)
            return remotos

        return []

    def obtener_publicacion(self, isbn: str) -> dict | None:
        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute(
                "SELECT * FROM publications_cache WHERE isbn = ?",
                (isbn,),
            ).fetchone()
        if row is None:
            return None

        publication = self._fila_a_diccionario(row)
        if not publication["description"]:
            publication = self._completar_detalles(publication)
        return publication

    def _completar_detalles(self, publication: dict) -> dict:
        open_url = publication["open_url"]
        if "/works/" not in open_url:
            return publication

        work_id = open_url.rsplit("/works/", 1)[-1].strip("/")
        url = f"https://openlibrary.org/works/{work_id}.json"
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "BiblioLogos/1.0"},
        )

        try:
            with urllib.request.urlopen(request, timeout=8) as response:
                details = json.loads(response.read().decode("utf-8"))
        except (OSError, json.JSONDecodeError, urllib.error.URLError):
            return publication

        description = details.get("description")
        if isinstance(description, dict):
            description = description.get("value")
        if isinstance(description, str) and description.strip():
            publication["description"] = description.strip()

        subjects = details.get("subjects") or []
        if subjects:
            publication["subjects"] = subjects[:8]

        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                UPDATE publications_cache
                SET description = ?, subjects = ?
                WHERE isbn = ?
                """,
                (
                    publication["description"],
                    json.dumps(publication["subjects"]),
                    publication["isbn"],
                ),
            )

        return publication

    def recomendar(self, isbn: str, limite: int = 6) -> list[dict]:
        fuente = self.obtener_publicacion(isbn)
        if fuente is None:
            return []

        candidatas = self.buscar(
            fuente["genre"],
            limite=min(limite * 3, 30),
        )
        recommendations = []
        for candidata in candidatas:
            if candidata["isbn"] == isbn:
                continue

            score = 0.0
            reasons = []
            if candidata["genre"].lower() == fuente["genre"].lower():
                score += 1.2
                reasons.append("Comparte género y temas")
            source_subjects = set(fuente["subjects"])
            shared_subjects = source_subjects.intersection(set(candidata["subjects"]))
            if shared_subjects:
                score += 0.4 * len(shared_subjects)
                reasons.append("Comparte temas relacionados")
            if candidata["author"].lower() == fuente["author"].lower():
                score += 2.0
                reasons.append("El mismo autor")

            if reasons:
                recommendations.append(
                    {
                        "publication": candidata,
                        "score": round(candidata["rating"] + score, 2),
                        "reasons": reasons,
                    }
                )

        recommendations.sort(
            key=lambda item: (item["score"], item["publication"]["rating"]),
            reverse=True,
        )
        return recommendations[:limite]

    def _buscar_remoto(self, consulta: str, limite: int) -> list[dict]:
        params = urllib.parse.urlencode(
            {
                "q": consulta,
                "limit": limite,
                "fields":
                "key,title,author_name,subject,edition_count,"
                "number_of_pages_median,ratings_average,cover_i,"
                "ebook_access,first_publish_year,first_sentence",
            }
        )
        url = f"https://openlibrary.org/search.json?{params}"
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "BiblioLogos/1.0"},
        )

        try:
            with urllib.request.urlopen(request, timeout=8) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (OSError, json.JSONDecodeError, urllib.error.URLError):
            return []

        publications = []
        for document in payload.get("docs", []):
            isbn = self._extraer_isbn(document)
            title = str(document.get("title") or "").strip()
            authors = document.get("author_name") or []
            subjects = document.get("subject") or []
            first_sentence = document.get("first_sentence") or []
            if isinstance(first_sentence, list):
                description = " ".join(str(item) for item in first_sentence[:2])
            else:
                description = str(first_sentence)
            if not isbn or not title:
                continue

            cover_id = document.get("cover_i")
            cover_url = (
                f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                if cover_id
                else ""
            )
            subject = str(subjects[0]).strip() if subjects else "General"
            publications.append(
                {
                    "isbn": isbn,
                    "title": title,
                    "author": ", ".join(authors[:2]) if authors else "Autor desconocido",
                    "genre": subject,
                    "pages": int(document.get("number_of_pages_median") or 200),
                    "rating": round(float(document.get("ratings_average") or 4.0), 2),
                    "type": "ebook"
                    if document.get("ebook_access") not in (None, "no_ebook")
                    else "physical",
                    "format": "EPUB" if document.get("ebook_access") else None,
                    "cover_url": cover_url,
                    "open_url": f"https://openlibrary.org{document.get('key', '')}",
                    "description": description,
                    "subjects": subjects[:8],
                }
            )

        return publications

    def _extraer_isbn(self, document: dict) -> str:
        isbn = document.get("isbn")
        if isinstance(isbn, list) and isbn:
            return str(isbn[0])
        if isinstance(isbn, str):
            return isbn
        key = str(document.get("key") or "")
        return key.replace("/works/", "WORK-") if key else ""

    def _buscar_en_cache(self, query: str, limit: int) -> list[dict]:
        terms = [term.lower() for term in query.lower().split() if term]
        if not terms:
            return []

        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                "SELECT * FROM publications_cache LIMIT 500"
            ).fetchall()

        publications = []
        for row in rows:
            searchable = (
                f"{row['title']} {row['author']} "
                f"{row['genre']} {row['subjects']}"
            ).lower()
            if all(term in searchable for term in terms):
                publications.append(self._fila_a_diccionario(row))

        publications.sort(
            key=lambda publication: (
                publication["rating"],
                publication["title"].lower(),
            ),
            reverse=True,
        )
        return publications[:limit]

    def _guardar_remotos(self, publications: list[dict]) -> None:
        with sqlite3.connect(self.database_path) as connection:
            for publication in publications:
                connection.execute(
                    """
                    INSERT OR REPLACE INTO publications_cache (
                        isbn, title, author, genre, pages, rating, type,
                        format, cover_url, open_url, description, subjects
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        publication["isbn"],
                        publication["title"],
                        publication["author"],
                        publication["genre"],
                        publication["pages"],
                        publication["rating"],
                        publication["type"],
                        publication["format"],
                        publication["cover_url"],
                        publication["open_url"],
                        publication["description"],
                        json.dumps(publication["subjects"]),
                    ),
                )

    def _fila_a_diccionario(self, row: sqlite3.Row) -> dict:
        subjects = json.loads(row["subjects"] or "[]")
        return {
            "isbn": row["isbn"],
            "title": row["title"],
            "author": row["author"],
            "genre": row["genre"],
            "pages": row["pages"],
            "rating": row["rating"],
            "type": row["type"],
            "format": row["format"],
            "cover_url": row["cover_url"],
            "open_url": row["open_url"],
            "description": row["description"],
            "subjects": subjects,
        }
