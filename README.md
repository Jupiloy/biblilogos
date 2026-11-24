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

2. Crea la cuenta administradora inicial (el comando solicita la contraseña sin mostrarla):
   ```bash
   ./.venv/bin/python -m backend.create_admin
   ```

3. Inicia la API:
   ```bash
   uv run --python .venv/bin/python uvicorn backend.main:app --reload --port 8000
   ```

4. En otra terminal, inicia Angular:
   ```bash
   cd frontend
   npm install
   npm start
   ```

Abre `http://localhost:4200`. La API estará disponible en `http://localhost:8000/api`.
Los lectores pueden crear su propia cuenta desde la pantalla de acceso. El rol
administrador se crea localmente y es el único que puede crear, editar o eliminar
publicaciones. Los lectores pueden buscar, consultar y recibir recomendaciones.
Las contraseñas se almacenan con PBKDF2 y las sesiones expiran después de ocho horas.
Las cuentas y sesiones se guardan en `data/usuarios.db`.

## Catálogo abierto

Las búsquedas también consultan Open Library en tiempo real. Los resultados se guardan
localmente en `data/bibliologos.db` y se reutilizan como caché. El catálogo administrable
se guarda por separado en `data/catalogo.db`: desde la opción **Mi catálogo** en la
interfaz web se pueden registrar, actualizar y eliminar publicaciones locales, que
permanecen después de reiniciar el backend. Si Open Library no está disponible, la
búsqueda utiliza ese catálogo local como respaldo.

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

Genera indicadores y reportes NumPy/Pandas a partir del catálogo actual de
`data/catalogo.db`:

```bash
./.venv/bin/python -m analisis_datos
```

El análisis abre SQLite en modo de solo lectura y vuelve a consultar sus datos
cada vez que se ejecuta. Los reportes se escriben en `entregables/reportes/`.
`tests/fixtures/catalogo_pruebas.csv` se conserva como conjunto fijo y pequeño
para que las pruebas automatizadas sean reproducibles.

## Entregables académicos

El mapa de archivos y sus funciones está en [`GUIA_DE_ARCHIVOS.md`](./GUIA_DE_ARCHIVOS.md).

Los archivos finales se encuentran en `entregables/`:

- `Informe_Tecnico_BiblioLogos.docx`: informe editable en Word.
- `pdf/Informe_Tecnico_BiblioLogos.pdf`: informe exportado a PDF.
- `Presentacion_BiblioLogos.pptx`: presentación explicativa de 15 diapositivas, preparada para 9:30 minutos e incluye capturas de la interfaz, el código y diagramas.
- `EVIDENCIAS.md`: guía de evidencias y comandos.
- `reportes/`: reportes CSV generados con Pandas y NumPy.

Para regenerar el informe:

```bash
./.venv/bin/python scripts/generar_diagramas.py
./.venv/bin/python scripts/generar_informe.py
./.venv/bin/python scripts/generar_presentacion.py
libreoffice --headless --convert-to pdf --outdir entregables/pdf entregables/Informe_Tecnico_BiblioLogos.docx
```
