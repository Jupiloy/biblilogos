"""Análisis académico del catálogo con Pandas y NumPy."""

from pathlib import Path

import numpy as np
import pandas as pd


def cargar_catalogo(ruta_csv: str | Path) -> pd.DataFrame:
    """Carga y valida datos bibliográficos desde un CSV."""
    dataframe = pd.read_csv(ruta_csv)
    requeridas = {"isbn", "titulo", "autor", "genero", "paginas", "calificacion", "tipo"}
    faltantes = requeridas.difference(dataframe.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas CSV: {', '.join(sorted(faltantes))}")

    dataframe = dataframe.copy()
    dataframe["paginas"] = pd.to_numeric(dataframe["paginas"], errors="raise")
    dataframe["calificacion"] = pd.to_numeric(dataframe["calificacion"], errors="raise")
    if dataframe["paginas"].le(0).any():
        raise ValueError("Las páginas deben ser mayores que cero.")
    if dataframe["calificacion"].between(0.0, 5.0).eq(False).any():
        raise ValueError("Las calificaciones deben estar entre 0.0 y 5.0.")
    return dataframe


def generar_indicadores(dataframe: pd.DataFrame) -> dict:
    """Genera indicadores usando operaciones vectoriales de NumPy y Pandas."""
    calificaciones = dataframe["calificacion"].to_numpy(dtype=float)
    paginas = dataframe["paginas"].to_numpy(dtype=np.int64)
    cantidad = int(len(dataframe))
    return {
        "cantidad": cantidad,
        "calificacion_promedio": float(np.mean(calificaciones)) if cantidad else 0.0,
        "calificacion_mediana": float(np.median(calificaciones)) if cantidad else 0.0,
        "paginas_totales": int(np.sum(paginas)) if cantidad else 0,
        "horas_estimadas": int(np.ceil(np.sum(paginas) / 40.0)) if cantidad else 0,
        "generos": dataframe.groupby("genero", dropna=False).size().sort_values(
            ascending=False
        ).to_dict(),
    }


def exportar_reportes(dataframe: pd.DataFrame, carpeta_salida: str | Path) -> tuple[Path, Path]:
    """Exporta un reporte por género y un resumen estadístico."""
    salida = Path(carpeta_salida)
    salida.mkdir(parents=True, exist_ok=True)
    ruta_genero = salida / "publicaciones_por_genero.csv"
    reporte_genero = (
        dataframe.groupby("genero", as_index=False)
        .agg(
            publicaciones=("isbn", "count"),
            paginas_totales=("paginas", "sum"),
            calificacion_promedio=("calificacion", "mean"),
        )
        .sort_values(["publicaciones", "calificacion_promedio"], ascending=False)
    )
    reporte_genero.to_csv(ruta_genero, index=False)

    ruta_indicadores = salida / "indicadores.csv"
    indicadores = generar_indicadores(dataframe)
    pd.DataFrame(
        [{"indicador": clave, "valor": valor}
         for clave, valor in indicadores.items() if clave != "generos"]
    ).to_csv(ruta_indicadores, index=False)
    return ruta_genero, ruta_indicadores
