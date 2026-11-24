"""Genera una presentación breve alineada con la rúbrica del proyecto."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "entregables"
DIAGRAMAS = SALIDA / "diagramas"
RUTA_PRESENTACION = SALIDA / "Presentacion_BiblioLogos.pptx"

ANCHO = 13.333
ALTO = 7.5
FONDO = "F4F7FB"
AZUL = "132238"
AZUL_CLARO = "DDE9F5"
TURQUESA = "0D9488"
TEXTO = "172536"
GRIS = "5B6B7E"
BLANCO = "FFFFFF"
CODIGO = "101827"
VERDE = "DCFCE7"
AMARILLO = "FEF3C7"


def color(hexadecimal):
    return RGBColor.from_string(hexadecimal)


def agregar_texto(
    slide,
    texto,
    x,
    y,
    ancho,
    alto,
    tamano=18,
    color_texto=TEXTO,
    negrita=False,
    fuente="Aptos",
    alineacion=PP_ALIGN.LEFT,
    ancla=MSO_ANCHOR.TOP,
):
    caja = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(ancho), Inches(alto)
    )
    marco = caja.text_frame
    marco.clear()
    marco.word_wrap = True
    marco.margin_left = Inches(0.08)
    marco.margin_right = Inches(0.08)
    marco.margin_top = Inches(0.04)
    marco.margin_bottom = Inches(0.04)
    marco.vertical_anchor = ancla
    parrafo = marco.paragraphs[0]
    parrafo.alignment = alineacion
    parrafo.text = texto
    for run in parrafo.runs:
        run.font.name = fuente
        run.font.size = Pt(tamano)
        run.font.bold = negrita
        run.font.color.rgb = color(color_texto)
    return caja


def agregar_forma(slide, tipo, x, y, ancho, alto, relleno, linea=None):
    forma = slide.shapes.add_shape(
        tipo, Inches(x), Inches(y), Inches(ancho), Inches(alto)
    )
    forma.fill.solid()
    forma.fill.fore_color.rgb = color(relleno)
    forma.line.color.rgb = color(linea or relleno)
    return forma


def agregar_lista(slide, items, x, y, ancho, alto, tamano=17, color_texto=TEXTO):
    caja = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(ancho), Inches(alto)
    )
    marco = caja.text_frame
    marco.clear()
    marco.word_wrap = True
    marco.margin_left = Inches(0.05)
    marco.margin_right = Inches(0.04)
    for indice, item in enumerate(items):
        parrafo = marco.paragraphs[0] if indice == 0 else marco.add_paragraph()
        parrafo.text = item
        parrafo.level = 0
        parrafo.font.name = "Aptos"
        parrafo.font.size = Pt(tamano)
        parrafo.font.color.rgb = color(color_texto)
        parrafo.space_after = Pt(11)
        parrafo._p.get_or_add_pPr().insert(0, _crear_bullet())
    return caja


def _crear_bullet():
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import nsdecls

    return parse_xml(f'<a:buChar char="•" {nsdecls("a")}/>')


def agregar_codigo(slide, codigo, x, y, ancho, alto, tamano=15):
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, ancho, alto, CODIGO)
    caja = slide.shapes.add_textbox(
        Inches(x + 0.18), Inches(y + 0.12), Inches(ancho - 0.36), Inches(alto - 0.24)
    )
    marco = caja.text_frame
    marco.clear()
    marco.word_wrap = False
    marco.margin_left = 0
    marco.margin_right = 0
    marco.margin_top = 0
    marco.margin_bottom = 0
    for indice, linea in enumerate(codigo.strip("\n").splitlines()):
        parrafo = marco.paragraphs[0] if indice == 0 else marco.add_paragraph()
        parrafo.text = linea
        parrafo.font.name = "Cascadia Code"
        parrafo.font.size = Pt(tamano)
        parrafo.font.color.rgb = color("D7E2F0")
        parrafo.space_after = Pt(2)
    return caja


def nueva_slide(prs, seccion, titulo, duracion):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color(FONDO)
    agregar_texto(slide, seccion.upper(), 0.55, 0.18, 8.5, 0.28, 10, TURQUESA, True)
    agregar_texto(slide, titulo, 0.55, 0.48, 12.2, 0.55, 27, AZUL, True)
    agregar_forma(slide, MSO_SHAPE.RECTANGLE, 0.55, 1.08, 0.65, 0.05, TURQUESA)
    agregar_texto(
        slide,
        f"BiblioLogos  •  Exposición sugerida: {duracion}",
        0.55,
        7.13,
        10.5,
        0.2,
        9,
        GRIS,
    )
    agregar_texto(slide, f"{len(prs.slides):02d}", 12.15, 7.1, 0.6, 0.25, 10, GRIS, True, alineacion=PP_ALIGN.RIGHT)
    return slide


def agregar_etiqueta(slide, texto, x, y, ancho, relleno=AZUL_CLARO, tono=AZUL):
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, ancho, 0.36, relleno)
    agregar_texto(slide, texto, x + 0.06, y + 0.04, ancho - 0.12, 0.24, 10, tono, True, alineacion=PP_ALIGN.CENTER)


def agregar_imagen(slide, nombre, x, y, ancho=None, alto=None):
    ruta = DIAGRAMAS / nombre
    if ancho and alto:
        return slide.shapes.add_picture(
            str(ruta), Inches(x), Inches(y), Inches(ancho), Inches(alto)
        )
    if ancho:
        return slide.shapes.add_picture(str(ruta), Inches(x), Inches(y), width=Inches(ancho))
    return slide.shapes.add_picture(str(ruta), Inches(x), Inches(y), height=Inches(alto))


def construir_presentacion():
    prs = Presentation()
    prs.slide_width = Inches(ANCHO)
    prs.slide_height = Inches(ALTO)
    prs.core_properties.title = "BiblioLogos — Exposición del proyecto"
    prs.core_properties.subject = "Programación funcional, lógica y multiparadigma"
    prs.core_properties.author = "Equipo BiblioLogos"

    # 1. Portada
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color(AZUL)
    agregar_forma(slide, MSO_SHAPE.RECTANGLE, 0, 0, 0.22, ALTO, TURQUESA)
    agregar_etiqueta(slide, "PROYECTO INTEGRADOR", 0.8, 0.78, 2.45, "1D344A", "A8F0E7")
    agregar_texto(slide, "BIBLIOLOGOS", 0.8, 1.55, 9.2, 0.8, 38, BLANCO, True)
    agregar_texto(
        slide,
        "Sistema gestor y recomendador inteligente de libros",
        0.82,
        2.42,
        9.6,
        0.68,
        23,
        "D9E5F2",
    )
    agregar_texto(
        slide,
        "Programación funcional · lógica simulada · POO · ciencia de datos",
        0.82,
        3.35,
        10.8,
        0.45,
        16,
        "A8F0E7",
        True,
    )
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 0.82, 4.42, 6.3, 1.25, "1D344A")
    agregar_texto(
        slide,
        "Curso: Lenguajes de Programación — 100000SI68\n"
        "Integrantes: [Completar nombres]   |   Docente: [Completar]",
        1.02,
        4.68,
        5.9,
        0.72,
        14,
        BLANCO,
    )
    agregar_texto(slide, "Exposición — 24 minutos", 0.82, 6.62, 4.8, 0.3, 12, "D9E5F2")

    # 2. Problema y objetivos
    slide = nueva_slide(prs, "1 · Análisis", "¿Qué problema resolvemos?", "3 min")
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 0.65, 1.4, 5.85, 4.95, BLANCO)
    agregar_texto(slide, "Necesidad", 0.9, 1.68, 4.8, 0.35, 18, AZUL, True)
    agregar_texto(
        slide,
        "Organizar un catálogo bibliográfico, encontrar publicaciones y derivar recomendaciones "
        "sin depender de búsquedas y cálculos manuales.",
        0.9,
        2.14,
        5.1,
        1.16,
        18,
    )
    agregar_texto(slide, "Propuesta", 0.9, 3.55, 4.8, 0.35, 18, AZUL, True)
    agregar_texto(
        slide,
        "BiblioLogos integra catálogo, lectores, reglas de recomendación, CRUD y reportes en una "
        "aplicación con consola, escritorio y web.",
        0.9,
        4.0,
        5.1,
        1.3,
        17,
    )
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 6.8, 1.4, 5.85, 4.95, "E8F2F7")
    agregar_texto(slide, "Lo que exige el curso", 7.1, 1.68, 5.2, 0.35, 18, AZUL, True)
    agregar_lista(
        slide,
        [
            "Funciones, lambdas y funciones de orden superior",
            "Hechos, reglas, unificación y resolución lógica",
            "Estructuras, clases, objetos y herencia",
            "NumPy, Pandas, pruebas y resultados",
        ],
        7.1,
        2.18,
        5.1,
        3.6,
        16,
    )
    agregar_texto(
        slide,
        "La exposición y defensa vale 2 puntos; la demostración también evidencia los criterios técnicos.",
        7.1,
        5.72,
        5.1,
        0.45,
        12,
        GRIS,
    )

    # 3. Arquitectura
    slide = nueva_slide(prs, "2 · Diseño", "Una solución separada por responsabilidades", "3 min")
    agregar_imagen(slide, "arquitectura_general.png", 0.78, 1.42, ancho=11.8)
    agregar_texto(
        slide,
        "Código para citar: main.py · backend/ · motor_funcional.py · motor_logico.py · modelos.py · analisis_datos.py",
        0.82,
        6.28,
        11.6,
        0.38,
        12,
        GRIS,
    )

    # 4. Funcional
    slide = nueva_slide(prs, "3 · Programación funcional", "Filtrar, transformar y acumular", "≈2.5 min dentro del bloque funcional + lógico")
    agregar_codigo(
        slide,
        """# motor_funcional.py
return list(filter(
    lambda libro: libro.calificacion >= umbral,
    catalogo
))

return reduce(
    lambda total, libro: total + libro.paginas,
    catalogo, 0
)""",
        0.7,
        1.48,
        7.1,
        3.75,
        16,
    )
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 8.15, 1.48, 4.5, 3.75, BLANCO)
    agregar_texto(slide, "Temas de clase que se ven aquí", 8.45, 1.78, 3.95, 0.4, 17, AZUL, True)
    agregar_lista(
        slide,
        [
            "lambda: función anónima",
            "filter: selección por condición",
            "reduce: acumulación de páginas",
            "Nueva lista: evita alterar la entrada",
            "FOS: recibe una transformación",
        ],
        8.45,
        2.32,
        3.9,
        2.5,
        15,
    )
    agregar_imagen(slide, "flujo_funcional.png", 1.05, 5.38, ancho=7.6, alto=1.28)
    agregar_etiqueta(slide, "Referencia: motor_funcional.py:21, 61, 73, 101", 8.4, 5.72, 4.15)

    # 5. Lógica
    slide = nueva_slide(prs, "3 · Programación lógica", "Hechos → reglas → recomendaciones", "≈2.5 min dentro del bloque funcional + lógico")
    agregar_imagen(slide, "flujo_logico.png", 0.68, 1.45, ancho=6.1, alto=4.7)
    agregar_codigo(
        slide,
        """# motor_logico.py (idea central)
for isbn in libros_leidos:
    autor = base.es_autor(isbn)
    genero = base.es_genero(isbn)

for libro in catalogo:
    if existe_en_lista(libro.isbn, leidos):
        continue
    motivos, bono = estrategia.evaluar_candidato(...)
    if motivos:
        soluciones.append(...)

if corte and soluciones:
    return [soluciones[0]]""",
        6.95,
        1.48,
        5.72,
        3.9,
        12,
    )
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 6.95, 5.58, 5.72, 0.78, AMARILLO)
    agregar_texto(
        slide,
        "Precisión: es una simulación en Python. El backtracking recorre candidatos; el corte retorna una solución ya ordenada.",
        7.14,
        5.72,
        5.34,
        0.48,
        11,
        TEXTO,
        True,
    )
    agregar_texto(
        slide,
        "Referencias: motor_logico.py:19, 64, 103, 202",
        0.8,
        6.4,
        5.8,
        0.28,
        11,
        GRIS,
    )

    # 6. POO y tipos
    slide = nueva_slide(prs, "4 · Multiparadigma y POO", "Clases, herencia y colecciones", "≈3 min dentro del bloque multiparadigma + CRUD")
    agregar_imagen(slide, "diagrama_clases.png", 0.62, 1.48, ancho=7.2, alto=4.95)
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 8.05, 1.48, 4.6, 4.95, BLANCO)
    agregar_texto(slide, "Ejemplo de herencia", 8.35, 1.8, 4.0, 0.35, 17, AZUL, True)
    agregar_codigo(
        slide,
        """class LibroFisico(Publicacion):
    def mostrar_info(self):
        base = super().mostrar_info()
        return f'{base} | Stock: {self.stock}'""",
        8.3,
        2.28,
        4.1,
        1.62,
        12,
    )
    agregar_lista(
        slide,
        [
            "Lista: catálogo y lecturas",
            "Tupla: ficha inmutable",
            "Diccionario: índice por ISBN",
            "Fábrica y repositorio",
        ],
        8.35,
        4.18,
        3.9,
        1.8,
        14,
    )
    agregar_texto(slide, "Referencia: modelos.py:65, 103, 123, 178, 214", 0.8, 6.55, 7.4, 0.28, 11, GRIS)

    # 7. CRUD
    slide = nueva_slide(prs, "4 · CRUD", "El catálogo también se puede mantener", "≈2 min dentro del bloque multiparadigma + CRUD")
    agregar_imagen(slide, "flujo_crud.png", 0.65, 1.5, ancho=5.1, alto=3.45)
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 6.0, 1.5, 6.65, 3.45, BLANCO)
    agregar_texto(slide, "Operaciones disponibles en la API", 6.3, 1.78, 5.95, 0.35, 18, AZUL, True)
    agregar_lista(
        slide,
        [
            "POST /api/publicaciones — crear",
            "GET /api/publicaciones — buscar/listar",
            "PUT /api/publicaciones/{isbn} — actualizar",
            "DELETE /api/publicaciones/{isbn} — eliminar",
        ],
        6.35,
        2.3,
        5.9,
        2.35,
        16,
    )
    agregar_codigo(
        slide,
        """@router.put("/publicaciones/{isbn}")
def actualizar_publicacion(isbn, solicitud):
    publicacion = servicio_catalogo.actualizar_publicacion(
        isbn, solicitud.model_dump(exclude_unset=True)
    )""",
        0.75,
        5.2,
        7.4,
        1.25,
        11,
    )
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 8.45, 5.2, 4.2, 1.25, "E8F2F7")
    agregar_texto(
        slide,
        "La API valida entradas; el repositorio actualiza en memoria durante la ejecución.",
        8.7,
        5.43,
        3.7,
        0.76,
        13,
        TEXTO,
    )
    agregar_texto(slide, "Referencia: backend/api/routes.py:101–128 · modelos.py:253–299", 0.8, 6.62, 10.2, 0.25, 10, GRIS)

    # 8. Ciencia de datos
    slide = nueva_slide(prs, "5 · Ciencia de datos", "Pandas organiza; NumPy calcula", "≈1.5 min dentro del bloque de ciencia de datos + pruebas")
    agregar_codigo(
        slide,
        """# analisis_datos.py
df = pd.read_csv(ruta_csv)
calificaciones = df["calificacion"].to_numpy(dtype=float)
paginas = df["paginas"].to_numpy(dtype=np.int64)

promedio = np.mean(calificaciones)
mediana = np.median(calificaciones)
total = np.sum(paginas)
horas = np.ceil(total / 40.0)""",
        0.7,
        1.5,
        6.5,
        3.65,
        14,
    )
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 7.55, 1.5, 5.05, 3.65, BLANCO)
    agregar_texto(slide, "Resultado sobre CSV de prueba (3 libros)", 7.85, 1.82, 4.45, 0.5, 17, AZUL, True)
    indicadores = [
        ("Publicaciones", "3"),
        ("Promedio", "4.77 / 5"),
        ("Páginas", "1,010"),
        ("Horas estimadas", "26"),
    ]
    for indice, (nombre, valor) in enumerate(indicadores):
        fila, columna = divmod(indice, 2)
        x = 7.85 + columna * 2.2
        y = 2.62 + fila * 1.12
        agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, 2.0, 0.88, AZUL_CLARO)
        agregar_texto(slide, nombre, x + 0.12, y + 0.1, 1.75, 0.25, 10, GRIS, True)
        agregar_texto(slide, valor, x + 0.12, y + 0.4, 1.75, 0.3, 17, AZUL, True)
    agregar_imagen(slide, "flujo_datos.png", 0.95, 5.37, ancho=7.2, alto=1.25)
    agregar_texto(slide, "Son indicadores del conjunto de prueba, no del catálogo completo.", 8.0, 5.68, 4.4, 0.5, 12, GRIS, True)
    agregar_texto(slide, "Referencia: analisis_datos.py:9, 27, 44 · tests/fixtures/catalogo_pruebas.csv", 0.8, 6.68, 11.5, 0.25, 10, GRIS)

    # 9. Pruebas y resultados
    slide = nueva_slide(prs, "5 · Evidencia", "¿Cómo comprobamos que funciona?", "≈1.5 min dentro del bloque de ciencia de datos + pruebas")
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 0.7, 1.52, 5.85, 4.85, BLANCO)
    agregar_texto(slide, "Pruebas Python: 6 aprobadas", 1.0, 1.84, 5.1, 0.4, 20, AZUL, True)
    agregar_lista(
        slide,
        [
            "CRUD y rechazo de ISBN duplicado",
            "Pipeline y filtros funcionales",
            "Unificación y recursividad",
            "Inferencia de recomendaciones",
            "Carga CSV e indicadores",
        ],
        1.02,
        2.48,
        4.95,
        3.1,
        15,
    )
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 6.85, 1.52, 5.78, 4.85, VERDE)
    agregar_texto(slide, "También verificado", 7.15, 1.84, 4.9, 0.4, 20, AZUL, True)
    agregar_lista(
        slide,
        [
            "Frontend Angular: 2 pruebas aprobadas",
            "Build Angular: completado",
            "API: health y POST/PUT/DELETE probados",
            "Compilación de módulos Python: correcta",
        ],
        7.16,
        2.5,
        4.85,
        2.9,
        15,
    )
    agregar_codigo(
        slide,
        "./.venv/bin/python -m unittest discover -s tests -v",
        1.0,
        5.7,
        5.15,
        0.48,
        10,
    )

    # 10. Cierre y preguntas
    slide = nueva_slide(prs, "6 · Defensa", "Tres paradigmas, un sistema", "5 min de preguntas")
    tarjetas = [
        ("FUNCIONAL", "Transformar datos\nsin alterar el catálogo", "filter · map · reduce"),
        ("LÓGICA", "Representar relaciones\ny derivar recomendaciones", "hechos · reglas · unificación"),
        ("POO / DATOS", "Modelar el dominio\ny medir el catálogo", "clases · Pandas · NumPy"),
    ]
    for indice, (titulo_tarjeta, detalle, conceptos) in enumerate(tarjetas):
        x = 0.75 + indice * 4.22
        agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.75, 3.8, 2.3, BLANCO)
        agregar_texto(slide, titulo_tarjeta, x + 0.22, 2.02, 3.35, 0.32, 14, TURQUESA, True)
        agregar_texto(slide, detalle, x + 0.22, 2.52, 3.3, 0.72, 18, AZUL, True)
        agregar_texto(slide, conceptos, x + 0.22, 3.45, 3.3, 0.3, 11, GRIS)
    agregar_forma(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 0.75, 4.52, 11.98, 1.35, AZUL)
    agregar_texto(
        slide,
        "¿Qué parte del sistema quisieran que expliquemos con más detalle?",
        1.1,
        4.92,
        11.3,
        0.5,
        24,
        BLANCO,
        True,
        alineacion=PP_ALIGN.CENTER,
    )
    agregar_texto(
        slide,
        "Cierre: elegimos Python porque permite demostrar los tres enfoques en módulos separados; "
        "la parte lógica es una simulación aceptada por las indicaciones del curso.",
        1.1,
        6.12,
        11.1,
        0.48,
        13,
        GRIS,
        alineacion=PP_ALIGN.CENTER,
    )

    SALIDA.mkdir(parents=True, exist_ok=True)
    prs.save(RUTA_PRESENTACION)
    return RUTA_PRESENTACION


if __name__ == "__main__":
    print(construir_presentacion())
