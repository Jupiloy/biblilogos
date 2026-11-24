import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError

from backend.models.schemas import SolicitudPublicacion
from backend.services.catalog_service import ServicioCatalogo
from modelos import RepositorioBiblioteca


class PruebasCatalogoPersistente(unittest.TestCase):
    def setUp(self):
        self.directorio = tempfile.TemporaryDirectory()
        self.ruta_db = Path(self.directorio.name) / "catalogo.db"
        self.servicio = ServicioCatalogo(self.ruta_db)

    def tearDown(self):
        RepositorioBiblioteca().limpiar_repositorio()
        self.directorio.cleanup()

    def test_crud_persiste_entre_instancias(self):
        datos = {
            "isbn": "PERSIST-001",
            "titulo": "Persistencia",
            "autor": "Autora de prueba",
            "genero": "Tecnología",
            "paginas": 220,
            "calificacion": 4.5,
            "tipo": "fisico",
            "stock": 3,
            "ubicacion": "Estante P-1",
        }
        creada = self.servicio.crear_publicacion(datos)
        self.assertEqual(creada.titulo, "Persistencia")
        self.servicio.crear_publicacion(
            {
                "isbn": "PERSIST-002",
                "titulo": "Persistencia digital",
                "autor": "Otro autor",
                "genero": "Tecnología",
                "paginas": 180,
                "calificacion": 4.2,
                "tipo": "ebook",
                "formato": "EPUB",
                "peso_mb": 2.4,
            }
        )

        self.servicio = ServicioCatalogo(self.ruta_db)
        recuperada = self.servicio.obtener_publicacion("PERSIST-001")
        self.assertIsNotNone(recuperada)
        self.assertEqual(recuperada.stock, 3)
        ebook = self.servicio.obtener_publicacion("PERSIST-002")
        self.assertEqual(ebook.formato, "EPUB")
        self.assertEqual(ebook.peso_mb, 2.4)

        actualizada = self.servicio.actualizar_publicacion(
            "PERSIST-001",
            {
                "isbn": "PERSIST-003",
                "titulo": "Persistencia actualizada",
                "stock": 5,
            },
        )
        self.assertEqual(actualizada.titulo, "Persistencia actualizada")

        self.servicio = ServicioCatalogo(self.ruta_db)
        self.assertIsNone(self.servicio.obtener_publicacion("PERSIST-001"))
        recuperada = self.servicio.obtener_publicacion("PERSIST-003")
        self.assertEqual(recuperada.titulo, "Persistencia actualizada")
        self.assertEqual(recuperada.stock, 5)

        self.servicio.eliminar_publicacion("PERSIST-003")
        self.servicio = ServicioCatalogo(self.ruta_db)
        self.assertIsNone(self.servicio.obtener_publicacion("PERSIST-003"))

    def test_catalogo_vacio_no_se_vuelve_a_precargar(self):
        for publicacion in self.servicio.listar_publicaciones():
            self.servicio.eliminar_publicacion(publicacion.isbn)

        self.servicio = ServicioCatalogo(self.ruta_db)
        self.assertEqual(self.servicio.listar_publicaciones(), [])

    def test_solicitud_valida_campos_segun_tipo(self):
        base = {
            "isbn": "VALID-001",
            "titulo": "Validación",
            "autor": "Autora",
            "genero": "Ficción",
            "paginas": 100,
            "calificacion": 4.0,
            "tipo": "fisico",
        }
        with self.assertRaises(ValidationError):
            SolicitudPublicacion(**base)

        solicitud = SolicitudPublicacion(
            **base,
            stock=2,
            ubicacion="Estante V-1",
        )
        self.assertEqual(solicitud.tipo, "fisico")


if __name__ == "__main__":
    unittest.main()
