import sqlite3
import threading
from pathlib import Path

from main import cargar_datos_iniciales
from modelos import FabricaPublicaciones, RepositorioBiblioteca


class ServicioCatalogo:
    def __init__(self, database_path: str | Path | None = None) -> None:
        self.repositorio = RepositorioBiblioteca()
        self._lock = threading.RLock()
        self.database_path = (
            Path(database_path)
            if database_path is not None
            else Path(__file__).resolve().parents[2] / "data" / "catalogo.db"
        )
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _initialize_database(self) -> None:
        self.repositorio.limpiar_repositorio()
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS publications (
                    isbn TEXT PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    genero TEXT NOT NULL,
                    paginas INTEGER NOT NULL,
                    calificacion REAL NOT NULL,
                    tipo TEXT NOT NULL CHECK (tipo IN ('fisico', 'ebook')),
                    stock INTEGER,
                    ubicacion TEXT,
                    formato TEXT,
                    peso_mb REAL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS catalog_metadata (
                    clave TEXT PRIMARY KEY,
                    valor TEXT NOT NULL
                )
                """
            )
            initialized = connection.execute(
                "SELECT valor FROM catalog_metadata WHERE clave = 'seeded'"
            ).fetchone()

            if initialized is None:
                cargar_datos_iniciales(self.repositorio)
                self._save_catalog(connection)
                connection.execute(
                    "INSERT INTO catalog_metadata (clave, valor) VALUES ('seeded', '1')"
                )
            else:
                self._load_catalog(connection)

    def _load_catalog(self, connection: sqlite3.Connection) -> None:
        self.repositorio.limpiar_repositorio()
        rows = connection.execute(
            """
            SELECT isbn, titulo, autor, genero, paginas, calificacion,
                   tipo, stock, ubicacion, formato, peso_mb
            FROM publications ORDER BY rowid
            """
        ).fetchall()
        for row in rows:
            isbn, titulo, autor, genero, paginas, rating, tipo, stock, location, fmt, weight = row
            datos = {
                "isbn": isbn,
                "titulo": titulo,
                "autor": autor,
                "genero": genero,
                "paginas": paginas,
                "calificacion": rating,
            }
            if tipo == "fisico":
                datos.update(stock=stock, ubicacion=location)
            else:
                datos.update(formato=fmt, peso_mb=weight)
            self.repositorio.agregar_publicacion(
                FabricaPublicaciones.crear_publicacion(tipo, **datos)
            )

    def _save_catalog(self, connection: sqlite3.Connection) -> None:
        publications = self.repositorio.obtener_lista_catalogo()
        connection.execute("DELETE FROM publications")
        connection.executemany(
            """
            INSERT INTO publications (
                isbn, titulo, autor, genero, paginas, calificacion,
                tipo, stock, ubicacion, formato, peso_mb
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    publication.isbn,
                    publication.titulo,
                    publication.autor,
                    publication.genero,
                    publication.paginas,
                    publication.calificacion,
                    "fisico" if hasattr(publication, "stock") else "ebook",
                    getattr(publication, "stock", None),
                    getattr(publication, "ubicacion", None),
                    getattr(publication, "formato", None),
                    getattr(publication, "peso_mb", None),
                )
                for publication in publications
            ],
        )

    def _persist_catalog(self) -> None:
        with sqlite3.connect(self.database_path) as connection:
            self._save_catalog(connection)

    def listar_publicaciones(self) -> list[object]:
        with self._lock:
            return self.repositorio.obtener_lista_catalogo()

    def obtener_publicacion(self, isbn: str) -> object | None:
        with self._lock:
            return self.repositorio.buscar_publicacion_por_isbn(isbn)

    def buscar(self, consulta: str = "", genero: str = "") -> list[object]:
        consulta_normalizada = consulta.strip().lower()
        genero_normalizado = genero.strip().lower()

        with self._lock:
            publicaciones = self.listar_publicaciones()
        if genero_normalizado and genero_normalizado != "todos":
            publicaciones = [
                publicacion
                for publicacion in publicaciones
                if publicacion.genero.lower() == genero_normalizado
            ]

        if not consulta_normalizada:
            return publicaciones

        terminos = consulta_normalizada.split()
        return [
            publicacion
            for publicacion in publicaciones
            if all(
                term in (
                    f"{publicacion.titulo} {publicacion.autor} "
                    f"{publicacion.genero}"
                ).lower()
                for term in terminos
            )
        ]

    def crear_publicacion(self, datos: dict) -> object:
        tipo = datos["tipo"]
        argumentos = {
            "isbn": datos["isbn"],
            "titulo": datos["titulo"],
            "autor": datos["autor"],
            "genero": datos["genero"],
            "paginas": datos["paginas"],
            "calificacion": datos["calificacion"],
        }
        if tipo == "fisico":
            argumentos["stock"] = datos.get("stock")
            argumentos["ubicacion"] = datos.get("ubicacion")
        else:
            argumentos["formato"] = datos.get("formato")
            argumentos["peso_mb"] = datos.get("peso_mb")

        with self._lock:
            publicacion = FabricaPublicaciones.crear_publicacion(tipo, **argumentos)
            if self.repositorio.buscar_publicacion_por_isbn(publicacion.isbn):
                raise ValueError(
                    f"Ya existe una publicación registrada con ISBN {publicacion.isbn}."
                )
            self.repositorio.agregar_publicacion(publicacion)
            try:
                self._persist_catalog()
            except sqlite3.Error:
                self.repositorio.eliminar_publicacion(publicacion.isbn)
                raise
            return publicacion

    def actualizar_publicacion(self, isbn: str, datos: dict) -> object:
        with self._lock:
            actual = self.repositorio.buscar_publicacion_por_isbn(isbn)
            if actual is None:
                raise KeyError(f"No existe una publicación con ISBN {isbn}.")

            tipo = "fisico" if hasattr(actual, "stock") else "ebook"
            datos_actualizados = {
                "isbn": datos.get("isbn", actual.isbn),
                "titulo": datos.get("titulo", actual.titulo),
                "autor": datos.get("autor", actual.autor),
                "genero": datos.get("genero", actual.genero),
                "paginas": datos.get("paginas", actual.paginas),
                "calificacion": datos.get("calificacion", actual.calificacion),
            }
            if tipo == "fisico":
                datos_actualizados.update(
                    stock=datos.get("stock", actual.stock),
                    ubicacion=datos.get("ubicacion", actual.ubicacion),
                )
            else:
                datos_actualizados.update(
                    formato=datos.get("formato", actual.formato),
                    peso_mb=datos.get("peso_mb", actual.peso_mb),
                )

            replacement = FabricaPublicaciones.crear_publicacion(
                tipo, **datos_actualizados
            )
            duplicate = self.repositorio.buscar_publicacion_por_isbn(replacement.isbn)
            if duplicate is not None and replacement.isbn != actual.isbn:
                raise ValueError(
                    f"Ya existe una publicación registrada con ISBN {replacement.isbn}."
                )

            self.repositorio.actualizar_publicacion(isbn, datos)
            try:
                self._persist_catalog()
            except sqlite3.Error:
                self.repositorio.actualizar_publicacion(
                    replacement.isbn,
                    {
                        "isbn": actual.isbn,
                        "titulo": actual.titulo,
                        "autor": actual.autor,
                        "genero": actual.genero,
                        "paginas": actual.paginas,
                        "calificacion": actual.calificacion,
                        **(
                            {"stock": actual.stock, "ubicacion": actual.ubicacion}
                            if tipo == "fisico"
                            else {"formato": actual.formato, "peso_mb": actual.peso_mb}
                        ),
                    },
                )
                raise
            return replacement

    def eliminar_publicacion(self, isbn: str) -> object:
        with self._lock:
            publicacion = self.repositorio.buscar_publicacion_por_isbn(isbn)
            if publicacion is None:
                raise KeyError(f"No existe una publicación con ISBN {isbn}.")
            self.repositorio.eliminar_publicacion(isbn)
            try:
                self._persist_catalog()
            except sqlite3.Error:
                self.repositorio.agregar_publicacion(publicacion)
                raise
            return publicacion
