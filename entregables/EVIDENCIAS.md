# Evidencias de validación

## Ejecución técnica

Comando:

```bash
./.venv/bin/python -m unittest discover -s tests -v
```

Resultado esperado: 6 pruebas aprobadas.

## Análisis NumPy/Pandas

Comando:

```bash
./.venv/bin/python - <<'PY'
from analisis_datos import cargar_catalogo, generar_indicadores
df = cargar_catalogo("tests/fixtures/catalogo_pruebas.csv")
print(generar_indicadores(df))
PY
```

## Capturas incluidas en la exposición

La presentación dura aproximadamente 9 minutos y 30 segundos, con 30 segundos
de margen para no superar el límite de 10 minutos. Se seleccionaron solo las
capturas necesarias para explicar la interfaz y los conceptos principales:

- `capturas/busqueda_resultados.png`: búsqueda real desde la interfaz web.
- `capturas/codigo_motor_funcional_101_129.png`: pipeline `filter`, `map` y `reduce`.
- `capturas/codigo_motor_logico_229_256.png`: inferencia, orden y corte, simulados en Python.
- `capturas/codigo_modelos_103_121.png`: herencia en `LibroFisico`.
- `capturas/codigo_routes_101_129.png`: endpoints CRUD de FastAPI.
- `capturas/codigo_analisis_datos_27_43.png`: indicadores con Pandas y NumPy.

Las imágenes de código se regeneran automáticamente al ejecutar
`./.venv/bin/python scripts/generar_presentacion.py`.
