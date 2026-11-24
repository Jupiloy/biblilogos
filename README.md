# BiblioLogos — Sistema Gestor y Recomendador Inteligente de Libros

Proyecto final para el curso **Lenguajes de Programación (100000SI68)** desarrollado 100% en **Python 3** utilizando únicamente la **biblioteca estándar** (sin `pip install` ni dependencias externas).

## Estructura del Proyecto (VS Code)

```text
sistema_libros_multiparadigma/
├── modelos.py            # Unidad 3: POO, herencia, cadenas + Fábrica + Repositorio Singleton
├── motor_funcional.py    # Unidad 1: Funciones puras, lambda, filter, map, reduce, FOS, pipeline
├── motor_logico.py       # Unidad 2: Base de conocimiento, unificar, [Cabeza|Cola], Estrategia, corte !
├── main.py               # Unidad 3: Tuplas, listas, dicts, statistics/random/datetime/math + consola
├── interfaz_grafica.py   # Interfaz Gráfica nativa (GUI) usando tkinter (biblioteca estándar)
└── README.md             # Guía rápida de ejecución
```

## Cómo ejecutar en VS Code

1. Abre la carpeta `sistema_libros_multiparadigma` en **Visual Studio Code**.
2. Abre una terminal integrada (`Ctrl + ñ` o `Terminal > Nuevo terminal`).
3. Para iniciar el **menú interactivo en consola**:
   ```bash
   python main.py
   ```
4. Para iniciar la **interfaz gráfica de escritorio (GUI Tkinter)**:
   ```bash
   python interfaz_grafica.py
   ```

## Interfaz web Angular + API FastAPI

La nueva interfaz web utiliza Angular 20 para el frontend y FastAPI para el backend.

1. Instala las dependencias de Python:
   ```bash
   uv venv .venv
   uv pip install --python .venv/bin/python fastapi uvicorn
   ```

2. Inicia la API:
   ```bash
   uv run --python .venv/bin/python uvicorn backend.main:app --reload --port 8000
   ```

3. En otra terminal, inicia Angular:
   ```bash
   cd frontend
   npm install
   npm start
   ```

Abre `http://localhost:4200`. La API estará disponible en `http://localhost:8000/api`.

## Catálogo abierto

Las búsquedas también consultan Open Library en tiempo real. Los resultados se guardan
localmente en `data/bibliologos.db` y se reutilizan como caché. Si Open Library no está
disponible, el sistema utiliza el catálogo local de ocho publicaciones como respaldo.

> Nota: En algunos sistemas Linux/macOS utiliza `python3` en lugar de `python`.

## Pruebas y análisis de datos

Instala las dependencias:

```bash
./.venv/bin/python -m pip install -r requirements.txt
```

Ejecuta las pruebas Python:

```bash
./.venv/bin/python -m unittest discover -s tests -v
```

Genera los reportes NumPy/Pandas:

```bash
./.venv/bin/python - <<'PY'
from analisis_datos import cargar_catalogo, exportar_reportes
df = cargar_catalogo("tests/fixtures/catalogo_pruebas.csv")
print(exportar_reportes(df, "entregables/reportes"))
PY
```

## Entregables académicos

Los archivos finales se encuentran en `entregables/`:

- `Informe_Tecnico_BiblioLogos.docx`: informe editable en Word.
- `pdf/Informe_Tecnico_BiblioLogos.pdf`: informe exportado a PDF.
- `EVIDENCIAS.md`: guía de evidencias y comandos.
- `reportes/`: reportes CSV generados con Pandas y NumPy.

Para regenerar el informe:

```bash
./.venv/bin/python scripts/generar_diagramas.py
./.venv/bin/python scripts/generar_informe.py
libreoffice --headless --convert-to pdf --outdir entregables/pdf entregables/Informe_Tecnico_BiblioLogos.docx
```
