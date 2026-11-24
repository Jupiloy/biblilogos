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


def agregar_imagen(documento, ruta, ancho=6.3, pie=None):
    parrafo = documento.add_paragraph()
    parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    parrafo.add_run().add_picture(str(ruta), width=Inches(ancho))
    if pie:
        pie_parrafo = documento.add_paragraph(pie)
        pie_parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pie_parrafo.runs[0].italic = True


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
    agregar_bullets(documento, [
        "1. Introducción",
        "2. Descripción de la problemática",
        "3. Justificación",
        "4. Objetivos",
        "5. Alcance y limitaciones",
        "6. Requerimientos funcionales y no funcionales",
        "7. Diseño de la solución",
        "8. Desarrollo de la programación funcional",
        "9. Desarrollo de la programación lógica",
        "10. Multiparadigma y POO",
        "11. Aplicación de NumPy y Pandas",
        "12. CRUD y API",
        "13. Pruebas y resultados",
        "14. Comparación de paradigmas",
        "15. Evidencias de ejecución",
        "16. Conclusiones",
        "17. Recomendaciones",
        "18. Referencias bibliográficas",
        "19. Anexos",
    ])

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
    documento.add_heading("Situación actual", level=2)
    documento.add_paragraph(
        "Un catálogo bibliográfico puede crecer hasta contener cientos de publicaciones. "
        "Localizar títulos por texto o género, evitar duplicados, mantener lectores y préstamos, "
        "sugerir lecturas y producir indicadores son procesos que requieren validaciones, reglas "
        "claras y una estructura mantenible."
    )
    documento.add_heading("Impacto del problema", level=2)
    documento.add_paragraph(
        "Sin una solución organizada, la búsqueda manual consume tiempo, los registros pueden "
        "duplicarse y no existen criterios consistentes para recomendar títulos. Tampoco se "
        "obtienen indicadores sobre la cantidad de publicaciones, sus páginas o sus calificaciones "
        "sin realizar cálculos manuales."
    )
    documento.add_heading("Propuesta de solución", level=2)
    documento.add_paragraph(
        "BiblioLogos propone un catálogo indexado por ISBN, interfaces en consola y web, una API "
        "FastAPI, recomendaciones derivadas de autor y género, operaciones CRUD y análisis con "
        "Pandas/NumPy. Las interfaces muestran el mismo núcleo de dominio y evitan duplicar reglas "
        "de negocio críticas."
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
    documento.add_heading("Incluido", level=2)
    agregar_bullets(documento, [
        "Catálogo inicial de publicaciones físicas y digitales.",
        "Registro, búsqueda, actualización y eliminación de publicaciones.",
        "Registro de lectores y asociación de libros leídos.",
        "Recomendaciones por autor, género y calificación.",
        "Filtros funcionales, estadísticas y exportación CSV.",
        "Interfaz de consola, escritorio Tkinter y aplicación Angular.",
    ])
    documento.add_heading("Limitado o no incluido", level=2)
    agregar_bullets(documento, [
        "No se implementó autenticación ni roles de usuario.",
        "El motor lógico simulado representa hechos y resolución en Python.",
        "El catálogo web puede consultar Open Library y usar una caché SQLite.",
        "Las operaciones CRUD principales están persistidas en memoria del repositorio durante la ejecución.",
        "El informe final debe completar datos institucionales y nombres reales del equipo.",
    ])

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
    agregar_imagen(
        documento,
        SALIDA / "diagramas" / "arquitectura_general.png",
        6.4,
        "Figura 1. Arquitectura general del sistema.",
    )
    documento.add_heading("Diagrama de flujo de procesos", level=2)
    documento.add_paragraph(
        "El usuario inicia una operación desde consola, Tkinter o Angular. Las operaciones del "
        "dominio pasan por validaciones y servicios. Una consulta puede leer el repositorio local "
        "o la caché/Open Library; una operación funcional transforma colecciones; una operación "
        "lógica carga hechos y devuelve recomendaciones."
    )
    documento.add_heading("Estructuras de datos", level=2)
    tabla = documento.add_table(rows=1, cols=3)
    tabla.style = "Table Grid"
    for index, texto in enumerate(("Estructura", "Uso", "Razón")):
        tabla.rows[0].cells[index].text = texto
    for fila in (
        ("Lista", "Catálogo, lectores y soluciones", "Permite iterar y transformar elementos."),
        ("Tupla", "Ficha inmutable (ISBN, título, autor)", "Representa datos que no deberían cambiar."),
        ("Diccionario", "Índices por ISBN y código de lector", "Acceso directo y búsqueda por clave."),
        ("DataFrame", "Análisis del catálogo CSV", "Filtrado, agregación y exportación tabular."),
        ("ndarray", "Cálculos numéricos vectoriales", "Operaciones eficientes con NumPy."),
    ):
        celdas = tabla.add_row().cells
        for index, texto in enumerate(fila):
            celdas[index].text = texto

    agregar_encabezado(documento, "8. Desarrollo de la programación funcional")
    documento.add_paragraph(
        "El motor funcional usa lambdas, filter y map para filtrar y transformar el catálogo. "
        "functools.reduce acumula las páginas. procesar_catalogo recibe una función de "
        "transformación como parámetro y ejecutar_pipeline_analisis encadena las operaciones "
        "sin modificar el catálogo original."
    )
    documento.add_heading("Funciones puras e inmutabilidad", level=2)
    documento.add_paragraph(
        "Las funciones filtrar_por_calificacion y filtrar_por_genero reciben colecciones y "
        "devuelven nuevas listas. Las transformaciones tampoco modifican las publicaciones "
        "originales. Una tupla representa cada ficha resumida y reduce recibe un acumulador "
        "explícito; de esta forma se facilita la explicación y la prueba del comportamiento."
    )
    agregar_imagen(
        documento,
        SALIDA / "diagramas" / "flujo_funcional.png",
        6.4,
        "Figura 2. Pipeline funcional filter -> map -> reduce.",
    )
    documento.add_heading("Funciones anónimas y de orden superior", level=2)
    agregar_bullets(documento, [
        "lambda libro: libro.calificacion >= umbral filtra por calificación.",
        "lambda libro: libro.genero.lower() == objetivo filtra por género.",
        "map() aplica lambdas o procesar_catalogo() a cada publicación.",
        "reduce() acumula páginas mediante una función de dos parámetros.",
        "procesar_catalogo() recibe la transformación como parámetro.",
    ])

    agregar_encabezado(documento, "9. Desarrollo de la programación lógica")
    documento.add_paragraph(
        "BaseConocimiento representa hechos es_autor, es_genero y le_gusta. unificar compara "
        "variables y constantes. existe_en_lista aplica recursividad cabeza/cola. El motor "
        "recomienda publicaciones nuevas y usa backtracking o corte para controlar las soluciones."
    )
    documento.add_heading("Hechos, predicados y reglas", level=2)
    tabla = documento.add_table(rows=1, cols=3)
    tabla.style = "Table Grid"
    for index, texto in enumerate(("Elemento lógico", "Representación", "Ejemplo")):
        tabla.rows[0].cells[index].text = texto
    for fila in (
        ("Hecho", "Dato cargado en diccionario", "es_genero(P-2, Ficción)."),
        ("Predicado", "Método de consulta", "es_autor(PRUEBA-002)."),
        ("Regla", "Estrategia que combina predicados", "Mismo autor o mismo género."),
        ("Consulta", "Llamada al motor", "recomendar_libros(lector)."),
        ("Resolución", "Búsqueda y ordenamiento", "Candidatas y puntaje de afinidad."),
    ):
        celdas = tabla.add_row().cells
        for index, texto in enumerate(fila):
            celdas[index].text = texto
    agregar_imagen(
        documento,
        SALIDA / "diagramas" / "flujo_logico.png",
        6.4,
        "Figura 3. Motor lógico simulado, backtracking y corte.",
    )
    documento.add_paragraph(
        "Unificación: el prefijo mayúsculo identifica una variable lógica. Por ejemplo, "
        "unificar('Autor', 'Borges') enlaza Autor con Borges. La recursividad existe_en_lista "
        "separa cada colección en cabeza y cola, con la lista vacía como caso base."
    )

    agregar_encabezado(documento, "10. Multiparadigma y POO")
    documento.add_paragraph(
        "Publicacion define atributos comunes y LibroFisico/Ebook heredan de ella. La fábrica "
        "centraliza la creación y el repositorio índice publicaciones con diccionarios. El programa "
        "también usa tuplas inmutables, listas, variables, operadores, condicionales y ciclos."
    )
    agregar_imagen(
        documento,
        SALIDA / "diagramas" / "diagrama_clases.png",
        6.4,
        "Figura 4. Diagrama de clases simplificado.",
    )
    documento.add_heading("Clases principales", level=2)
    agregar_bullets(documento, [
        "Publicacion: ISBN, título, autor, género, páginas y calificación.",
        "LibroFisico: hereda de Publicacion y añade stock y ubicación.",
        "Ebook: hereda de Publicacion y añade formato y peso.",
        "Lector: código, nombre, correo, categoría y libros leídos.",
        "FabricaPublicaciones: aplica el patrón Fábrica.",
        "RepositorioBiblioteca: aplica índices Singleton y operaciones CRUD.",
    ])

    agregar_encabezado(documento, "11. Aplicación de NumPy y Pandas")
    documento.add_paragraph(
        "analisis_datos.py carga el archivo CSV con Pandas, valida los tipos y genera indicadores "
        "mediante NumPy: promedio, mediana, suma de páginas y horas estimadas. Pandas agrupa por "
        "género y exporta CSV de publicaciones por género e indicadores."
    )
    agregar_imagen(
        documento,
        SALIDA / "diagramas" / "flujo_datos.png",
        6.4,
        "Figura 5. Flujo de análisis de datos.",
    )
    documento.add_heading("Operaciones demostradas", level=2)
    agregar_bullets(documento, [
        "Pandas read_csv carga el archivo de prueba.",
        "Pandas to_numeric convierte y valida columnas numéricas.",
        "Pandas groupby agrega publicaciones por género.",
        "NumPy mean calcula el promedio de calificaciones.",
        "NumPy median calcula la mediana.",
        "NumPy sum obtiene el total de páginas.",
        "NumPy ceil redondea hacia arriba las horas estimadas.",
    ])

    agregar_encabezado(documento, "12. CRUD y API")
    documento.add_paragraph(
        "El repositorio permite agregar, buscar, actualizar y eliminar publicaciones. La API "
        "FastAPI expone POST, GET, PUT y DELETE para las operaciones principales."
    )
    agregar_imagen(
        documento,
        SALIDA / "diagramas" / "flujo_crud.png",
        6.4,
        "Figura 6. Flujo CRUD y validación mediante API.",
    )
    tabla = documento.add_table(rows=1, cols=4)
    tabla.style = "Table Grid"
    for index, texto in enumerate(("Operación", "Método", "Ruta", "Resultado")):
        tabla.rows[0].cells[index].text = texto
    for fila in (
        ("Crear", "POST", "/api/publicaciones", "Código 201"),
        ("Consultar", "GET", "/api/publicaciones", "Lista de publicaciones"),
        ("Buscar detalle", "GET", "/api/publicaciones/{isbn}", "Publicación o 404"),
        ("Actualizar", "PUT", "/api/publicaciones/{isbn}", "Objeto actualizado"),
        ("Eliminar", "DELETE", "/api/publicaciones/{isbn}", "ISBN eliminado"),
    ):
        celdas = tabla.add_row().cells
        for index, texto in enumerate(fila):
            celdas[index].text = texto

    agregar_encabezado(documento, "13. Pruebas y resultados")
    documento.add_paragraph(
        "Se implementaron seis pruebas Python: CSV y Pandas/NumPy, duplicados, CRUD, pipeline "
        "funcional, unificación y recursividad, e inferencia lógica."
    )
    documento.add_heading("Diseño de pruebas", level=2)
    documento.add_paragraph(
        "Las pruebas automatizadas utilizan unittest y datos controlados. Se validan efectos "
        "observables, no solamente la existencia de funciones: cantidades filtradas, páginas "
        "totales, horas redondeadas, ligaduras de unificación, recomendaciones y operaciones CRUD."
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
    documento.add_heading("Caso de prueba resumido", level=2)
    tabla = documento.add_table(rows=1, cols=4)
    tabla.style = "Table Grid"
    for index, texto in enumerate(("Entrada", "Proceso", "Resultado esperado", "Resultado obtenido")):
        tabla.rows[0].cells[index].text = texto
    for fila in (
        ("3 registros CSV", "Pandas + NumPy", "3 libros, 1010 páginas, 26 horas", "Aprobado"),
        ("Libro TEST-001", "Actualizar stock/título", "Nuevos datos visibles", "Aprobado"),
        ("Catálogo P-1/P-2", "Pipeline funcional", "Solo filtro de 4.6+", "Aprobado"),
        ("Autor variable", "unificar('Autor','Borges')", "Ligadura Autor=Borges", "Aprobado"),
        ("POST/PUT/DELETE", "API FastAPI", "201, 200 y eliminación", "Aprobado"),
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
    documento.add_heading("Evidencia de compilación", level=2)
    documento.add_paragraph(
        "python -m compileall verificó los módulos Python del proyecto. La construcción Angular "
        "obtuvo una salida exitosa y las pruebas Angular ejecutaron dos casos con éxito."
    )
    documento.add_heading("Evidencia de pruebas", level=2)
    documento.add_paragraph(
        "La suite unittest ejecutó seis pruebas sin errores ni fallos. Las pruebas cubren los "
        "componentes funcional, lógico, POO/CRUD y ciencia de datos."
    )
    documento.add_heading("Rúbrica de evidencias a completar", level=2)
    tabla = documento.add_table(rows=1, cols=3)
    tabla.style = "Table Grid"
    for index, texto in enumerate(("Evidencia", "Estado", "Anexo sugerido")):
        tabla.rows[0].cells[index].text = texto
    for fila in (
        ("Pruebas Python", "Generada", "Captura de terminal"),
        ("API POST/PUT/DELETE", "Generada", "Captura de respuestas"),
        ("Interfaz Angular", "Generada", "Captura del navegador"),
        ("Pipeline funcional", "Código disponible", "Captura de consola"),
        ("Motor lógico", "Código disponible", "Captura de recomendaciones"),
        ("Pandas/NumPy", "Código y CSV disponibles", "Captura e indicadores"),
    ):
        celdas = tabla.add_row().cells
        for index, texto in enumerate(fila):
            celdas[index].text = texto

    agregar_encabezado(documento, "16. Conclusiones")
    documento.add_paragraph(
        "El proyecto demuestra la integración de los paradigmas y las herramientas obligatorias "
        "en una solución funcional. La simulación lógica permite explicar hechos, reglas y "
        "unificación sin requerir Prolog real. NumPy y Pandas completan el análisis de datos."
    )
    documento.add_paragraph(
        "La separación en módulos permitió localizar responsabilidades: modelos, funcionalidad "
        "pura, inferencia, persistencia, API y análisis. Los casos de prueba proporcionaron "
        "evidencia verificable de que las reglas críticas producen los resultados esperados."
    )
    documento.add_paragraph(
        "Las principales limitaciones son la persistencia CRUD limitada en memoria para el "
        "repositorio principal y la ausencia de autenticación. Estas mejoras no impiden demostrar "
        "el núcleo académico y pueden implementarse en una segunda versión."
    )

    agregar_encabezado(documento, "17. Recomendaciones")
    documento.add_paragraph(
        "Persistir las publicaciones mediante SQLite en todas las interfaces, añadir autenticación "
        "y roles, completar operaciones CRUD desde la GUI, incorporar exportación web y ampliar "
        "las pruebas de API."
    )
    agregar_bullets(documento, [
        "Añadir un archivo de configuración para URLs y constantes.",
        "Completar la actualización y eliminación desde la interfaz Tkinter.",
        "Persistir lectores y préstamos en SQLite.",
        "Ampliar pruebas de errores, validaciones y endpoints.",
        "Agregar datos históricos para análisis temporal.",
        "Publicar capturas reales dentro del informe después de cada demostración.",
    ])

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
    documento.add_paragraph(
        "El archivo contiene ISBN, título, autor, género, páginas, calificación, tipo y atributos "
        "específicos de publicaciones físicas o digitales."
    )
    documento.add_heading("Anexo B — Casos de prueba", level=2)
    documento.add_paragraph("Ubicación: tests/")
    documento.add_paragraph(
        "Los casos están separados por modelo/CRUD, paradigmas y ciencia de datos para facilitar "
        "la ejecución y la ubicación de errores."
    )
    documento.add_heading("Anexo C — Fuentes de diagramas", level=2)
    documento.add_paragraph(
        "Los archivos PNG y SVG se generan con Graphviz. Las versiones editables .drawio pueden "
        "abrirse en diagrams.net, draw.io o Visual Studio Code."
    )
    for ruta in sorted((SALIDA / "diagramas").glob("*.drawio")):
        documento.add_paragraph(ruta.name)
    documento.add_heading("Anexo C — Informe reproducible", level=2)
    documento.add_paragraph("El documento puede regenerarse con: python scripts/generar_informe.py")

    ruta = SALIDA / "Informe_Tecnico_BiblioLogos.docx"
    documento.save(ruta)
    print(ruta)


if __name__ == "__main__":
    main()
