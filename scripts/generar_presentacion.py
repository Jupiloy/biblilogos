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
    prs.core_properties.title = "BiblioLogos — Exposición de 10 minutos"
    prs.core_properties.subject = (
        "Presentación concisa con evidencias de aplicación y código"
    )
    prs.core_properties.author = "Equipo BiblioLogos"

    # 1. Portada (20 s)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = rgb(NAVY)
    add_shape(slide, MSO_SHAPE.RECTANGLE, 0, 0, 0.22, HEIGHT, TEAL)
    add_panel(slide, 0.82, 0.8, 2.65, 0.42, "1D344A")
    add_text(slide, "PROYECTO INTEGRADOR", 0.95, 0.9, 2.4, 0.2, 10,
             "A8F0E7", True, PP_ALIGN.CENTER)
    add_text(slide, "BIBLIOLOGOS", 0.82, 1.65, 9.5, 0.8, 38, WHITE, True)
    add_text(
        slide,
        "Gestor y recomendador inteligente de libros",
        0.84,
        2.58,
        10.5,
        0.55,
        23,
        "D9E5F2",
    )
    add_text(
        slide,
        "Funcional · lógica simulada · POO · Pandas y NumPy",
        0.84,
        3.42,
        11.3,
        0.42,
        16,
        "A8F0E7",
        True,
    )
    add_panel(slide, 0.82, 4.55, 7.4, 1.15, "1D344A")
    add_text(
        slide,
        "Curso: Lenguajes de Programación — 100000SI68\n"
        "Integrantes: [Completar]   ·   Docente: [Completar]",
        1.08,
        4.82,
        6.9,
        0.64,
        14,
        WHITE,
    )
    add_text(slide, "Objetivo: 9:30 · margen: 0:30", 0.84, 6.62, 5.2,
             0.3, 12, "D9E5F2")

    # 2. Problema y diseño (1 min 10 s)
    slide = new_slide(prs, 2, "Problema y diseño",
                      "Un catálogo que también ayuda a decidir qué leer",
                      "1:10")
    add_panel(slide, 0.72, 1.42, 4.1, 5.15)
    add_text(slide, "Necesidad", 1.02, 1.78, 3.45, 0.38, 19, NAVY, True)
    add_text(
        slide,
        "Buscar, mantener y analizar publicaciones, además de recomendar "
        "lecturas según los intereses del lector.",
        1.02,
        2.34,
        3.45,
        1.55,
        17,
    )
    add_text(slide, "Solución", 1.02, 4.25, 3.45, 0.38, 19, NAVY, True)
    add_text(
        slide,
        "Módulos separados para modelos, procesamiento funcional, "
        "recomendación, API e indicadores.",
        1.02,
        4.82,
        3.45,
        1.2,
        16,
    )
    add_panel(slide, 5.05, 1.42, 7.58, 5.15, WHITE)
    add_diagram(slide, "arquitectura_general.png", 5.2, 1.62, 7.28, 4.75)
    add_text(slide, "Interfaz → API → lógica y modelos → análisis",
             5.25, 6.34, 7.2, 0.24, 11, MUTED, align=PP_ALIGN.CENTER)

    # 3. Aplicación (1 min)
    slide = new_slide(prs, 3, "Demostración", "Así se ve la búsqueda en la aplicación",
                      "1:00")
    add_panel(slide, 0.68, 1.4, 8.45, 5.2, WHITE)
    add_capture(slide, "busqueda_resultados.png", 0.82, 1.54, 8.17, 4.92)
    add_panel(slide, 9.42, 1.4, 3.2, 5.2, PALE_BLUE)
    add_text(slide, "Flujo breve", 9.7, 1.78, 2.65, 0.4, 17, NAVY, True)
    add_bullets(slide, [
        "Buscar un título o autor",
        "Revisar resultados",
        "Usar catálogo local como respaldo",
    ], 9.7, 2.4, 2.6, 14, 0.83)
    add_text(slide, "Captura real de la app.", 9.7, 5.8, 2.6, 0.3, 10,
             MUTED)

    # 4. Programación funcional (1 min 30 s)
    add_code_slide(
        prs,
        4,
        "Programación funcional",
        "El pipeline filter → map → reduce",
        "1:30",
        "codigo_motor_funcional_101_129.png",
        "Filtra el catálogo, transforma los datos para estimar horas y reduce "
        "resultados para obtener totales. El catálogo original no se modifica.",
        "motor_funcional.py:101–129",
    )

    # 5. Programación lógica simulada (1 min 30 s)
    add_code_slide(
        prs,
        5,
        "Programación lógica",
        "Recomendaciones e inferencia",
        "1:30",
        "codigo_motor_logico_229_256.png",
        "La base de conocimiento aporta hechos; el motor explora candidatos, "
        "ordena soluciones y puede aplicar un corte. Es una simulación en "
        "Python, como permite la indicación del curso.",
        "motor_logico.py:229–256",
    )

    # 6. POO (1 min)
    add_code_slide(
        prs,
        6,
        "POO",
        "Herencia para publicaciones físicas y digitales",
        "1:00",
        "codigo_modelos_103_121.png",
        "LibroFisico especializa la clase base: hereda atributos comunes y "
        "añade los propios. Ebook sigue el mismo principio.",
        "modelos.py:103–121",
    )

    # 7. CRUD/API (1 min)
    add_code_slide(
        prs,
        7,
        "CRUD y API",
        "Las rutas conectan las solicitudes con el dominio",
        "1:00",
        "codigo_routes_101_129.png",
        "POST, PUT y DELETE gestionan cambios; GET permite consultar. "
        "FastAPI valida solicitudes y el repositorio conserva cambios "
        "durante la ejecución.",
        "backend/api/routes.py:101–129",
    )

    # 8. Ciencia de datos y comprobación (1 min)
    slide = new_slide(prs, 8, "Ciencia de datos y pruebas",
                      "Indicadores calculados desde un CSV",
                      "1:00")
    add_panel(slide, 0.68, 1.42, 8.45, 5.15, DARK)
    add_capture(slide, "codigo_analisis_datos_27_43.png",
                0.84, 1.58, 8.13, 4.8)
    add_panel(slide, 9.42, 1.42, 3.2, 5.15, PALE_BLUE)
    add_text(slide, "Qué se calcula", 9.7, 1.78, 2.65, 0.4, 17, NAVY, True)
    add_bullets(slide, [
        "Promedio y mediana",
        "Páginas totales",
        "Horas estimadas",
        "Pruebas: 6 aprobadas",
    ], 9.7, 2.4, 2.6, 14, 0.75)
    add_text(slide, "Pandas organiza; NumPy opera sobre arreglos.",
             9.7, 5.75, 2.6, 0.5, 11, MUTED)

    # 9. Cierre y preguntas (1 min)
    slide = new_slide(prs, 9, "Cierre y defensa",
                      "Un proyecto, varios paradigmas",
                      "1:00")
    cards = [
        ("FUNCIONAL", "Transformar colecciones"),
        ("LÓGICA", "Inferir recomendaciones"),
        ("POO / DATOS", "Modelar y medir"),
    ]
    for index, (heading, detail) in enumerate(cards):
        x = 0.82 + index * 4.18
        add_panel(slide, x, 1.72, 3.75, 1.6, WHITE)
        add_text(slide, heading, x + 0.22, 2.0, 3.3, 0.3, 13, TEAL, True)
        add_text(slide, detail, x + 0.22, 2.48, 3.3, 0.42, 17, NAVY, True)
    add_panel(slide, 0.82, 3.85, 11.7, 1.45, NAVY)
    add_text(slide, "¿Preguntas?", 1.15, 4.27, 11.0, 0.5, 26, WHITE, True,
             PP_ALIGN.CENTER)
    add_text(slide, "Guarda el último minuto para preguntas y defensa.",
             1.0, 5.8, 11.3, 0.35, 14, MUTED, align=PP_ALIGN.CENTER)

    DELIVERABLES.mkdir(parents=True, exist_ok=True)
    prs.save(OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    print(build_presentation())
