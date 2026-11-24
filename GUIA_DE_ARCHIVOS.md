# Guía general de archivos de BiblioLogos

Esta guía resume para qué sirve cada archivo propio del proyecto. No enumera
dependencias instaladas (`.venv/`, `node_modules/`) ni cachés temporales. Los
archivos compilados en `frontend/dist/` y la base de caché local se describen
al final porque son resultados generados, no fuentes que normalmente se editan.

## 1. Aplicación Python en la raíz

### Documentación y configuración

| Archivo | Función |
|---|---|
| `README.md` | Presenta el proyecto, cómo ejecutar la consola, la GUI y la aplicación web, además de pruebas y entregables. |
| `requirements.txt` | Declara dependencias Python del backend, análisis de datos e instrumentos para generar entregables. |
| `.gitignore` | Evita subir entornos virtuales, bases locales, cachés y otros archivos de máquina. |

### Módulos Python

| Archivo | Función |
|---|---|
| `main.py` | Punto de entrada de la aplicación de consola. Precarga libros y lectores, muestra el menú y conecta los modelos con los motores funcional y lógico. |
| `modelos.py` | Define las clases del dominio: publicaciones físicas y digitales, lectores, fábrica y repositorio con operaciones CRUD y validaciones. |
| `motor_funcional.py` | Contiene funciones para filtrar, transformar y resumir el catálogo; incluye el pipeline `filter`, `map` y `reduce`. |
| `motor_logico.py` | Simula en Python conceptos de programación lógica: hechos, unificación, recursividad cabeza/cola, estrategias e inferencia de recomendaciones. |
| `analisis_datos.py` | Lee el catálogo persistente SQLite o CSV de prueba, valida datos, calcula indicadores con Pandas/NumPy y exporta reportes. |
| `interfaz_grafica.py` | Interfaz de escritorio Tkinter para consultar y gestionar el catálogo y probar funciones del proyecto. Es una alternativa a la interfaz web. |

## 2. Backend FastAPI

| Archivo | Función |
|---|---|
| `backend/__init__.py` | Marca `backend` como paquete Python. |
| `backend/main.py` | Crea la aplicación FastAPI, configura CORS e incorpora el router de la API. Es el punto de entrada usado por Uvicorn. |
| `backend/api/__init__.py` | Marca `backend.api` como paquete Python. |
| `backend/api/routes.py` | Declara los endpoints HTTP de salud, búsqueda, detalle, CRUD, recomendaciones y estadísticas; coordina esquemas y servicios. |
| `backend/models/__init__.py` | Marca `backend.models` como paquete Python. |
| `backend/models/schemas.py` | Define con Pydantic los formatos de solicitudes y respuestas, además de restricciones como páginas positivas y calificación de 0 a 5. |
| `backend/services/__init__.py` | Marca `backend.services` como paquete Python de servicios. |
| `backend/services/auth_service.py` | Registra usuarios, verifica contraseñas con PBKDF2 y gestiona sesiones bearer con vencimiento en SQLite. |
| `backend/services/catalog_service.py` | Adapta el repositorio de dominio para listar, buscar y ejecutar CRUD desde la API; reutiliza la precarga declarada en `main.py`. |
| `backend/services/open_library_service.py` | Consulta Open Library, convierte sus resultados al formato de la aplicación y mantiene una caché local SQLite; también recomienda títulos externos. |
| `backend/services/recommendation_service.py` | Recomienda publicaciones del catálogo local según coincidencias de autor y género, puntúa resultados y aplica un límite. |
| `backend/create_admin.py` | Crea una cuenta administradora local solicitando la contraseña de forma oculta desde la terminal. |

## 3. Interfaz web Angular

### Configuración y recursos del frontend

| Archivo | Función |
|---|---|
| `frontend/.editorconfig` | Define reglas básicas de formato del editor, como codificación, indentación y saltos de línea. |
| `frontend/.gitignore` | Excluye dependencias, compilaciones, cachés y archivos locales del frontend al usar Git. |
| `frontend/angular.json` | Configura los procesos Angular de compilación, servidor de desarrollo, recursos, estilos y pruebas. |
| `frontend/package.json` | Declara dependencias npm y comandos como `start`, `build` y `test`. |
| `frontend/package-lock.json` | Fija el árbol de versiones npm para instalaciones reproducibles. |
| `frontend/README.md` | Documentación inicial generada por Angular CLI sobre desarrollo, build y pruebas. |
| `frontend/tsconfig.json` | Configuración común de TypeScript y opciones estrictas del compilador Angular. |
| `frontend/tsconfig.app.json` | Configuración TypeScript específica para compilar la aplicación. |
| `frontend/tsconfig.spec.json` | Configuración TypeScript para los archivos de pruebas. |
| `frontend/public/favicon.ico` | Icono del sitio copiado como recurso público durante la compilación. |
| `frontend/.vscode/extensions.json` | Recomienda extensiones de VS Code para el proyecto. |
| `frontend/.vscode/launch.json` | Configuración de depuración de VS Code. |
| `frontend/.vscode/tasks.json` | Tareas de VS Code para ejecutar acciones del proyecto. |

### Arranque y componente principal

| Archivo | Función |
|---|---|
| `frontend/src/index.html` | Página HTML inicial donde Angular monta `<app-root>` y declara metadatos del navegador. |
| `frontend/src/main.ts` | Arranca la aplicación Angular con el componente raíz y su configuración. |
| `frontend/src/styles.css` | Estilos globales mínimos, como el reinicio de márgenes y la tipografía de controles. |
| `frontend/src/app/app.ts` | Componente principal: gestiona búsquedas, vistas, guardados, errores, estadísticas y recomendaciones mediante el servicio. |
| `frontend/src/app/app.html` | Plantilla principal de la interfaz: navegación, búsqueda, resultados, estados vacíos, detalle y recomendaciones. |
| `frontend/src/app/app.css` | Estilos y adaptación responsive del espacio principal, resultados y panel de detalle. |
| `frontend/src/app/app.config.ts` | Registra proveedores globales de Angular, enrutador y cliente HTTP. |
| `frontend/src/app/app.routes.ts` | Declara las rutas Angular; actualmente la lista está vacía porque la interfaz funciona como una vista principal. |
| `frontend/src/app/app.spec.ts` | Pruebas básicas del componente raíz: creación y renderizado del título de bienvenida. |

### Componentes reutilizables

| Archivo | Función |
|---|---|
| `frontend/src/app/components/publication-card/publication-card.ts` | Define las entradas y el evento de selección de una tarjeta bibliográfica. |
| `frontend/src/app/components/publication-card/publication-card.html` | Presenta portada, título, autor, género, calificación y motivo de recomendación. |
| `frontend/src/app/components/publication-card/publication-card.css` | Estilos visuales de las tarjetas de publicaciones. |
| `frontend/src/app/components/search-bar/search-bar.ts` | Conserva el texto de búsqueda y emite la consulta cuando se envía el formulario. |
| `frontend/src/app/components/search-bar/search-bar.html` | Formulario de búsqueda de títulos, autores o temas. |
| `frontend/src/app/components/search-bar/search-bar.css` | Estilos de la barra y el botón de búsqueda. |
| `frontend/src/app/components/sidebar/sidebar.ts` | Controla el estado contraído del menú y emite cambios de navegación. |
| `frontend/src/app/components/sidebar/sidebar.html` | Presenta las opciones Buscar, Explorar y Guardados. |
| `frontend/src/app/components/sidebar/sidebar.css` | Estilos del menú lateral y sus estados. |

### Tipos y comunicación con la API

| Archivo | Función |
|---|---|
| `frontend/src/app/core/models/library.models.ts` | Define interfaces TypeScript para publicaciones, recomendaciones e indicadores. |
| `frontend/src/app/core/services/library.service.ts` | Encapsula las solicitudes HTTP para buscar, recomendar y consultar estadísticas en FastAPI. |
| `frontend/src/app/core/services/auth.service.ts` | Inicia/cierra sesión, registra lectores y mantiene el estado de usuario autenticado. |
| `frontend/src/app/core/interceptors/auth.interceptor.ts` | Adjunta el token bearer a solicitudes de la API usando la sesión de la pestaña. |

## 4. Pruebas y datos de prueba

| Archivo | Función |
|---|---|
| `tests/test_modelos.py` | Prueba el CRUD del repositorio y el rechazo de publicaciones duplicadas. |
| `tests/test_paradigmas.py` | Prueba el pipeline funcional, la unificación, la recursividad y las recomendaciones lógicas simuladas. |
| `tests/test_analisis_datos.py` | Prueba CSV, carga SQLite actualizable, indicadores NumPy/Pandas y creación de reportes. |
| `tests/test_auth_service.py` | Prueba hash de credenciales, sesiones, revocación y validación de roles. |
| `tests/fixtures/catalogo_pruebas.csv` | Catálogo pequeño y controlado usado por las pruebas de análisis. |

## 5. Scripts de generación

| Archivo | Función |
|---|---|
| `scripts/generar_capturas_codigo.py` | Genera capturas resaltadas con números de línea para los fragmentos de código usados en la exposición. |
| `scripts/generar_diagramas.py` | Genera fuentes Graphviz, diagramas PNG/SVG y archivos editables de diagrams.net/draw.io. |
| `scripts/generar_informe.py` | Construye el informe académico en formato DOCX, insertando texto, tablas y diagramas. |
| `scripts/generar_presentacion.py` | Construye el PowerPoint breve; también ejecuta el generador de capturas de código antes de crear las diapositivas. |

## 6. Datos y entregables

### Archivos de datos y reportes

| Archivo | Función |
|---|---|
| `data/bibliologos.db` | Base SQLite local usada como caché de resultados de Open Library. Se genera durante la ejecución y no es una fuente de código. |
| `data/catalogo.db` | Base SQLite persistente del catálogo administrable. Conserva las publicaciones iniciales y las creadas, editadas o eliminadas desde la aplicación. |
| `data/usuarios.db` | Base SQLite de cuentas y sesiones. Guarda hashes de contraseña, no contraseñas en texto plano, y tokens de sesión revocables. |
| `entregables/reportes/indicadores.csv` | Exportación tabular de indicadores generales del catálogo de prueba. |
| `entregables/reportes/publicaciones_por_genero.csv` | Reporte agregado de publicaciones y métricas por género. |

### Evidencias visuales usadas en la presentación

| Archivo | Función |
|---|---|
| `entregables/capturas/busqueda_resultados.png` | Captura de la interfaz web mostrando resultados de búsqueda. |
| `entregables/capturas/codigo_motor_funcional_101_129.png` | Fragmento del pipeline funcional real con números de línea. |
| `entregables/capturas/codigo_motor_logico_229_256.png` | Fragmento de inferencia, orden y corte lógico simulado. |
| `entregables/capturas/codigo_modelos_103_121.png` | Fragmento de la clase `LibroFisico` y su herencia. |
| `entregables/capturas/codigo_routes_101_129.png` | Fragmento de rutas CRUD de FastAPI. |
| `entregables/capturas/codigo_analisis_datos_27_43.png` | Fragmento de cálculo de indicadores con Pandas y NumPy. |

### Diagramas

Para cada diagrama, `.dot` es la fuente Graphviz, `.png` es la imagen rasterizada y
`.svg` es la versión vectorial. Los diagramas de arquitectura y clases también
tienen una versión editable `.drawio`.

- Arquitectura: `entregables/diagramas/arquitectura_general.dot`,
  `arquitectura_general.drawio`, `arquitectura_general.png` y
  `arquitectura_general.svg`.
- Clases: `entregables/diagramas/diagrama_clases.dot`,
  `diagrama_clases.drawio`, `diagrama_clases.png` y `diagrama_clases.svg`.
- CRUD: `entregables/diagramas/flujo_crud.dot`, `flujo_crud.png` y `flujo_crud.svg`.
- Datos: `entregables/diagramas/flujo_datos.dot`, `flujo_datos.png` y `flujo_datos.svg`.
- Funcional: `entregables/diagramas/flujo_funcional.dot`,
  `flujo_funcional.png` y `flujo_funcional.svg`.
- Lógica: `entregables/diagramas/flujo_logico.dot`,
  `flujo_logico.png` y `flujo_logico.svg`.

### Entregables académicos

| Archivo | Función |
|---|---|
| `entregables/EVIDENCIAS.md` | Reúne el comando de pruebas, el procedimiento de análisis y las capturas incluidas en la exposición. |
| `entregables/Informe_Tecnico_BiblioLogos.docx` | Informe técnico editable del proyecto. |
| `entregables/pdf/Informe_Tecnico_BiblioLogos.pdf` | Versión PDF del informe. |
| `entregables/Presentacion_BiblioLogos.pptx` | Presentación explicativa de 15 diapositivas preparada para 9:30 minutos. |

## 7. Archivos generados

Estos archivos se crean al compilar Angular; se pueden regenerar con `npm run build`
dentro de `frontend/` y no se editan manualmente:

- `frontend/dist/frontend/3rdpartylicenses.txt`: licencias de dependencias incluidas en la compilación.
- `frontend/dist/frontend/browser/favicon.ico`: copia compilada del icono público.
- `frontend/dist/frontend/browser/index.html`: página de entrada compilada.
- `frontend/dist/frontend/browser/main-YK2J5PNN.js`: bundle principal JavaScript; el sufijo puede cambiar al compilar.
- `frontend/dist/frontend/browser/polyfills-5CFQRCPP.js`: compatibilidad de ejecución de JavaScript; el sufijo puede cambiar.
- `frontend/dist/frontend/browser/styles-RMZWM2PI.css`: estilos globales compilados; el sufijo puede cambiar.
- `frontend/dist/frontend/prerendered-routes.json`: metadatos de rutas prerenderizadas del build.

Los nombres con hash dentro de `dist/` pueden variar entre builds. `.gitignore`
define qué cachés, entornos locales y resultados compilados quedan fuera de Git.
