"""Genera una presentación breve con evidencias reales de BiblioLogos."""

from pathlib import Path
import subprocess
import sys

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
DELIVERABLES = ROOT / "entregables"
CAPTURES = DELIVERABLES / "capturas"
DIAGRAMS = DELIVERABLES / "diagramas"
OUTPUT = DELIVERABLES / "Presentacion_BiblioLogos.pptx"

WIDTH = 13.333
HEIGHT = 7.5
BG = "F4F7FB"
NAVY = "132238"
TEAL = "0D9488"
PALE_BLUE = "E8F2F7"
WHITE = "FFFFFF"
TEXT = "172536"
MUTED = "5B6B7E"
DARK = "18202D"
GREEN = "DCFCE7"
YELLOW = "FEF3C7"


def rgb(value):
    return RGBColor.from_string(value)


def add_text(slide, value, x, y, width, height, size=17, tone=TEXT,
             bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(width), Inches(height)
    )
    box.fill.background()
    box.line.fill.background()
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(0.06)
    frame.margin_right = Inches(0.06)
    frame.margin_top = Inches(0.03)
    frame.margin_bottom = Inches(0.03)
    frame.vertical_anchor = anchor
    paragraph = frame.paragraphs[0]
    paragraph.text = value
    paragraph.alignment = align
    for run in paragraph.runs:
        run.font.name = "Aptos"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = rgb(tone)
    return box


def add_shape(slide, kind, x, y, width, height, fill):
    result = slide.shapes.add_shape(
        kind, Inches(x), Inches(y), Inches(width), Inches(height)
    )
    result.fill.solid()
    result.fill.fore_color.rgb = rgb(fill)
    result.line.color.rgb = rgb(fill)
    return result


def add_panel(slide, x, y, width, height, fill=WHITE):
    return add_shape(
        slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, width, height, fill
    )


def add_bullets(slide, items, x, y, width, size=16, spacing=0.57):
    for index, item in enumerate(items):
        add_text(
            slide,
            f"•  {item}",
            x,
            y + index * spacing,
            width,
            spacing,
            size,
        )


def add_image_fit(slide, path, x, y, box_width, box_height):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Falta evidencia visual: {path}")
    with Image.open(path) as image:
        image_width, image_height = image.size
    scale = min(box_width / image_width, box_height / image_height)
    width = image_width * scale
    height = image_height * scale
    return slide.shapes.add_picture(
        str(path),
        Inches(x + (box_width - width) / 2),
        Inches(y + (box_height - height) / 2),
        Inches(width),
        Inches(height),
    )


def add_capture(slide, name, x, y, width, height):
    return add_image_fit(slide, CAPTURES / name, x, y, width, height)


def add_diagram(slide, name, x, y, width, height):
    return add_image_fit(slide, DIAGRAMS / name, x, y, width, height)


def add_footer(slide, number, minutes):
    add_text(slide, f"Exposición · máximo 10 min · {minutes}", 0.62, 7.1,
             10.8, 0.2, 9, MUTED)
    add_text(slide, f"{number:02d}", 12.15, 7.08, 0.55, 0.22, 10, MUTED,
             True, PP_ALIGN.RIGHT)


def new_slide(prs, number, section, title, minutes):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = rgb(BG)
    add_text(slide, section.upper(), 0.55, 0.16, 11.5, 0.26, 10, TEAL, True)
    add_text(slide, title, 0.55, 0.47, 12.2, 0.58, 27, NAVY, True)
    add_shape(slide, MSO_SHAPE.RECTANGLE, 0.58, 1.08, 0.68, 0.05, TEAL)
    add_footer(slide, number, minutes)
    return slide


def add_code_slide(prs, number, section, title, minutes, image, summary,
                   source):
    slide = new_slide(prs, number, section, title, minutes)
    add_panel(slide, 0.68, 1.4, 8.45, 5.2, DARK)
    add_capture(slide, image, 0.84, 1.52, 8.13, 4.95)
    add_panel(slide, 9.42, 1.4, 3.2, 5.2, PALE_BLUE)
    add_text(slide, "Para explicar", 9.7, 1.76, 2.65, 0.4, 17, NAVY, True)
    add_text(slide, summary, 9.7, 2.35, 2.6, 2.9, 15, TEXT)
    add_text(slide, source, 9.7, 5.73, 2.6, 0.6, 10, MUTED)
    return slide


def build_presentation():
    subprocess.run(
        [sys.executable, "-m", "scripts.generar_capturas_codigo"],
        cwd=ROOT,
        check=True,
    )
    prs = Presentation()
    prs.slide_width = Inches(WIDTH)
    prs.slide_height = Inches(HEIGHT)
    prs.core_properties.title = "BiblioLogos — Proyecto multiparadigma"
    prs.core_properties.subject = "Explicación del problema, solución, arquitectura y temas del curso"
    prs.core_properties.author = "Equipo BiblioLogos"

    # 1. Portada (20 s)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = rgb(NAVY)
    add_shape(slide, MSO_SHAPE.RECTANGLE, 0, 0, 0.22, HEIGHT, TEAL)
    add_panel(slide, 0.82, 0.8, 2.65, 0.42, "1D344A")
    add_text(slide, "PROYECTO INTEGRADOR", 0.95, 0.9, 2.4, 0.2, 10,
             "A8F0E7", True, PP_ALIGN.CENTER)
    add_text(slide, "BIBLIOLOGOS", 0.82, 1.55, 9.5, 0.8, 38, WHITE, True)
    add_text(
        slide,
        "Gestor y recomendador inteligente de libros",
        0.84,
        2.42,
        10.5,
        0.55,
        23,
        "D9E5F2",
    )
    add_text(
        slide,
        "Funcional · lógica simulada · POO · Pandas y NumPy",
        0.84,
        3.12,
        11.3,
        0.42,
        16,
        "A8F0E7",
        True,
    )
    add_panel(slide, 0.82, 3.82, 9.2, 2.25, "1D344A")
    add_text(
        slide,
        "INTEGRANTES\n"
        "Julio Aldieri Noblecilla Rondoy\n"
        "Marcos Lachira Ruiz · Frank Velasquez Lopez\n"
        "Anderson Abad Huertas Padro",
        1.08,
        4.05,
        8.6,
        1.35,
        15,
        WHITE,
    )
    add_text(
        slide,
        "Lenguajes de Programación · 100000SI68\nDuración prevista: 9:30 · margen: 0:30",
        0.84,
        6.35,
        8.7,
        0.55,
        12,
        "D9E5F2",
    )

    # 2. Problemática (40 s)
    slide = new_slide(prs, 2, "Problema", "¿Qué necesidad aborda BiblioLogos?", "0:40")
    cards = [
        ("Problemática", "Un catálogo puede crecer y sus libros se vuelven difíciles de localizar, mantener y clasificar."),
        ("Dificultades", "La gestión manual favorece errores o duplicados; recomendar y calcular estadísticas exige trabajo adicional."),
        ("Alcance honesto", "Es un caso académico. No afirmamos haber medido una biblioteca real ni sus tiempos de búsqueda."),
    ]
    for index, (heading, body) in enumerate(cards):
        x = 0.72 + index * 4.18
        add_panel(slide, x, 1.62, 3.78, 3.95, WHITE)
        add_text(slide, heading, x + 0.24, 1.95, 3.3, 0.38, 17, TEAL, True)
        add_text(slide, body, x + 0.24, 2.55, 3.3, 2.45, 16, TEXT)
    add_text(
        slide,
        "Pregunta guía: ¿cómo organizar publicaciones y ayudar a descubrir lecturas de forma clara?",
        0.9,
        5.95,
        11.5,
        0.42,
        16,
        NAVY,
        True,
        PP_ALIGN.CENTER,
    )

    # 3. Objetivos (40 s)
    slide = new_slide(prs, 3, "Objetivos", "Qué nos propusimos lograr", "0:40")
    add_panel(slide, 0.75, 1.55, 4.0, 4.85, NAVY)
    add_text(slide, "OBJETIVO GENERAL", 1.05, 1.9, 3.35, 0.35, 14, "A8F0E7", True)
    add_text(
        slide,
        "Desarrollar un sistema bibliográfico multiparadigma para registrar, consultar, actualizar, eliminar y analizar publicaciones, además de recomendar libros.",
        1.05,
        2.48,
        3.35,
        2.3,
        19,
        WHITE,
    )
    add_text(slide, "OBJETIVOS ESPECÍFICOS", 5.15, 1.75, 6.9, 0.36, 16, TEAL, True)
    add_bullets(
        slide,
        [
            "Procesar el catálogo con funciones puras, lambda, filter, map y reduce.",
            "Representar hechos y simular unificación e inferencia lógica en Python.",
            "Modelar publicaciones mediante clases, herencia y patrones de diseño.",
            "Analizar CSV con Pandas y NumPy y verificar funciones con pruebas.",
        ],
        5.15,
        2.35,
        6.9,
        16,
        0.86,
    )

    # 4. Solución (40 s)
    slide = new_slide(prs, 4, "Solución", "Una aplicación que integra consulta y gestión", "0:40")
    add_panel(slide, 0.68, 1.42, 7.55, 5.2, WHITE)
    add_capture(slide, "busqueda_resultados.png", 0.82, 1.58, 7.25, 4.88)
    add_panel(slide, 8.55, 1.42, 4.08, 5.2, PALE_BLUE)
    add_text(slide, "Qué permite hacer", 8.88, 1.8, 3.45, 0.42, 18, NAVY, True)
    add_bullets(
        slide,
        [
            "Buscar por título, autor o tema.",
            "Explorar y consultar detalles.",
            "Recibir recomendaciones.",
            "Guardar favoritos en el navegador.",
            "Administrar un catálogo local persistente.",
        ],
        8.88,
        2.45,
        3.4,
        14,
        0.72,
    )
    add_text(slide, "La búsqueda externa usa Open Library; Mi catálogo es local.",
             8.88, 6.0, 3.35, 0.42, 11, MUTED)

    # 5. Arquitectura (40 s)
    slide = new_slide(prs, 5, "Arquitectura", "Cómo se organizan las partes", "0:40")
    add_panel(slide, 0.68, 1.4, 11.95, 5.25, WHITE)
    add_diagram(slide, "arquitectura_general.png", 0.9, 1.56, 11.5, 4.92)
    add_text(
        slide,
        "Angular → FastAPI → servicios y modelos → bases SQLite",
        1.0,
        6.35,
        11.3,
        0.24,
        12,
        MUTED,
        align=PP_ALIGN.CENTER,
    )

    # 6. Flujo de datos (35 s)
    slide = new_slide(prs, 6, "Funcionamiento", "De una solicitud a una respuesta", "0:35")
    add_panel(slide, 0.7, 1.5, 7.3, 4.95, WHITE)
    add_diagram(slide, "flujo_crud.png", 0.9, 1.85, 6.9, 4.15)
    add_panel(slide, 8.25, 1.5, 4.35, 4.95, PALE_BLUE)
    add_text(slide, "Pasos", 8.58, 1.85, 3.65, 0.35, 17, NAVY, True)
    add_bullets(
        slide,
        [
            "La interfaz envía una petición HTTP.",
            "FastAPI recibe la ruta y valida el cuerpo.",
            "El servicio aplica reglas del dominio.",
            "SQLite conserva datos del catálogo.",
            "La API devuelve JSON a Angular.",
        ],
        8.58,
        2.4,
        3.6,
        14,
        0.7,
    )

    # 7. POO y modelos (40 s)
    slide = new_slide(prs, 7, "POO", "Clases que representan el dominio", "0:40")
    add_panel(slide, 0.68, 1.4, 7.7, 5.2, WHITE)
    add_diagram(slide, "diagrama_clases.png", 0.92, 1.55, 7.2, 4.9)
    add_panel(slide, 8.62, 1.4, 4.0, 5.2, PALE_BLUE)
    add_text(slide, "Ejemplo de herencia", 8.95, 1.82, 3.4, 0.45, 17, NAVY, True)
    add_text(
        slide,
        "Publicacion contiene los datos comunes. LibroFisico añade stock y ubicación; Ebook añade formato y peso. Ambos sobrescriben mostrar_info() y reutilizan la clase base con super().",
        8.95,
        2.45,
        3.35,
        2.65,
        15,
    )
    add_text(slide, "modelos.py", 8.95, 5.83, 3.3, 0.32, 11, MUTED)

    # 8. Patrones (40 s)
    slide = new_slide(prs, 8, "Diseño", "Patrones usados para organizar responsabilidades", "0:40")
    pattern_cards = [
        ("Factory Method", "FabricaPublicaciones decide y construye LibroFisico o Ebook."),
        ("Singleton", "RepositorioBiblioteca centraliza una única instancia del catálogo en el proceso."),
        ("Strategy", "El motor lógico puede intercambiar reglas: por autor, género o combinación."),
        ("Repositorio", "La clase concentra operaciones de acceso y CRUD del dominio."),
    ]
    positions = [(0.8, 1.55), (6.85, 1.55), (0.8, 4.05), (6.85, 4.05)]
    for (heading, body), (x, y) in zip(pattern_cards, positions):
        add_panel(slide, x, y, 5.65, 2.1, WHITE)
        add_text(slide, heading, x + 0.28, y + 0.28, 5.05, 0.36, 17, TEAL, True)
        add_text(slide, body, x + 0.28, y + 0.82, 5.05, 0.95, 15, TEXT)

    # 9. Funcional (45 s)
    add_code_slide(
        prs,
        9,
        "Programación funcional",
        "El pipeline filter → map → reduce",
        "0:45",
        "codigo_motor_funcional_101_129.png",
        "filter selecciona; map calcula horas estimadas; reduce acumula páginas y tiempo. Las funciones devuelven resultados nuevos y no alteran la lista original.",
        "motor_funcional.py:101–129",
    )

    # 10. Lógica simulada (50 s)
    add_code_slide(
        prs,
        10,
        "Programación lógica",
        "Hechos, unificación y búsqueda de recomendaciones",
        "0:50",
        "codigo_motor_logico_229_256.png",
        "La base registra autor, género y preferencias. Se comparan términos, se exploran candidatos y se ordenan soluciones. Es una simulación didáctica en Python, no un motor Prolog/SLD.",
        "motor_logico.py:229–256",
    )

    # 11. Análisis de datos (40 s)
    slide = new_slide(prs, 11, "Datos", "Pandas y NumPy analizan CSV y SQLite", "0:40")
    add_panel(slide, 0.68, 1.4, 7.65, 5.2, DARK)
    add_capture(slide, "codigo_analisis_datos_27_43.png", 0.85, 1.58, 7.3, 4.85)
    add_panel(slide, 8.58, 1.4, 4.05, 5.2, PALE_BLUE)
    add_text(slide, "Proceso", 8.9, 1.82, 3.4, 0.38, 17, NAVY, True)
    add_bullets(
        slide,
        [
            "Pandas lee y valida columnas.",
            "NumPy calcula promedio, mediana, suma y horas.",
            "Pandas agrupa por género.",
            "Se exportan reportes CSV.",
        ],
        8.9,
        2.42,
        3.35,
        14,
        0.8,
    )
    add_text(
        slide,
        "CSV fijo para pruebas; los reportes reales consultan el SQLite actualizado.",
        8.9,
        5.88,
        3.35,
        0.5,
        11,
        MUTED,
    )

    # 12. CRUD y persistencia (40 s)
    slide = new_slide(prs, 12, "CRUD y persistencia", "Qué se guarda y dónde", "0:40")
    add_panel(slide, 0.75, 1.55, 11.85, 1.15, NAVY)
    add_text(
        slide,
        "CREAR  →  LEER  →  ACTUALIZAR  →  ELIMINAR",
        1.0,
        1.92,
        11.3,
        0.38,
        21,
        WHITE,
        True,
        PP_ALIGN.CENTER,
    )
    storage_cards = [
        ("catalogo.db", "Catálogo local editable; persiste tras reiniciar."),
        ("bibliologos.db", "Caché de búsquedas y publicaciones de Open Library."),
        ("usuarios.db", "Cuentas, roles y sesiones; contraseñas como hash PBKDF2."),
    ]
    for index, (heading, body) in enumerate(storage_cards):
        x = 0.75 + index * 4.0
        add_panel(slide, x, 3.12, 3.72, 2.55, WHITE)
        add_text(slide, heading, x + 0.25, 3.48, 3.22, 0.4, 16, TEAL, True)
        add_text(slide, body, x + 0.25, 4.05, 3.22, 1.22, 15, TEXT)
    add_text(slide, "Son bases separadas para responsabilidades distintas.",
             1.0, 6.05, 11.3, 0.32, 13, MUTED, align=PP_ALIGN.CENTER)

    # 13. Roles y acceso (40 s)
    slide = new_slide(prs, 13, "Acceso", "Dos roles, permisos distintos", "0:40")
    role_cards = [
        ("ADMINISTRADOR", "Inicia sesión con una cuenta creada en el backend. Puede consultar y gestionar el catálogo: crear, editar y eliminar."),
        ("LECTOR", "Puede crear su propia cuenta; puede buscar publicaciones, consultar detalles y recibir recomendaciones. No administra registros."),
    ]
    for index, (heading, body) in enumerate(role_cards):
        x = 0.85 + index * 6.0
        add_panel(slide, x, 1.65, 5.55, 3.55, WHITE)
        add_text(slide, heading, x + 0.35, 2.02, 4.85, 0.4, 18, TEAL, True)
        add_text(slide, body, x + 0.35, 2.7, 4.82, 1.65, 16, TEXT)
    add_panel(slide, 0.85, 5.55, 11.55, 0.75, PALE_BLUE)
    add_text(
        slide,
        "FastAPI comprueba el token y el rol en la API; ocultar botones en Angular no sustituye esa comprobación.",
        1.05,
        5.75,
        11.15,
        0.34,
        13,
        NAVY,
        True,
        PP_ALIGN.CENTER,
    )

    # 14. Validación, límites y alcance (35 s)
    slide = new_slide(prs, 14, "Controles y límites", "Qué limita el sistema y qué falta", "0:35")
    add_panel(slide, 0.75, 1.5, 5.65, 4.95, WHITE)
    add_text(slide, "Controles implementados", 1.05, 1.85, 5.0, 0.4, 17, TEAL, True)
    add_bullets(
        slide,
        [
            "Páginas positivas; calificación de 0 a 5.",
            "Stock no negativo y requisitos por formato.",
            "Búsquedas limitadas a 100; recomendaciones a 20.",
            "Open Library tiene timeout y la búsqueda puede recurrir al catálogo local.",
        ],
        1.05,
        2.48,
        5.0,
        14,
        0.78,
    )
    add_panel(slide, 6.75, 1.5, 5.65, 4.95, PALE_BLUE)
    add_text(slide, "Límites actuales", 7.05, 1.85, 5.0, 0.4, 17, NAVY, True)
    add_bullets(
        slide,
        [
            "Prototipo académico, no despliegue productivo.",
            "Sin recuperación de contraseña ni panel para administrar cuentas.",
            "Sin respaldo automático de las bases SQLite.",
            "La simulación lógica no es Prolog formal.",
        ],
        7.05,
        2.48,
        5.0,
        14,
        0.88,
    )

    # 15. Pruebas y cierre (25 s)
    slide = new_slide(prs, 15, "Cierre", "Un problema, varios paradigmas", "0:25")
    summary_cards = [
        ("FUNCIONAL", "Transformar y resumir"),
        ("LÓGICA", "Relacionar hechos"),
        ("POO", "Modelar el dominio"),
        ("DATOS", "Medir y reportar"),
    ]
    for index, (heading, body) in enumerate(summary_cards):
        x = 0.68 + index * 3.15
        add_panel(slide, x, 1.65, 2.85, 1.45, WHITE)
        add_text(slide, heading, x + 0.18, 1.92, 2.5, 0.3, 12, TEAL, True)
        add_text(slide, body, x + 0.18, 2.35, 2.5, 0.45, 15, NAVY, True)
    add_panel(slide, 0.85, 3.55, 11.55, 1.1, NAVY)
    add_text(slide, "14 pruebas Python · 4 pruebas Angular", 1.05, 3.9, 11.15, 0.35,
             19, WHITE, True, PP_ALIGN.CENTER)
    add_text(
        slide,
        "BiblioLogos integra búsqueda, catálogo, recomendaciones y análisis. Gracias. ¿Preguntas?",
        1.0,
        5.35,
        11.3,
        0.5,
        17,
        MUTED,
        align=PP_ALIGN.CENTER,
    )

    DELIVERABLES.mkdir(parents=True, exist_ok=True)
    prs.save(OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    print(build_presentation())
