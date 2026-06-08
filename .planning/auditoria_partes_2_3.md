# Auditoria de suficiencia - Partes 2 y 3

Fecha: 2026-06-07

## Conclusion corta

La division original cubria lo minimo del enunciado, pero le faltaban controles para defender calidad:

- Parte 2 necesitaba trazabilidad de OCR, control de confianza y evidencia de seleccion de paginas.
- Parte 3 necesitaba contratos de columnas, fallbacks de archivos faltantes, pruebas reales de Streamlit y cache con limites.
- "Data balanceado" no aplica como balanceo de clases porque no hay modelo ML entrenado, pero si aplica balance de cobertura: las 15 paginas OCR deben cubrir tipos de contenido relevantes y no solo paginas faciles.

## Fuentes revisadas

- PaddleOCR OCR pipeline: https://www.paddleocr.ai/main/en/version3.x/pipeline_usage/OCR.html
- PaddleOCR PP-StructureV3: https://www.paddleocr.ai/main/en/version3.x/pipeline_usage/PP-StructureV3.html
- Streamlit caching: https://docs.streamlit.io/develop/concepts/architecture/caching
- Streamlit AppTest: https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest

## Gaps detectados en Parte 2

- No habia archivo obligatorio para manifestar que paginas se seleccionaron ni por que.
- No habia metrica de calidad OCR por pagina.
- No se exigia guardar OCR crudo por pagina para auditoria.
- No se exigia trazabilidad `amount_raw` -> `amount_numeric`.
- No se distinguia entre OCR general y table/document parsing para tablas complejas.
- No se exigia reportar paginas que requieren revision manual.

## Ajuste recomendado para Parte 2

Archivos nuevos a exigir:

- `data/snapshots/ocr_page_selection_1964.csv`
- `data/processed/ocr_pages_1964/`
- `data/processed/ocr_quality_1964.csv`

Columnas minimas:

- `ocr_page_selection_1964.csv`: `page_number`, `page_index`, `reason`, `content_type`, `quality_note`
- `ocr_quality_1964.csv`: `page_number`, `line_count`, `numeric_token_count`, `avg_confidence`, `low_confidence_count`, `manual_review_required`
- `historical_1964.csv`: `page_number`, `source_line`, `category`, `concept`, `amount_raw`, `amount_numeric`, `parser_confidence`

Validaciones minimas:

- Exactamente 15 paginas.
- Ninguna pagina con menos de 50 caracteres extraidos.
- Cada pagina con al menos algun token numerico si se eligio por matriz financiera.
- Montos numericos rastreables a texto original.
- Paginas de baja confianza marcadas, no ocultadas.

## Gaps detectados en Parte 3

- El checklist pedia `@st.cache_data`, pero no limites de cache.
- No habia prueba de que el app tenga exactamente 4 tabs con Streamlit.
- No habia fallback si faltan datos procesados.
- No habia contrato de columnas para evitar errores silenciosos.
- El evaluator report estaba mencionado, pero sin archivo estable.
- No habia benchmark obligatorio para el video.

## Ajuste recomendado para Parte 3

Archivo nuevo a exigir:

- `docs/evaluator_report.md`

Contratos minimos:

- 2025: `PIM`, `DEVENGADO`, region/departamento, unidad ejecutora o entidad, periodo.
- 1964: `page_number`, `category`, `concept`, `amount_raw`, `amount_numeric`.
- OCR quality: `page_number`, `avg_confidence`, `manual_review_required`.

Validaciones minimas:

- `AppTest.from_file("app.py").run()` ejecuta sin excepciones.
- La app renderiza exactamente 4 tabs.
- Si falta un processed file, la app muestra aviso accionable y no crashea.
- Tabs 2, 3 y 4 no leen ni muestran dataset 1964.
- Tab 1 no calcula comparaciones entre 2025 y 1964.
- Cache usa `ttl` o `max_entries`.

## Buenas practicas integradas

- Para OCR: guardar evidencia intermedia, confianza por pagina y trazabilidad de montos.
- Para tablas: considerar PP-StructureV3 cuando la pagina sea tabular o tenga layout complejo.
- Para Streamlit: cachear cargas y transformaciones, limitar cache con `ttl` o `max_entries`, y probar con AppTest.
- Para presentacion: reportar benchmarks antes/despues y limitaciones reales, especialmente OCR de baja calidad.
