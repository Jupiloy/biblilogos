import tempfile
import unittest
from pathlib import Path

from backend.services.auth_service import ServicioAutenticacion, UsuarioDuplicadoError


class PruebasAutenticacion(unittest.TestCase):
    def setUp(self):
        self.directorio = tempfile.TemporaryDirectory()
        self.servicio = ServicioAutenticacion(
            Path(self.directorio.name) / "usuarios.db"
        )

    def tearDown(self):
        self.directorio.cleanup()

    def test_usuario_lector_y_sesion_revocable(self):
        usuario = self.servicio.crear_usuario(
            "LectorUno", "una-clave-segura-123", "lector"
        )
        self.assertEqual(usuario["role"], "lector")

        sesion = self.servicio.iniciar_sesion(
            "lectoruno", "una-clave-segura-123"
        )
        self.assertIsNotNone(sesion)
        usuario_autenticado = self.servicio.autenticar_token(sesion["access_token"])
        self.assertEqual(usuario_autenticado["username"], "lectoruno")
        self.assertEqual(usuario_autenticado["role"], "lector")

        self.servicio.cerrar_sesion(sesion["access_token"])
        self.assertIsNone(self.servicio.autenticar_token(sesion["access_token"]))
        self.assertIsNone(self.servicio.autenticar_token("token-no-ascii-ñ"))

    def test_contrasena_incorrecta_y_usuario_duplicado_se_rechazan(self):
        self.servicio.crear_usuario("lector", "una-clave-segura-123", "lector")
        self.assertIsNone(
            self.servicio.iniciar_sesion("lector", "otra-clave-segura-123")
        )
        with self.assertRaises(UsuarioDuplicadoError):
            self.servicio.crear_usuario(
                "LECTOR", "otra-clave-segura-123", "lector"
            )

    def test_rechaza_rol_y_contrasena_invalidos(self):
        with self.assertRaises(ValueError):
            self.servicio.crear_usuario(
                "cuenta", "una-clave-segura-123", "admin-no-permitido"
            )
        with self.assertRaises(ValueError):
            self.servicio.crear_usuario("cuenta", "corta", "lector")


if __name__ == "__main__":
    unittest.main()
