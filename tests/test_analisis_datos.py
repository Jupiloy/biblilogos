import tempfile
import unittest
from pathlib import Path

from analisis_datos import cargar_catalogo, exportar_reportes, generar_indicadores


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


if __name__ == "__main__":
    unittest.main()
