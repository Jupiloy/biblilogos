"""Genera el informe técnico en formato DOCX."""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Inches, Pt


RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "entregables"


def agregar_encabezado(documento, titulo):
    parrafo = documento.add_heading(titulo, level=1)
    parrafo.alignment = WD_ALIGN_PARAGRAPH.LEFT


def agregar_bullets(documento, elementos):
    for elemento in elementos:
        documento.add_paragraph(elemento, style="List Bullet")


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    documento = Document()
    estilos = documento.styles
    estilos["Normal"].font.name = "Calibri"
    estilos["Normal"].font.size = Pt(11)

    titulo = documento.add_paragraph()
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = titulo.add_run("BIBLIOLOGOS")
    run.bold = True
    run.font.size = Pt(26)
    subtitulo = documento.add_paragraph()
    subtitulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitulo.add_run(
        "Sistema gestor y recomendador inteligente de libros\n"
        "Proyecto integrador de programación multiparadigma"
    )
    run.font.size = Pt(16)

    for texto in (
        "Curso: Lenguajes de Programación – 100000SI68",
        "Carrera: Ingeniería de Software / Ingeniería de Sistemas",
        "Integrantes: [Completar nombres]",
        "Docente: [Completar nombre]",
        "Periodo académico: [Completar]",
        "Fecha de entrega: Semana 18",
    ):
        parrafo = documento.add_paragraph(texto)
        parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    documento.add_page_break()
    agregar_encabezado(documento, "Índice")
    campo = documento.add_paragraph()
    campo.add_run(
        'Para actualizar el índice: clic derecho sobre esta página y seleccionar "Actualizar campo".'
    )

    documento.add_page_break()
    agregar_encabezado(documento, "1. Introducción")
    documento.add_paragraph(
        "BiblioLogos es una solución informática para organizar publicaciones bibliográficas, "
        "consultar su información, recomendar títulos y analizar indicadores del catálogo. "
        "El proyecto integra una aplicación de consola, una interfaz Tkinter y una interfaz web "
        "Angular apoyada por una API FastAPI."
    )

    agregar_encabezado(documento, "2. Descripción de la problemática")
    documento.add_paragraph(
        "Las bibliotecas y catálogos digitales requieren búsquedas, clasificación, reglas de "
        "recomendación y estadísticas. Un único paradigma no muestra de forma explícita todos los "
        "fundamentos requeridos por el curso. BiblioLogos combina los enfoques funcional, lógico "
        "simulado, orientado a objetos y el análisis de datos."
    )

    agregar_encabezado(documento, "3. Justificación")
    documento.add_paragraph(
        "El caso permite demostrar estructuras de datos, herencia, funciones puras, funciones de "
        "orden superior, hechos y reglas simuladas, consultas CRUD, Pandas y NumPy en un contexto "
        "relevante y verificable."
    )

    agregar_encabezado(documento, "4. Objetivos")
    documento.add_heading("Objetivo general", level=2)
    documento.add_paragraph(
        "Desarrollar un sistema bibliográfico multiparadigma que permita registrar, consultar, "
        "actualizar, eliminar y analizar publicaciones, además de recomendar libros."
    )
    documento.add_heading("Objetivos específicos", level=2)
    agregar_bullets(documento, [
        "Aplicar funciones puras, lambdas, filter, map, reduce y funciones de orden superior.",
        "Simular hechos, predicados, unificación, recursividad y resolución lógica.",
        "Implementar POO, herencia, validaciones y patrones Fábrica y Repositorio.",
        "Utilizar NumPy y Pandas para calcular indicadores y exportar reportes CSV.",
        "Ejecutar casos de prueba y documentar evidencias de funcionamiento.",
    ])

    agregar_encabezado(documento, "5. Alcance y limitaciones")
    documento.add_paragraph(
        "El alcance incluye publicaciones físicas y digitales, lectores, préstamos, búsqueda, "
        "recomendaciones y estadísticas. La solución lógica es una simulación en Python aprobada "
        "por las indicaciones del curso; no utiliza un motor SWI-Prolog real."
    )

    agregar_encabezado(documento, "6. Requerimientos funcionales y no funcionales")
    tabla = documento.add_table(rows=1, cols=2)
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla.style = "Table Grid"
    tabla.rows[0].cells[0].text = "Tipo"
    tabla.rows[0].cells[1].text = "Requerimiento"
    for tipo, texto in [
        ("Funcional", "Registrar, consultar, actualizar y eliminar publicaciones."),
        ("Funcional", "Buscar por texto y género."),
        ("Funcional", "Generar recomendaciones con reglas de autor y género."),
        ("Funcional", "Calcular estadísticas y reportes."),
        ("No funcional", "Validar datos antes de crear o actualizar registros."),
        ("No funcional", "Organizar el programa en módulos con responsabilidades claras."),
        ("No funcional", "Permitir ejecución por consola, escritorio y API web."),
    ]:
        fila = tabla.add_row().cells
        fila[0].text = tipo
        fila[1].text = texto

    agregar_encabezado(documento, "7. Diseño de la solución")
    documento.add_heading("Arquitectura modular", level=2)
    agregar_bullets(documento, [
        "modelos.py: POO, validaciones, publicaciones, lectores y repositorio.",
        "motor_funcional.py: filtros, transformaciones, reduce y pipeline.",
        "motor_logico.py: hechos, unificación, recursividad, estrategia y corte.",
        "analisis_datos.py: carga CSV, NumPy, Pandas e informes.",
        "backend/: API REST, servicios, esquemas y caché bibliográfico.",
        "frontend/: interfaz Angular que consume FastAPI.",
        "tests/: casos unitarios y datos de prueba.",
    ])

    agregar_encabezado(documento, "8. Desarrollo de la programación funcional")
    documento.add_paragraph(
        "El motor funcional usa lambdas, filter y map para filtrar y transformar el catálogo. "
        "functools.reduce acumula las páginas. procesar_catalogo recibe una función de "
        "transformación como parámetro y ejecutar_pipeline_analisis encadena las operaciones "
        "sin modificar el catálogo original."
    )

    agregar_encabezado(documento, "9. Desarrollo de la programación lógica")
    documento.add_paragraph(
        "BaseConocimiento representa hechos es_autor, es_genero y le_gusta. unificar compara "
        "variables y constantes. existe_en_lista aplica recursividad cabeza/cola. El motor "
        "recomienda publicaciones nuevas y usa backtracking o corte para controlar las soluciones."
    )

    agregar_encabezado(documento, "10. Multiparadigma y POO")
    documento.add_paragraph(
        "Publicacion define atributos comunes y LibroFisico/Ebook heredan de ella. La fábrica "
        "centraliza la creación y el repositorio índice publicaciones con diccionarios. El programa "
        "también usa tuplas inmutables, listas, variables, operadores, condicionales y ciclos."
    )

    agregar_encabezado(documento, "11. Aplicación de NumPy y Pandas")
    documento.add_paragraph(
        "analisis_datos.py carga el archivo CSV con Pandas, valida los tipos y genera indicadores "
        "mediante NumPy: promedio, mediana, suma de páginas y horas estimadas. Pandas agrupa por "
        "género y exporta CSV de publicaciones por género e indicadores."
    )

    agregar_encabezado(documento, "12. CRUD y API")
    documento.add_paragraph(
        "El repositorio permite agregar, buscar, actualizar y eliminar publicaciones. La API "
        "FastAPI expone POST, GET, PUT y DELETE para las operaciones principales."
    )

    agregar_encabezado(documento, "13. Pruebas y resultados")
    documento.add_paragraph(
        "Se implementaron seis pruebas Python: CSV y Pandas/NumPy, duplicados, CRUD, pipeline "
        "funcional, unificación y recursividad, e inferencia lógica."
    )
    tabla = documento.add_table(rows=1, cols=3)
    tabla.style = "Table Grid"
    tabla.rows[0].cells[0].text = "Grupo"
    tabla.rows[0].cells[1].text = "Casos"
    tabla.rows[0].cells[2].text = "Resultado"
    for fila in (
        ("Ciencia de datos", "Carga CSV e indicadores", "Aprobado"),
        ("POO y CRUD", "Crear, actualizar, eliminar y duplicados", "Aprobado"),
        ("Funcional", "Pipeline y recálculo", "Aprobado"),
        ("Lógica", "Unificación, recursividad e inferencia", "Aprobado"),
    ):
        celdas = tabla.add_row().cells
        for index, texto in enumerate(fila):
            celdas[index].text = texto

    agregar_encabezado(documento, "14. Comparación de paradigmas")
    tabla = documento.add_table(rows=1, cols=3)
    tabla.style = "Table Grid"
    for index, texto in enumerate(("Paradigma", "Ventaja", "Uso en BiblioLogos")):
        tabla.rows[0].cells[index].text = texto
    for fila in (
        ("Funcional", "Transformaciones declarativas y predecibles.", "Filter, map, reduce y pipeline."),
        ("Lógico", "Hechos y reglas expresan relaciones.", "Recomendación por autor y género."),
        ("Multiparadigma", "Combina estructuras y comportamiento.", "API, POO, control de flujo y datos."),
    ):
        celdas = tabla.add_row().cells
        for index, texto in enumerate(fila):
            celdas[index].text = texto

    agregar_encabezado(documento, "15. Evidencias de ejecución")
    agregar_bullets(documento, [
        "Ejecutar: python main.py",
        "Ejecutar pruebas: python -m unittest discover -s tests -v",
        "Ejecutar API: uvicorn backend.main:app --reload --port 8000",
        "Ejecutar análisis: python -m analisis_datos",
        "Capturar imágenes de consola, API, interfaz web y pruebas para anexarlas.",
    ])

    agregar_encabezado(documento, "16. Conclusiones")
    documento.add_paragraph(
        "El proyecto demuestra la integración de los paradigmas y las herramientas obligatorias "
        "en una solución funcional. La simulación lógica permite explicar hechos, reglas y "
        "unificación sin requerir Prolog real. NumPy y Pandas completan el análisis de datos."
    )

    agregar_encabezado(documento, "17. Recomendaciones")
    documento.add_paragraph(
        "Persistir las publicaciones mediante SQLite en todas las interfaces, añadir autenticación "
        "y roles, completar operaciones CRUD desde la GUI, incorporar exportación web y ampliar "
        "las pruebas de API."
    )

    agregar_encabezado(documento, "18. Referencias bibliográficas")
    agregar_bullets(documento, [
        "Documentación oficial de Python.",
        "Documentación oficial de Pandas.",
        "Documentación oficial de NumPy.",
        "Documentación oficial de FastAPI.",
        "Documentación oficial de Angular.",
        "Indicaciones del proyecto final: PROYECTO FINAL DEL CURSO.pdf.",
    ])

    agregar_encabezado(documento, "19. Anexos")
    documento.add_heading("Anexo A — Archivo de datos", level=2)
    documento.add_paragraph("Ubicación: tests/fixtures/catalogo_pruebas.csv")
    documento.add_heading("Anexo B — Casos de prueba", level=2)
    documento.add_paragraph("Ubicación: tests/")
    documento.add_heading("Anexo C — Informe reproducible", level=2)
    documento.add_paragraph("El documento puede regenerarse con: python scripts/generar_informe.py")

    ruta = SALIDA / "Informe_Tecnico_BiblioLogos.docx"
    documento.save(ruta)
    print(ruta)


if __name__ == "__main__":
    main()
