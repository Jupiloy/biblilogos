# Evidencias de validación

## Ejecución técnica

Comando:

```bash
./.venv/bin/python -m unittest discover -s tests -v
```

Resultado verificado: 14 pruebas Python aprobadas.

## Análisis NumPy/Pandas del catálogo actual

Ejecuta el análisis contra el catálogo persistente en SQLite:

```bash
./.venv/bin/python -m analisis_datos
```

La lectura de `data/catalogo.db` es de solo lectura; los reportes se generan en
`entregables/reportes/`. El CSV pequeño de pruebas permanece como fixture para
reproducir los casos automatizados.

Para ejecutar los indicadores sobre el CSV fijo de prueba:

```bash
./.venv/bin/python - <<'PY'
from analisis_datos import cargar_catalogo, generar_indicadores
df = cargar_catalogo("tests/fixtures/catalogo_pruebas.csv")
print(generar_indicadores(df))
PY
```

## Capturas incluidas en la exposición

La presentación tiene 15 diapositivas y dura aproximadamente 9 minutos y 30
segundos, con 30 segundos de margen para no superar el límite de 10 minutos.
Incluye capturas y diagramas para explicar la interfaz y los conceptos:

- `capturas/busqueda_resultados.png`: búsqueda real desde la interfaz web.
- `capturas/codigo_motor_funcional_101_129.png`: pipeline `filter`, `map` y `reduce`.
- `capturas/codigo_motor_logico_229_256.png`: inferencia, orden y corte, simulados en Python.
- `capturas/codigo_modelos_103_121.png`: herencia en `LibroFisico`.
- `capturas/codigo_routes_101_129.png`: endpoints CRUD de FastAPI.
- `capturas/codigo_analisis_datos_27_43.png`: indicadores con Pandas y NumPy.

Las imágenes de código se regeneran automáticamente al ejecutar
`./.venv/bin/python scripts/generar_presentacion.py`.

## Catálogo web persistente

La opción **Mi catálogo** de la interfaz permite crear, consultar, actualizar y
eliminar publicaciones locales. Los cambios se guardan en `data/catalogo.db` y
se conservan al reiniciar el backend. Los favoritos de **Guardados** son una
colección personal aparte almacenada en el navegador.

## Acceso por roles

Las cuentas lectoras pueden registrarse desde la interfaz, buscar publicaciones y
ver recomendaciones. La cuenta administradora se crea localmente con
`./.venv/bin/python -m backend.create_admin`; solo ese rol puede ejecutar el CRUD
del catálogo. La API verifica la sesión y el rol en cada operación protegida.
