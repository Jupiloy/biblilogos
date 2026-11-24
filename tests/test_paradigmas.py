import unittest

from modelos import FabricaPublicaciones, Lector
from motor_funcional import ejecutar_pipeline_analisis
from motor_logico import BaseConocimiento, existe_en_lista, recomendar_libros, unificar


class PruebasParadigmas(unittest.TestCase):
    def setUp(self):
        self.libro_uno = FabricaPublicaciones.crear_publicacion(
            "fisico",
            isbn="PRUEBA-001",
            titulo="Uno",
            autor="Borges",
            genero="Ficción",
            paginas=200,
            calificacion=4.8,
            stock=3,
            ubicacion="A",
        )
        self.libro_dos = FabricaPublicaciones.crear_publicacion(
            "ebook",
            isbn="PRUEBA-002",
            titulo="Dos",
            autor="Borges",
            genero="Ficción",
            paginas=100,
            calificacion=4.5,
            formato="PDF",
            peso_mb=1.0,
        )

    def test_pipeline_funcional(self):
        resultado = ejecutar_pipeline_analisis(
            [self.libro_uno, self.libro_dos],
            genero="Ficción",
            calificacion_minima=4.6,
        )
        self.assertEqual(resultado["cantidad_filtrada"], 1)
        self.assertEqual(resultado["total_paginas"], 200)
        self.assertEqual(resultado["horas_redondeadas"], 5)

    def test_unificacion_y_recursividad(self):
        exito, ligaduras, _ = unificar("Autor", "Borges")
        self.assertTrue(exito)
        self.assertEqual(ligaduras["Autor"], "Borges")
        self.assertTrue(existe_en_lista("PRUEBA-001", ["PRUEBA-001", "PRUEBA-002"]))
        self.assertFalse(existe_en_lista("PRUEBA-003", ["PRUEBA-001", "PRUEBA-002"]))

    def test_inferencia_logica(self):
        lector = Lector(
            "L-1",
            "Persona Prueba",
            "prueba@test.edu",
            "general",
            ["PRUEBA-001"],
        )
        base = BaseConocimiento()
        base.cargar_desde_repositorio([self.libro_uno, self.libro_dos], [lector])
        recomendaciones = recomendar_libros(
            lector, base, [self.libro_uno, self.libro_dos]
        )
        self.assertEqual(recomendaciones[0]["libro"].isbn, "PRUEBA-002")
        self.assertIn("Mismo autor predilecto", recomendaciones[0]["motivos"][0])


if __name__ == "__main__":
    unittest.main()
