"""Genera diagramas PNG y fuentes editables compatibles con diagrams.net/draw.io."""

import html
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape


RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "entregables" / "diagramas"


def render_dot(nombre, contenido):
    SALIDA.mkdir(parents=True, exist_ok=True)
    ruta_dot = SALIDA / f"{nombre}.dot"
    ruta_png = SALIDA / f"{nombre}.png"
    ruta_svg = SALIDA / f"{nombre}.svg"
    ruta_dot.write_text(contenido, encoding="utf-8")
    subprocess.run(["dot", "-Tpng", str(ruta_dot), "-o", str(ruta_png)], check=True)
    subprocess.run(["dot", "-Tsvg", str(ruta_dot), "-o", str(ruta_svg)], check=True)


def crear_drawio(nombre, titulo, nodos, conexiones):
    """Crea un archivo .drawio sencillo y editable."""
    partes = []
    ancho = 120
    alto = 50
    id_por_nombre = {}

    for index, (texto, x, y) in enumerate(nodos):
        id_nodo = f"n{index}"
        id_por_nombre[texto] = id_nodo
        estilo = (
            "rounded=1;whiteSpace=wrap;html=1;fillColor=#DAE8FC;"
            "strokeColor=#6C8EBF;fontSize=12;"
        )
        partes.append(
            f'<mxCell id="{id_nodo}" value="{escape(texto)}" style="{estilo}" '
            f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" '
            f'width="{ancho}" height="{alto}" as="geometry"/></mxCell>'
        )

    for origen, destino in conexiones:
        if origen not in id_por_nombre or destino not in id_por_nombre:
            continue
        id_arista = f"e{len(partes)}"
        partes.append(
            f'<mxCell id="{id_arista}" style="edgeStyle=orthogonalEdgeStyle;" '
            f'edge="1" parent="1" source="{id_por_nombre[origen]}" '
            f'target="{id_por_nombre[destino]}"><mxGeometry relative="1" '
            'as="geometry"/></mxCell>'
        )

    contenido = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<mxfile host="app.diagrams.net">'
        f'<diagram name="{html.escape(titulo)}">'
        '<mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" '
        'guides="1" tooltips="1" connect="1" arrows="1" '
        'fold="1" page="1" pageScale="1" pageWidth="1169" '
        'pageHeight="827" math="0" shadow="0">'
        '<root><mxCell id="0"/><mxCell id="1" parent="0"/>'
        + "".join(partes)
        + "</root></mxGraphModel></diagram></mxfile>"
    )
    (SALIDA / f"{nombre}.drawio").write_text(contenido, encoding="utf-8")


def main():
    arquitectura = """
digraph G {
  rankdir=LR; graph [bgcolor="white"]; node [shape=box, style="rounded,filled", fillcolor="#DAE8FC", fontname="Arial"];
  Usuario [label="Usuario"];
  Consola [label="main.py\\nMenú consola"];
  GUI [label="interfaz_grafica.py\\nTkinter"];
  Angular [label="Angular 20\\nInterfaz web"];
  API [label="FastAPI\\nEndpoints REST"];
  Funcional [label="motor_funcional.py"];
  Logico [label="motor_logico.py"];
  POO [label="modelos.py\\nPOO y CRUD"];
  Datos [label="analisis_datos.py\\nPandas + NumPy"];
  CSV [shape=cylinder, label="CSV de prueba"];
  Cache [shape=cylinder, label="SQLite caché"];
  Usuario -> Consola; Usuario -> GUI; Usuario -> Angular;
  Consola -> Funcional; Consola -> Logico; Consola -> POO;
  Angular -> API;
  API -> POO; API -> Logico; API -> Datos;
  Datos -> CSV; API -> Cache;
}
"""
    render_dot("arquitectura_general", arquitectura)

    clases = """
digraph G {
  rankdir=TB; node [shape=record, style=filled, fillcolor="#FFF2CC", fontname="Arial"];
  Publicacion [label="{Publicacion|isbn : str\\ltitulo : str\\lautor : str\\lgenero : str\\npaginas : int\\lcalificacion : float|obtener_ficha_inmutable()\\lmostrar_info()}"];
  LibroFisico [label="{LibroFisico|stock : int\\lubicacion : str|mostrar_info()}"];
  Ebook [label="{Ebook|formato : str\\lpeso_mb : float|mostrar_info()}"];
  Lector [label="{Lector|codigo : str\\lnombre : str\\lcorreo : str\\lcategoria : str\\llibros_leidos : list|registrar_lectura()}"];
  Repositorio [label="{RepositorioBiblioteca|catalogo_por_isbn : dict\\llectores_por_codigo : dict\\lhistorial_prestamos : list|CRUD publicaciones\\lCRUD lectores}"];
  Fabrica [label="{FabricaPublicaciones|crear_publicacion()}"];
  Publicacion -> LibroFisico [arrowhead=empty]; Publicacion -> Ebook [arrowhead=empty];
  Fabrica -> Publicacion [arrowhead=vee, label="crea"];
  Repositorio -> Publicacion [arrowhead=diamond]; Repositorio -> Lector [arrowhead=diamond];
}
"""
    render_dot("diagrama_clases", clases)

    funcional = """
digraph G {
  rankdir=LR; node [shape=box, style="rounded,filled", fillcolor="#D5E8D4", fontname="Arial"];
  Catalogo [label="Catálogo original"];
  Genero [label="filter()\\nfiltrar género"];
  Calificacion [label="filter()\\ncalificación mínima"];
  Map [label="map()\\ncalcular horas"];
  Reduce [label="reduce()\\nsumar páginas"];
  Resultado [shape=folder, label="Diccionario de resultados"];
  Catalogo -> Genero -> Calificacion -> Map -> Reduce -> Resultado;
}
"""
    render_dot("flujo_funcional", funcional)

    logico = """
digraph G {
  rankdir=LR; node [shape=box, style="rounded,filled", fillcolor="#E1D5E7", fontname="Arial"];
  Hechos [shape=cylinder, label="Hechos\\nes_autor / es_genero"];
  Gustos [shape=cylinder, label="le_gusta(lector, libro)"];
  Leidos [label="Excluir libros leídos"];
  Unificar [label="Unificar autor/género"];
  Estrategia [label="Estrategia combinada"];
  Soluciones [label="Backtracking"];
  Corte [shape=diamond, label="¿Corte (!)?"];
  Mejor [label="Primera mejor solución"];
  Todas [label="Todas las soluciones"];
  Hechos -> Gustos -> Leidos -> Unificar -> Estrategia -> Soluciones -> Corte;
  Corte -> Mejor [label="Sí"]; Corte -> Todas [label="No"];
}
"""
    render_dot("flujo_logico", logico)

    crud = """
digraph G {
  rankdir=LR; node [shape=box, style="rounded,filled", fillcolor="#F8CECC", fontname="Arial"];
  Solicitud [label="Solicitud HTTP"];
  Pydantic [label="Validación Pydantic"];
  Servicio [label="ServicioCatalogo"];
  Repositorio [shape=cylinder, label="RepositorioBiblioteca"];
  Respuesta [label="Respuesta JSON"];
  Solicitud -> Pydantic -> Servicio -> Repositorio;
  Repositorio -> Servicio -> Respuesta;
}
"""
    render_dot("flujo_crud", crud)

    datos = """
digraph G {
  rankdir=LR; node [shape=box, style="rounded,filled", fillcolor="#FFE6CC", fontname="Arial"];
  CSV [shape=cylinder, label="catalogo_pruebas.csv"];
  Pandas [label="Pandas\\nread_csv / groupby"];
  Validacion [label="Validación de tipos"];
  NumPy [label="NumPy\\nmean / median / sum / ceil"];
  Reportes [shape=folder, label="CSV de resultados"];
  CSV -> Pandas -> Validacion -> NumPy -> Reportes;
}
"""
    render_dot("flujo_datos", datos)

    crear_drawio(
        "arquitectura_general",
        "Arquitectura general",
        [
            ("Usuario", 20, 180), ("Consola", 220, 40),
            ("Tkinter", 220, 180), ("Angular", 220, 320),
            ("FastAPI", 430, 320), ("POO / CRUD", 640, 40),
            ("Motor funcional", 640, 180), ("Motor lógico", 640, 320),
            ("Pandas + NumPy", 640, 460), ("Reportes CSV", 850, 460),
        ],
        [
            ("Usuario", "Consola"), ("Usuario", "Tkinter"), ("Usuario", "Angular"),
            ("Consola", "POO / CRUD"), ("Consola", "Motor funcional"),
            ("Consola", "Motor lógico"), ("Angular", "FastAPI"),
            ("FastAPI", "POO / CRUD"), ("FastAPI", "Motor lógico"),
            ("FastAPI", "Pandas + NumPy"), ("Pandas + NumPy", "Reportes CSV"),
        ],
    )

    crear_drawio(
        "diagrama_clases",
        "Diagrama de clases",
        [
            ("Publicacion", 400, 40), ("LibroFisico", 220, 180),
            ("Ebook", 580, 180), ("FabricaPublicaciones", 400, 320),
            ("RepositorioBiblioteca", 400, 460), ("Lector", 650, 460),
        ],
        [
            ("LibroFisico", "Publicacion"), ("Ebook", "Publicacion"),
            ("FabricaPublicaciones", "Publicacion"),
            ("RepositorioBiblioteca", "Publicacion"),
            ("RepositorioBiblioteca", "Lector"),
        ],
    )


if __name__ == "__main__":
    main()
    print(SALIDA)
