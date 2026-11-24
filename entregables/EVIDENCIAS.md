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

## Evidencias pendientes de captura

- Menú principal de la aplicación.
- Pipeline funcional.
- Recomendación lógica y corte.
- CRUD por API o consola.
- Estadísticas Pandas/NumPy.
- Ejecución de las seis pruebas.
