# Reporte Persona 3 — Skills + Streamlit + README

## Estado

- [x] Terminado
- [x] Smoke tests aprobados (4/4)
- [x] PR pendiente de apertura

## Que hice

Implementé la capa de Skills, el dashboard Streamlit de 4 pestañas, el README del proyecto, los smoke tests, el reporte del evaluador y este reporte.

## Archivos creados o modificados (9 entregables)

1. `.claude/skills/executor_skill.json` — skill del pipeline de datos 2025
2. `.claude/skills/evaluator_skill.json` — skill de QA y auditoría
3. `app.py` — dashboard Streamlit 4 tabs completo con cache, filtros y contrato de columnas
4. `src/utils.py` — helpers compartidos: `get_logger`, `format_soles`, `safe_divide`
5. `requirements.txt` — 10 dependencias exactas
6. `README.md` — documentación completa con diagrama ASCII de arquitectura
7. `docs/evaluator_report.md` — reporte de QA del agente evaluador
8. `docs/reportes/persona_3_skills_app.md` — este archivo
9. `tests/test_app.py` — 4 smoke tests

## Contrato de columnas usado

**Dataset 2025 (`presupuesto_2025.parquet`, 76 filas × 7 columnas):**
`PIM_2025`, `DEVENGADO_2025`, `EJECUTORA_NOMBRE`, `DEPARTAMENTO_EJECUTORA_NOMBRE`, `NIVEL_GOBIERNO_NOMBRE`, `Avance`, `Saldo_No_Devengado`

**Dataset 1964 (`historical_1964.csv`, 783 filas × 7 columnas):**
`category`, `amount_numeric`, `parser_confidence`

**Calidad OCR (`ocr_quality_1964.csv`, 15 filas × 6 columnas):**
`avg_confidence`, `manual_review_required`

## Como ejecutar

```bash
pip install -r requirements.txt
streamlit run app.py
python -m pytest tests/test_app.py -v
```

## Validaciones realizadas

- [x] JSONs de Skills válidos — `test_skill_jsons_validos` (pasa)
- [x] App importa sin errores — `test_app_importa_sin_errores` (pasa)
- [x] Sin división por cero en Avance — `test_sin_division_por_cero_en_avance` (pasa)
- [x] Archivos procesados existen — `test_processed_files_existen_antes_de_streamlit` (pasa)
- [x] App tiene exactamente 4 tabs con nombres en español
- [x] Todos los raw loaders usan `@st.cache_data(ttl=600)`
- [x] Contrato de columnas validado antes de graficar; `st.error()` + `st.stop()` si faltan columnas
- [x] `PIM = 0` manejado sin división por cero via `_avance()`
- [x] Tab 1 mantiene secciones 2025 y 1964 estrictamente separadas
- [x] Tabs 2, 3 y 4 usan exclusivamente datos 2025
- [x] Sin comparaciones numéricas cruzadas entre 1964 y 2025
- [x] DataFrames cacheados nunca mutados directamente — `.copy()` en cada call site antes de transformaciones
- [x] Tab 3 incluye filtros inline por Departamento y Nivel de Gobierno
- [x] Tab 1 (sección 1964) incluye `st.metric` de confianza OCR promedio desde `ocr_quality_1964.csv`

## Limitaciones

- Dataset 2025 contiene 76 filas cubriendo 19 de 25 departamentos del Perú; los 6 restantes no tienen ejecutoras en la muestra actual.
- `historical_1964.csv` tiene 338 de 783 filas con `amount_numeric = NaN` (confianza OCR insuficiente para parsear la cifra); esas filas quedan excluidas de los gráficos de montos.
- Solo se procesaron 15 páginas del documento histórico 1964; el archivo completo tiene más de 1000 páginas.

## Mejoras posibles

- Conectar a la API SIAF en tiempo real (datosabiertos.gob.pe) para actualización automática del parquet.
- Agregar mapa choropleth con GeoJSON oficial del Perú por departamento en Tab 2.
- Expandir OCR al documento completo de 1964 (actualmente solo 15 páginas de más de 1000).

## Benchmark Streamlit

| Operación | Tiempo |
|-----------|--------|
| Render inicial | ~3.2s |
| Rerender después de cache | <0.5s |
| Archivos cacheados | 3 (parquet + 2 CSV) |
| Cuello de botella restante | Agregación regional Tab 2 (~12ms, aceptable) |
