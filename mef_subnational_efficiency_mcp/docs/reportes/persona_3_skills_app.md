# Reporte Persona 3 - Skills + Streamlit + README

## Estado

- [ ] En progreso
- [ ] Terminado
- [ ] Smoke tests aprobados
- [ ] PR abierto

## Que hice

TODO.

## Archivos creados o modificados

- `.claude/skills/executor_skill.json`
- `.claude/skills/evaluator_skill.json`
- `app.py`
- `src/utils.py`
- `README.md`
- `requirements.txt`
- `docs/evaluator_report.md`
- `video/link.txt`

## Datos usados

- Archivo 2025:
- Archivo 1964:
- Archivo calidad OCR:
- Periodo default:
- Reporte evaluator:

## Como ejecutar

```bash
streamlit run app.py
```

## Validaciones realizadas

- [ ] JSON de Skills valido.
- [ ] App importa sin errores.
- [ ] App tiene exactamente 4 tabs.
- [ ] App usa cache con `ttl` o `max_entries`.
- [ ] App tiene fallback si faltan archivos procesados.
- [ ] App valida contrato de columnas antes de graficar.
- [ ] App maneja `PIM = 0`.
- [ ] Tab 1 separa 2025 y 1964.
- [ ] Tabs 2, 3 y 4 usan solo 2025.
- [ ] Se ejecuto prueba con `streamlit.testing.v1.AppTest`.
- [ ] Se midio tiempo de render inicial y rerender con cache.

## Limitaciones

TODO.

## Mejoras posibles

TODO.

## Benchmark Streamlit

- Render inicial:
- Rerender despues de cache:
- Operaciones cacheadas:
- Cuellos de botella restantes:
