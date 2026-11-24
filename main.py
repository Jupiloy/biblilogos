"""
main.py
Unidad 3: Estructuras de Datos (tuplas, listas, diccionarios),
Módulos Estándar (statistics, random, datetime, math) y Menú Interactivo.
Curso: Lenguajes de Programación (100000SI68)
Ejecución en VS Code: python main.py
"""

from datetime import datetime
import math
import random
import statistics

from modelos import (
    FabricaPublicaciones,
    Lector,
    RepositorioBiblioteca,
)
from motor_funcional import (
    ejecutar_pipeline_analisis,
    procesar_catalogo,
    transformar_a_etiqueta_calidad,
    transformar_a_ficha_resumen,
)
from motor_logico import (
    BaseConocimiento,
    EstrategiaCombinada,
    EstrategiaPorAutor,
    EstrategiaPorGenero,
    existe_en_lista,
    recomendar_libros,
    unificar,
)


# ==============================================================================
# [Unidad 3 - Precarga de 8 publicaciones (LibroFisico y Ebook) + 3 Lectores]
# Utiliza los patrones Fábrica y Repositorio Singleton.
# ==============================================================================

def cargar_datos_iniciales(repositorio):
    """Precarga 8 libros variados y 3 lectores si el repositorio está vacío."""
    if len(repositorio.catalogo_por_isbn) > 0:
        return

    datos_libros = [
        (
            "fisico",
            {
                "isbn": "978-0307474728",
                "titulo": "Cien años de soledad",
                "autor": "Gabriel García Márquez",
                "genero": "Realismo Mágico",
                "paginas": 471,
                "calificacion": 4.9,
                "stock": 5,
                "ubicacion": "Estante A-12",
            },
        ),
        (
            "ebook",
            {
                "isbn": "978-0307387264",
                "titulo": "El amor en los tiempos del cólera",
                "autor": "Gabriel García Márquez",
                "genero": "Realismo Mágico",
                "paginas": 368,
                "calificacion": 4.7,
                "formato": "EPUB",
                "peso_mb": 3.4,
            },
        ),
        (
            "fisico",
            {
                "isbn": "978-8420471839",
                "titulo": "La casa de los espíritus",
                "autor": "Isabel Allende",
                "genero": "Realismo Mágico",
                "paginas": 499,
                "calificacion": 4.6,
                "stock": 3,
                "ubicacion": "Estante A-14",
            },
        ),
        (
            "fisico",
            {
                "isbn": "978-8499089515",
                "titulo": "Ficciones",
                "autor": "Jorge Luis Borges",
                "genero": "Ficción Especulativa",
                "paginas": 218,
                "calificacion": 4.9,
                "stock": 4,
                "ubicacion": "Estante B-03",
            },
        ),
        (
            "ebook",
            {
                "isbn": "978-8499890944",
                "titulo": "El Aleph",
                "autor": "Jorge Luis Borges",
                "genero": "Ficción Especulativa",
                "paginas": 204,
                "calificacion": 4.8,
                "formato": "PDF",
                "peso_mb": 2.8,
            },
        ),
        (
            "fisico",
            {
                "isbn": "978-8466320535",
                "titulo": "Rayuela",
                "autor": "Julio Cortázar",
                "genero": "Ficción Especulativa",
                "paginas": 632,
                "calificacion": 4.5,
                "stock": 2,
                "ubicacion": "Estante B-07",
            },
        ),
        (
            "ebook",
            {
                "isbn": "978-8499926223",
                "titulo": "Sapiens: De animales a dioses",
                "autor": "Yuval Noah Harari",
                "genero": "Divulgación Científica",
                "paginas": 496,
                "calificacion": 4.7,
                "formato": "EPUB",
                "peso_mb": 5.1,
            },
        ),
        (
            "ebook",
            {
                "isbn": "978-8499929767",
                "titulo": "Breves respuestas a las grandes preguntas",
                "autor": "Stephen Hawking",
                "genero": "Divulgación Científica",
                "paginas": 256,
                "calificacion": 4.4,
                "formato": "PDF",
                "peso_mb": 4.2,
            },
        ),
    ]

    for tipo, info in datos_libros:
        publicacion = FabricaPublicaciones.crear_publicacion(tipo, **info)
        repositorio.agregar_publicacion(publicacion)

    lectores_iniciales = [
        Lector(
            "LEC-001",
            "Valentina Ríos Mendoza",
            "valentina.rios@universidad.edu.pe",
            "vip",
            ["978-0307474728"],
        ),
        Lector(
            "LEC-002",
            "Mateo Paredes Quispe",
            "mateo.paredes@universidad.edu.pe",
            "frecuente",
            ["978-8499089515", "978-8499926223"],
        ),
        Lector(
            "LEC-003",
            "Camila Soto Herrera",
            "camila.soto@universidad.edu.pe",
            "general",
            ["978-8420471839"],
        ),
    ]

    for lector in lectores_iniciales:
        repositorio.agregar_lector(lector)


# ==============================================================================
# [Unidad 3 - Módulos estándar: statistics, random, datetime, math]
# ==============================================================================

def generar_reporte_estadistico(repositorio):
    """Calcula promedio, mediana, redondeos controlados y marca temporal."""
    catalogo = repositorio.obtener_lista_catalogo()
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    print("\n" + "=" * 68)
    print(f" REPORTE ESTADÍSTICO DEL CATÁLOGO  |  Fecha: {fecha_actual}")
    print("=" * 68)

    if len(catalogo) == 0:
        print("El catálogo se encuentra vacío. No es posible calcular estadísticas.")
        return

    calificaciones = [libro.calificacion for libro in catalogo]
    promedio = statistics.mean(calificaciones)
    mediana = statistics.median(calificaciones)
    total_paginas = sum(libro.paginas for libro in catalogo)
    horas_ceil = math.ceil(total_paginas / 40.0)

    print(f"Total de publicaciones : {len(catalogo)}")
    print(f"Total de páginas       : {total_paginas} páginas")
    print(f"Lectura total (ceil)   : {horas_ceil} horas (a 40 pág./hora)")
    print(f"Promedio calificación  : {promedio:.2f} / 5.00")
    print(f"Mediana calificación   : {mediana:.2f} / 5.00")
    print(f"Fichas inmutables      : {len(repositorio.fichas_inmutables)} tuplas registradas")
    print("=" * 68)


def mostrar_libro_sorpresa(repositorio):
    """[Unidad 3 - Módulo random] Selecciona aleatoriamente el Libro Sorpresa del Día."""
    catalogo = repositorio.obtener_lista_catalogo()
    if len(catalogo) == 0:
        print("No hay libros registrados para sortear.")
        return
    elegido = random.choice(catalogo)
    codigo_prestamo = f"PREST-{random.randint(1000, 9999)}"
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    print("\n--- LIBRO SORPRESA DEL DÍA ---")
    print(elegido.mostrar_info())
    print(f"Código sugerido de préstamo: {codigo_prestamo} | Generado: {fecha_actual}")


def registrar_nueva_publicacion(repositorio):
    """Solicita datos por consola y usa FabricaPublicaciones con validación."""
    print("\n--- REGISTRAR NUEVA PUBLICACIÓN (Patrón Fábrica) ---")
    tipo = input("Tipo ('fisico' o 'ebook'): ").strip().lower()
    isbn = input("ISBN: ").strip()
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    genero = input("Género: ").strip()

    try:
        paginas = int(input("Número de páginas: ").strip())
        calificacion = float(input("Calificación (0.0 a 5.0): ").strip())

        if tipo == "fisico":
            stock = int(input("Stock disponible: ").strip())
            ubicacion = input("Ubicación en estantería: ").strip()
            pub = FabricaPublicaciones.crear_publicacion(
                "fisico",
                isbn=isbn,
                titulo=titulo,
                autor=autor,
                genero=genero,
                paginas=paginas,
                calificacion=calificacion,
                stock=stock,
                ubicacion=ubicacion,
            )
        elif tipo == "ebook":
            formato = input("Formato (PDF / EPUB): ").strip().upper()
            peso_mb = float(input("Peso en MB: ").strip())
            pub = FabricaPublicaciones.crear_publicacion(
                "ebook",
                isbn=isbn,
                titulo=titulo,
                autor=autor,
                genero=genero,
                paginas=paginas,
                calificacion=calificacion,
                formato=formato,
                peso_mb=peso_mb,
            )
        else:
            print("Error: el tipo debe ser 'fisico' o 'ebook'.")
            return

        repositorio.agregar_publicacion(pub)
        print("Publicación registrada con éxito:")
        print(" ->", pub.mostrar_info())
    except ValueError as error:
        print(f"Entrada inválida: {error}")


def registrar_nuevo_lector(repositorio):
    """Crea un lector validando nombre, correo y categoría."""
    print("\n--- REGISTRAR NUEVO LECTOR ---")
    siguiente = len(repositorio.lectores_por_codigo) + 1
    codigo_sugerido = f"LEC-{siguiente:03d}"
    codigo = input(f"Código [{codigo_sugerido}]: ").strip() or codigo_sugerido
    nombre = input("Nombre completo: ")
    correo = input("Correo electrónico: ")
    categoria = input("Categoría (VIP / FRECUENTE / GENERAL): ")

    try:
        lector = Lector(codigo, nombre, correo, categoria)
        repositorio.agregar_lector(lector)
        print("Lector registrado correctamente:", lector.mostrar_info())
    except ValueError as error:
        print(f"Error de validación: {error}")


def registrar_prestamo_consola(repositorio):
    """Registra un préstamo con código aleatorio y fecha/hora formateada."""
    print("\n--- REGISTRAR PRÉSTAMO ---")
    codigo_lector = input("Código del lector (ej. LEC-001): ").strip().upper()
    lector = repositorio.buscar_lector_por_codigo(codigo_lector)
    if lector is None:
        print("No se encontró un lector con ese código.")
        return

    isbn = input("ISBN de la publicación: ").strip()
    libro = repositorio.buscar_publicacion_por_isbn(isbn)
    if libro is None:
        print("No se encontró ninguna publicación con ese ISBN.")
        return

    codigo_prestamo = f"PREST-{random.randint(1000, 9999)}"
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
    lector.registrar_lectura(libro.isbn)
    registro = {
        "codigo_prestamo": codigo_prestamo,
        "lector": lector.codigo,
        "isbn": libro.isbn,
        "titulo": libro.titulo,
        "fecha_hora": fecha_hora,
    }
    repositorio.registrar_prestamo(registro)
    print(f"Préstamo {codigo_prestamo} registrado el {fecha_hora} para {lector.nombre}.")


def ejecutar_menu_funcional(repositorio):
    """Demostración interactiva de la Unidad 1: Pipeline + FOS."""
    print("\n--- MOTOR FUNCIONAL (UNIDAD 1: filter -> map -> reduce) ---")
    genero = input("Género a filtrar (deje vacío o 'todos'): ").strip() or "todos"
    try:
        calif_txt = input("Calificación mínima (0.0 a 5.0) [4.5]: ").strip()
        calif_min = float(calif_txt) if calif_txt else 4.5
    except ValueError:
        print("Calificación inválida; se cancela el análisis.")
        return

    catalogo = repositorio.obtener_lista_catalogo()
    resultado = ejecutar_pipeline_analisis(catalogo, genero, calif_min)

    print(
        f"\nResultados del pipeline ({resultado['cantidad_filtrada']} de "
        f"{resultado['cantidad_original']} libros):"
    )
    if resultado["cantidad_filtrada"] == 0:
        print("Ningún libro cumplió los criterios de filtrado.")
        return

    for isbn, titulo, horas in resultado["tiempos_por_libro"]:
        print(f"  - [{isbn}] {titulo}: {horas:.2f} horas estimadas")

    print(f"Total acumulado de páginas (reduce): {resultado['total_paginas']} pág.")
    print(f"Horas exactas / redondeadas (ceil): {resultado['horas_exactas']} h / {resultado['horas_redondeadas']} h")

    print("\nDemostración FOS procesar_catalogo() -> Clasificación editorial:")
    etiquetas = procesar_catalogo(resultado["libros_filtrados"], transformar_a_etiqueta_calidad)
    for titulo, nivel in etiquetas:
        print(f"  * {titulo} -> {nivel}")


def ejecutar_menu_logico(repositorio, base_conocimiento):
    """Demostración interactiva de la Unidad 2: Recomendaciones, Unificación y [Cabeza|Cola]."""
    catalogo = repositorio.obtener_lista_catalogo()
    lectores = repositorio.obtener_lista_lectores()
    base_conocimiento.cargar_desde_repositorio(catalogo, lectores)

    print("\n--- MOTOR LÓGICO Y RECOMENDADOR (UNIDAD 2 + PATRÓN ESTRATEGIA) ---")
    for lec in lectores:
        print(" ", lec.mostrar_info())

    codigo = input("Ingrese código de lector (ej. LEC-001): ").strip().upper()
    lector = repositorio.buscar_lector_por_codigo(codigo)
    if lector is None:
        print("Lector no encontrado.")
        return

    print("Estrategias disponibles: 1) Combinada  2) Solo Género  3) Solo Autor")
    opc_est = input("Seleccione estrategia [1]: ").strip() or "1"
    if opc_est == "2":
        estrategia = EstrategiaPorGenero()
    elif opc_est == "3":
        estrategia = EstrategiaPorAutor()
    else:
        estrategia = EstrategiaCombinada()

    modo_corte = input("¿Activar operador corte (!) para solo la 1ra mejor? (s/n) [n]: ").strip().lower()
    usar_corte = modo_corte == "s"

    recomendaciones = recomendar_libros(
        lector, base_conocimiento, catalogo, corte=usar_corte, estrategia=estrategia
    )

    modo_texto = "CORTE (!)" if usar_corte else "BACKTRACKING (todas las soluciones)"
    print(f"\nInferencia para {lector.nombre} | {estrategia.nombre} | {modo_texto}:")
    if len(recomendaciones) == 0:
        print("No se dedujeron nuevas recomendaciones para este lector.")
    else:
        for idx, rec in enumerate(recomendaciones, start=1):
            print(f"  {idx}. {rec['libro'].mostrar_info()}")
            print(f"     Reglas deducidas: {' ; '.join(rec['motivos'])} | Afinidad: {rec['puntaje_afinidad']}")

    # Prueba rápida de unificación y recursividad [Cabeza | Cola]
    exito, ligaduras, msg = unificar("AutorPreferido", "Jorge Luis Borges")
    print(f"\n[Unificación] unificar('AutorPreferido', 'Jorge Luis Borges') -> {exito} {ligaduras} | {msg}")
    prueba_isbn = "978-0307474728"
    esta = existe_en_lista(prueba_isbn, lector.libros_leidos)
    print(f"[Recursividad Cabeza|Cola] existe_en_lista('{prueba_isbn}', leidos) -> {esta}")


# ==============================================================================
# [Unidad 3 - Menú Interactivo en Consola: while, if/elif/else, break]
# ==============================================================================

def iniciar_menu_consola():
    """Punto de entrada principal del menú interactivo en consola."""
    repositorio = RepositorioBiblioteca()
    cargar_datos_iniciales(repositorio)
    base_conocimiento = BaseConocimiento()

    while True:
        print("\n" + "=" * 68)
        print(" BIBLIOLOGOS — SISTEMA GESTOR Y RECOMENDADOR INTELIGENTE DE LIBROS")
        print("=" * 68)
        print(" 1. Listar catálogo completo (POO + Polimorfismo)")
        print(" 2. Buscar publicación por ISBN (Diccionario O(1) + Tupla inmutable)")
        print(" 3. Registrar nueva publicación (Patrón Fábrica)")
        print(" 4. Registrar nuevo lector (Validación de cadenas)")
        print(" 5. Ejecutar pipeline funcional (Unidad 1: filter -> map -> reduce)")
        print(" 6. Recomendador inteligente lógico (Unidad 2: Estrategia + Corte !)")
        print(" 7. Reporte estadístico y Libro Sorpresa del Día (Módulos estándar)")
        print(" 8. Registrar préstamo (random + datetime)")
        print(" 0. Salir del sistema")
        print("-" * 68)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- CATÁLOGO BIBLIOGRÁFICO ---")
            for libro in repositorio.obtener_lista_catalogo():
                print(" ", libro.mostrar_info())
        elif opcion == "2":
            isbn = input("Ingrese el ISBN a consultar: ").strip()
            libro = repositorio.buscar_publicacion_por_isbn(isbn)
            if libro is not None:
                print("Encontrado:", libro.mostrar_info())
                print("Ficha inmutable (tupla):", libro.obtener_ficha_inmutable())
            else:
                print("No existe ninguna publicación con ese ISBN.")
        elif opcion == "3":
            registrar_nueva_publicacion(repositorio)
        elif opcion == "4":
            registrar_nuevo_lector(repositorio)
        elif opcion == "5":
            ejecutar_menu_funcional(repositorio)
        elif opcion == "6":
            ejecutar_menu_logico(repositorio, base_conocimiento)
        elif opcion == "7":
            generar_reporte_estadistico(repositorio)
            mostrar_libro_sorpresa(repositorio)
        elif opcion == "8":
            registrar_prestamo_consola(repositorio)
        elif opcion == "0":
            print("\nGracias por utilizar BiblioLogos. Hasta pronto.")
            break
        else:
            print("Opción no válida. Por favor ingrese un número del 0 al 8.")


if __name__ == "__main__":
    iniciar_menu_consola()
