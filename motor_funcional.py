"""
motor_funcional.py
Unidad 1: Programación Funcional en Python 3.
Principios aplicados: funciones puras, inmutabilidad, ámbito local estricto,
lambda, filter(), map(), functools.reduce(), Funciones de Orden Superior (FOS)
y encadenamiento tipo pipeline (filter -> map -> reduce).
100% Python 3 — Biblioteca Estándar.
"""

from functools import reduce
import math

PAGINAS_POR_HORA = 40.0


# ==============================================================================
# [Unidad 1 - Funciones puras + lambda + filter()]
# Nunca modifican la lista recibida; siempre retornan una nueva lista.
# ==============================================================================

def filtrar_por_calificacion(catalogo, calificacion_minima):
    """Filtra publicaciones con calificación mayor o igual al umbral indicado."""
    umbral = float(calificacion_minima)
    return list(filter(lambda libro: libro.calificacion >= umbral, catalogo))


def filtrar_por_genero(catalogo, genero_objetivo):
    """Filtra publicaciones cuyo género coincide (sin distinguir mayúsculas)."""
    objetivo = str(genero_objetivo).strip().lower()
    if len(objetivo) == 0 or objetivo == "todos":
        return list(catalogo)
    return list(filter(lambda libro: libro.genero.lower() == objetivo, catalogo))


# ==============================================================================
# [Unidad 1 - Función pura + lambda + map()]
# Transformación sin efectos colaterales (40 páginas por hora).
# ==============================================================================

def calcular_tiempos_lectura(catalogo):
    """
    Transforma cada publicación en una tupla inmutable:
    (isbn, titulo, horas_estimadas).
    """
    return list(
        map(
            lambda libro: (
                libro.isbn,
                libro.titulo,
                round(libro.paginas / PAGINAS_POR_HORA, 2),
            ),
            catalogo,
        )
    )


# ==============================================================================
# [Unidad 1 - Función pura + lambda + functools.reduce()]
# ==============================================================================

def calcular_total_paginas(catalogo):
    """Calcula el total acumulado de páginas usando functools.reduce()."""
    if len(catalogo) == 0:
        return 0
    return reduce(lambda acumulado, libro: acumulado + libro.paginas, catalogo, 0)


# ==============================================================================
# [Unidad 1 - Función de Orden Superior (FOS) personalizada]
# Recibe una función de transformación como parámetro y devuelve nueva colección.
# ==============================================================================

def procesar_catalogo(catalogo, funcion_transformacion):
    """
    Función de Orden Superior que aplica funcion_transformacion a cada elemento
    del catálogo sin alterar la colección original.
    """
    return list(map(funcion_transformacion, catalogo))


# Transformaciones puras reutilizables para pasar a procesar_catalogo()
transformar_a_ficha_resumen = lambda libro: (libro.isbn, libro.titulo, libro.autor)
transformar_a_horas_lectura = lambda libro: {
    "isbn": libro.isbn,
    "titulo": libro.titulo,
    "paginas": libro.paginas,
    "horas_estimadas": round(libro.paginas / PAGINAS_POR_HORA, 2),
}
transformar_a_etiqueta_calidad = lambda libro: (
    libro.titulo,
    "Imprescindible" if libro.calificacion >= 4.8 else (
        "Muy Recomendado" if libro.calificacion >= 4.5 else "Lectura General"
    ),
)


# ==============================================================================
# [Unidad 1 - Pipeline Funcional Encadenado: filter -> map -> reduce]
# ==============================================================================

def ejecutar_pipeline_analisis(catalogo, genero="todos", calificacion_minima=0.0):
    """
    Ejecuta un pipeline funcional puro completo:
      1. filter(): filtra por género y calificación mínima.
      2. map(): calcula el tiempo estimado de lectura en horas (40 pág./hora).
      3. reduce(): acumula el total de páginas y horas del subconjunto filtrado.
    Devuelve un diccionario nuevo sin alterar el catálogo original.
    """
    # Etapa 1: filter (por género y calificación mínima)
    filtrados_genero = filtrar_por_genero(catalogo, genero)
    libros_filtrados = filtrar_por_calificacion(filtrados_genero, calificacion_minima)

    # Etapa 2: map (tiempo estimado por libro)
    tiempos_por_libro = calcular_tiempos_lectura(libros_filtrados)

    # Etapa 3: reduce (suma total de páginas y horas acumuladas)
    total_paginas = calcular_total_paginas(libros_filtrados)
    horas_exactas = round(
        reduce(lambda acc, item: acc + item[2], tiempos_por_libro, 0.0), 2
    )
    horas_redondeadas = math.ceil(total_paginas / PAGINAS_POR_HORA) if total_paginas > 0 else 0

    return {
        "cantidad_original": len(catalogo),
        "cantidad_filtrada": len(libros_filtrados),
        "libros_filtrados": libros_filtrados,
        "tiempos_por_libro": tiempos_por_libro,
        "total_paginas": total_paginas,
        "horas_exactas": horas_exactas,
        "horas_redondeadas": horas_redondeadas,
    }
