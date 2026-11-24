import sqlite3
import tempfile
import unittest
from pathlib import Path

from analisis_datos import (
    cargar_catalogo,
    cargar_catalogo_sqlite,
    exportar_reportes,
    generar_indicadores,
)


class PruebasCienciaDatos(unittest.TestCase):
    def test_csv_numpy_pandas(self):
        ruta = Path(__file__).parent / "fixtures" / "catalogo_pruebas.csv"
        dataframe = cargar_catalogo(ruta)
        indicadores = generar_indicadores(dataframe)
        self.assertEqual(indicadores["cantidad"], 3)
        self.assertEqual(indicadores["paginas_totales"], 1010)
        self.assertEqual(indicadores["horas_estimadas"], 26)
        self.assertAlmostEqual(indicadores["calificacion_promedio"], 4.77, places=2)

        with tempfile.TemporaryDirectory() as directorio:
            ruta_genero, ruta_indicadores = exportar_reportes(dataframe, directorio)
            self.assertTrue(ruta_genero.exists())
            self.assertTrue(ruta_indicadores.exists())

    def test_sqlite_se_lee_actualizado_en_cada_ejecucion(self):
        with tempfile.TemporaryDirectory() as directorio:
            ruta_db = Path(directorio) / "catalogo.db"
            with sqlite3.connect(ruta_db) as connection:
                connection.execute(
                    """
                    CREATE TABLE publications (
                        isbn TEXT PRIMARY KEY,
                        titulo TEXT NOT NULL,
                        autor TEXT NOT NULL,
                        genero TEXT NOT NULL,
                        paginas INTEGER NOT NULL,
                        calificacion REAL NOT NULL,
                        tipo TEXT NOT NULL
                    )
                    """
                )
                connection.executemany(
                    """
                    INSERT INTO publications
                        (isbn, titulo, autor, genero, paginas, calificacion, tipo)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    [
                        ("DB-001", "Libro uno", "Autora", "Ficción", 100, 4.5, "fisico"),
                        ("DB-002", "Libro dos", "Autor", "Historia", 200, 4.0, "ebook"),
                    ],
                )

            dataframe = cargar_catalogo_sqlite(ruta_db)
            self.assertEqual(generar_indicadores(dataframe)["paginas_totales"], 300)

            with sqlite3.connect(ruta_db) as connection:
                connection.execute(
                    "UPDATE publications SET paginas = 250 WHERE isbn = 'DB-001'"
                )

            actualizado = cargar_catalogo_sqlite(ruta_db)
            self.assertEqual(
                generar_indicadores(actualizado)["paginas_totales"], 450
            )

    def test_sqlite_inexistente_no_se_crea_silenciosamente(self):
        with tempfile.TemporaryDirectory() as directorio:
            ruta_db = Path(directorio) / "inexistente.db"
            with self.assertRaises(FileNotFoundError):
                cargar_catalogo_sqlite(ruta_db)
            self.assertFalse(ruta_db.exists())


if __name__ == "__main__":
    unittest.main()
