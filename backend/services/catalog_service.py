from main import cargar_datos_iniciales
from modelos import FabricaPublicaciones, RepositorioBiblioteca


class ServicioCatalogo:
    def __init__(self) -> None:
        self.repositorio = RepositorioBiblioteca()
        cargar_datos_iniciales(self.repositorio)

    def listar_publicaciones(self) -> list[object]:
        return self.repositorio.obtener_lista_catalogo()

    def obtener_publicacion(self, isbn: str) -> object | None:
        return self.repositorio.buscar_publicacion_por_isbn(isbn)

    def buscar(self, consulta: str = "", genero: str = "") -> list[object]:
        consulta_normalizada = consulta.strip().lower()
        genero_normalizado = genero.strip().lower()

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
            argumentos["stock"] = datos["stock"]
            argumentos["ubicacion"] = datos["ubicacion"]
        else:
            argumentos["formato"] = datos["formato"]
            argumentos["peso_mb"] = datos["peso_mb"]

        publicacion = FabricaPublicaciones.crear_publicacion(tipo, **argumentos)
        self.repositorio.agregar_publicacion(publicacion)
        return publicacion

    def actualizar_publicacion(self, isbn: str, datos: dict) -> object:
        return self.repositorio.actualizar_publicacion(isbn, datos)

    def eliminar_publicacion(self, isbn: str) -> object:
        return self.repositorio.eliminar_publicacion(isbn)
