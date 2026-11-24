from main import cargar_datos_iniciales
from modelos import RepositorioBiblioteca


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
