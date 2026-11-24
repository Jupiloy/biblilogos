"""Crea capturas legibles de fragmentos reales del código fuente."""

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.formatters.img import ImageFormatter
from pygments.lexers import PythonLexer


RAIZ = Path(__file__).resolve().parents[1]
CAPTURAS = RAIZ / "entregables" / "capturas"
FUENTE_NORMAL = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FUENTE_NEGRITA = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

FRAGMENTOS = [
    ("motor_funcional.py", 101, 129, "Pipeline funcional: filter, map y reduce"),
    ("motor_logico.py", 229, 256, "Inferencia, orden y corte lógico"),
    ("modelos.py", 103, 121, "Herencia y especialización de LibroFisico"),
    ("backend/api/routes.py", 101, 129, "Operaciones CRUD de la API"),
    ("analisis_datos.py", 27, 43, "Indicadores con Pandas y NumPy"),
]


def fuente(ruta, size):
    return ImageFont.truetype(ruta, size)


def crear_captura(archivo, inicio, fin, titulo):
    ruta_fuente = RAIZ / archivo
    lineas = ruta_fuente.read_text(encoding="utf-8").splitlines()
    codigo = "\n".join(lineas[inicio - 1:fin]) + "\n"
    formatter = ImageFormatter(
        style="monokai",
        font_name="DejaVu Sans Mono",
        font_size=18,
        line_numbers=True,
        line_number_start=inicio,
        line_number_fg="#8b949e",
        line_number_bg="#202938",
        line_number_separator=True,
        line_number_pad=16,
        image_pad=20,
        line_pad=7,
        image_bg="#151b26",
    )
    buffer = BytesIO()
    formatter.format(PythonLexer().get_tokens(codigo), buffer)
    codigo_imagen = Image.open(buffer).convert("RGB")

    cabecera = 68
    pie = 48
    lienzo = Image.new(
        "RGB",
        (codigo_imagen.width, codigo_imagen.height + cabecera + pie),
        "#151b26",
    )
    dibujo = ImageDraw.Draw(lienzo)
    dibujo.rectangle((0, 0, lienzo.width, cabecera), fill="#202938")
    dibujo.ellipse((20, 25, 34, 39), fill="#ff6b6b")
    dibujo.ellipse((44, 25, 58, 39), fill="#ffd166")
    dibujo.ellipse((68, 25, 82, 39), fill="#06d6a0")
    dibujo.text(
        (110, 17),
        f"{archivo}  ·  líneas {inicio}–{fin}",
        font=fuente(FUENTE_NEGRITA, 20),
        fill="#e6edf3",
    )
    lienzo.paste(codigo_imagen, (0, cabecera))
    dibujo.rectangle(
        (0, lienzo.height - pie, lienzo.width, lienzo.height),
        fill="#202938",
    )
    dibujo.text(
        (20, lienzo.height - 34),
        titulo,
        font=fuente(FUENTE_NORMAL, 16),
        fill="#9fb3c8",
    )
    destino = CAPTURAS / f"codigo_{ruta_fuente.stem}_{inicio}_{fin}.png"
    lienzo.save(destino)
    return destino


def main():
    CAPTURAS.mkdir(parents=True, exist_ok=True)
    for archivo, inicio, fin, titulo in FRAGMENTOS:
        print(crear_captura(archivo, inicio, fin, titulo))


if __name__ == "__main__":
    main()
