from backend.services.catalog_service import ServicioCatalogo


class ServicioRecomendaciones:
    def __init__(self, servicio_catalogo: ServicioCatalogo) -> None:
        self.servicio_catalogo = servicio_catalogo

    def recomendar(self, isbn: str, limite: int = 6) -> list[dict]:
        fuente = self.servicio_catalogo.obtener_publicacion(isbn)
        if fuente is None:
            return []

        recomendaciones = []
        for candidata in self.servicio_catalogo.listar_publicaciones():
            if candidata.isbn == fuente.isbn:
                continue

            puntaje = 0.0
            motivos = []
            if candidata.autor.lower() == fuente.autor.lower():
                puntaje += 2.0
                motivos.append("El mismo autor")
            if candidata.genero.lower() == fuente.genero.lower():
                puntaje += 1.2
                motivos.append("Comparte género y temas")
            if candidata.calificacion >= 4.7:
                puntaje += 0.3

            if motivos:
                recomendaciones.append(
                    {
                        "publication": candidata,
                        "score": round(candidata.calificacion + puntaje, 2),
                        "reasons": motivos,
                    }
                )

        recomendaciones.sort(
            key=lambda item: (item["score"], item["publication"].calificacion),
            reverse=True,
        )
        return recomendaciones[:limite]
