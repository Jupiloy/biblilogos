import unittest

from modelos import FabricaPublicaciones, RepositorioBiblioteca


class PruebasRepositorio(unittest.TestCase):
    def setUp(self):
        self.repositorio = RepositorioBiblioteca()
        self.repositorio.limpiar_repositorio()

    def tearDown(self):
        self.repositorio.limpiar_repositorio()

    def test_crud_publicacion(self):
        publicacion = FabricaPublicaciones.crear_publicacion(
            "fisico",
            isbn="TEST-001",
            titulo="Título original",
            autor="Autor prueba",
            genero="Sistemas",
            paginas=300,
            calificacion=4.5,
            stock=2,
            ubicacion="Estante A",
        )
        self.repositorio.agregar_publicacion(publicacion)
        self.assertIs(
            self.repositorio.buscar_publicacion_por_isbn("TEST-001"),
            publicacion,
        )

        actualizada = self.repositorio.actualizar_publicacion(
            "TEST-001", {"titulo": "Título actualizado", "stock": 7}
        )
        self.assertEqual(actualizada.titulo, "Título actualizado")
        self.assertEqual(actualizada.stock, 7)

        eliminada = self.repositorio.eliminar_publicacion("TEST-001")
        self.assertEqual(eliminada.isbn, "TEST-001")
        self.assertIsNone(self.repositorio.buscar_publicacion_por_isbn("TEST-001"))

    def test_duplicado_e_implicitos(self):
        datos = {
            "isbn": "TEST-002",
            "titulo": "Duplicada",
            "autor": "Autor",
            "genero": "Tecnología",
            "paginas": 200,
            "calificacion": 4.0,
            "stock": 1,
            "ubicacion": "A-1",
        }
        primera = FabricaPublicaciones.crear_publicacion("fisico", **datos)
        self.repositorio.agregar_publicacion(primera)
        with self.assertRaises(ValueError):
            self.repositorio.agregar_publicacion(
                FabricaPublicaciones.crear_publicacion("fisico", **datos)
            )


if __name__ == "__main__":
    unittest.main()
