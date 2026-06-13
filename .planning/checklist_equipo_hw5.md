# HW5 - Checklist maestro de equipo

Este archivo es la fuente unica para coordinar el trabajo de las 3 personas. Cada integrante debe marcar sus avances aqui y, al terminar, completar su reporte individual en `mef_subnational_efficiency_mcp/docs/reportes/`.

## Rama de trabajo

- Rama actual para esta estructura: `feature/team-workplan-structure`
- Regla: no trabajar directo en `main`.
- Cada bloque funcional debe ir en una rama descriptiva:
  - Persona 1: `feature/mcp-server-core` y `feature/data-snapshot-pipeline`
  - Persona 2: `feature/historical-1964-paddle-ocr` y `feature/analytical-engine`
  - Persona 3: `feature/executor-dashboard-draft` y `feature/evaluator-qa-refinement`

## Estructura oficial de archivos

Todos deben trabajar dentro de:

```text
mef_subnational_efficiency_mcp/
  app.py
  README.md
  requirements.txt
  .claude/
    skills/
      executor_skill.json
      evaluator_skill.json
  src/
    mcp_server.py
    data_pipeline.py
    ocr_engine.py
    analytical_engine.py
    utils.py
  data/
    raw_pdfs/
    snapshots/
    processed/
  docs/
    evaluator_report.md
    reportes/
      persona_1_mcp_pipeline.md
      persona_2_ocr_analytics.md
      persona_3_skills_app.md
  video/
    link.txt
```

## Reglas obligatorias

- [x] No subir datos crudos pesados al contexto del LLM.
- [ ] No leer CSV/JSON completos desde los Skills.
- [x] Inspeccionar maximo 5 a 10 filas para schema y muestras.
- [x] Procesar datasets pesados con scripts locales en Python.
- [x] Guardar salidas reducidas en `data/processed/`.
- [ ] Usar exactamente 15 paginas del PDF 1964 para OCR, salvo que el profesor indique otra cosa.
- [ ] Guardar evidencia de seleccion/calidad OCR, no solo el CSV final.
- [ ] Mantener Tab 1 con resumen independiente 2025 y 1964, sin comparaciones numericas entre epocas.
- [ ] Mantener Tabs 2, 3 y 4 solo con informacion moderna 2025.
- [ ] Validar contratos de columnas antes de lanzar Streamlit.
- [ ] Correr smoke tests antes del PR.
- [ ] Crear PR descriptivo para merge.

## Persona 1 - MCP Server + Data Pipeline 2025

Responsable de conectar con `datosabiertos.gob.pe`, inspeccionar datasets sin descargar todo y producir datos modernos reducidos.

### Entregables

- [x] `src/mcp_server.py`
- [x] `src/data_pipeline.py`
- [x] `data/snapshots/`
- [x] `data/processed/presupuesto_2025.parquet`
- [x] Reporte final: `docs/reportes/persona_1_mcp_pipeline.md`

### Checklist de trabajo

- [x] Crear rama `feature/mcp-server-core`.
- [x] Implementar tool `buscar_datasets`.
- [x] Implementar tool `obtener_detalle_dataset`.
- [x] Implementar tool `inspeccionar_esquema_csv` con maximo 10 filas.
- [x] Implementar tool `consultar_datastore_filtrado`.
- [x] Implementar tool `obtener_ultimas_actualizaciones`.
- [x] Implementar tool `listar_entidades_publicas`.
- [ ] Verificar conexion CKAN sin autenticacion. (portal MEF no tiene CKAN API funcional — ver reporte)
- [x] Crear rama `feature/data-snapshot-pipeline`.
- [x] Guardar schema/muestra en `data/snapshots/`.
- [x] Filtrar entidades con `PIM > 1000000`. (umbral ajustado por limitaciones de descarga — ver reporte)
- [x] Calcular `Avance = (Devengado / PIM) * 100`.
- [x] Calcular `Saldo No Devengado = PIM - Devengado`.
- [x] Guardar salida pequena en `data/processed/`.
- [x] Validar que no existan divisiones por cero.
- [ ] Correr smoke tests de MCP y pipeline. (pendiente dia 11 buffer)
- [x] Completar reporte individual con archivos usados, limitaciones y mejoras.
- [x] Abrir PR.

### Debe dejar listo para Persona 3

- [x] Archivo procesado 2025 en `data/processed/`. (76 filas, parquet < 50KB)
- [x] Nombres de columnas documentados en el reporte.
- [x] Periodo exacto usado documentado. (2025, columnas PIM_2025 y DEVENGADO_2025)
- [x] Comando para regenerar datos documentado.

## Persona 2 - OCR 1964 + Analytical Engine

Responsable del PDF historico, PaddleOCR y funciones analiticas compartidas.

### Entregables

- [ ] `src/ocr_engine.py`
- [ ] `src/analytical_engine.py`
- [ ] `data/raw_pdfs/presupuesto_1964.pdf`
- [ ] `data/snapshots/ocr_page_selection_1964.csv`
- [ ] `data/processed/historical_1964.csv`
- [ ] `data/processed/ocr_quality_1964.csv`
- [ ] Reporte final: `docs/reportes/persona_2_ocr_analytics.md`

### Checklist de trabajo

- [ ] Crear rama `feature/historical-1964-paddle-ocr`.
- [ ] Descargar PDF 1964 en `data/raw_pdfs/presupuesto_1964.pdf`.
- [ ] Seleccionar exactamente 15 paginas con tablas o matrices financieras.
- [ ] Documentar numeros de pagina usados.
- [ ] Guardar manifest de paginas en `data/snapshots/ocr_page_selection_1964.csv` con columnas: `page_number`, `page_index`, `reason`, `content_type`, `quality_note`.
- [ ] Balancear cobertura documental de las 15 paginas: incluir, si existen en el PDF, ingresos, gastos, departamentos/entidades y cuadros/resumenes; no escoger solo las paginas mas faciles.
- [ ] Convertir paginas a imagen con resolucion fija documentada, idealmente 300 DPI, para que el OCR sea reproducible.
- [ ] Aplicar preprocesamiento minimo si hace falta: rotacion/orientacion, escala de grises, contraste o binarizacion, sin alterar los montos.
- [ ] Ejecutar PaddleOCR sobre las 15 paginas.
- [ ] Usar OCR general para texto y considerar PP-Structure/table recognition cuando la pagina tenga tablas complejas.
- [ ] Guardar salida cruda por pagina en un formato auditable, por ejemplo JSONL o TXT dentro de `data/processed/ocr_pages_1964/`.
- [ ] Verificar que ninguna pagina devuelva texto vacio.
- [ ] Guardar `data/processed/ocr_quality_1964.csv` con: `page_number`, `line_count`, `numeric_token_count`, `avg_confidence`, `low_confidence_count`, `manual_review_required`.
- [ ] Marcar revision manual si `avg_confidence` es baja, si hay pocos numeros o si el texto extraido es menor a 50 caracteres.
- [ ] Parsear categorias, departamentos, montos o conceptos relevantes.
- [ ] Conservar columnas de trazabilidad en `historical_1964.csv`: `page_number`, `source_line`, `category`, `concept`, `amount_raw`, `amount_numeric`, `parser_confidence`.
- [ ] Normalizar montos con funcion unica y documentar separadores de miles/decimales.
- [ ] Validar que cada monto numerico venga de un `amount_raw` rastreable.
- [ ] Guardar datos limpios en `data/processed/historical_1964.csv`.
- [ ] Crear rama `feature/analytical-engine`.
- [ ] Implementar metricas 2025 reutilizables en `analytical_engine.py`.
- [ ] Implementar resumen 1964 reutilizable en `analytical_engine.py`.
- [ ] Implementar resumen de calidad OCR: paginas procesadas, lineas extraidas, porcentaje con revision manual y conteo de montos.
- [ ] Confirmar que `analytical_engine.py` solo lee `data/processed/`.
- [ ] Correr smoke tests de OCR y resumen 1964.
- [ ] Completar reporte individual con archivos usados, limitaciones y mejoras.
- [ ] Abrir PR.

### Debe dejar listo para Persona 3

- [ ] CSV 1964 limpio en `data/processed/`.
- [ ] Carpeta `data/processed/ocr_pages_1964/` con texto/JSON por pagina.
- [ ] Archivo `data/processed/ocr_quality_1964.csv`.
- [ ] Lista de 15 paginas usadas.
- [ ] Explicacion breve de metricas historicas.
- [ ] Comando para regenerar OCR documentado.

## Persona 3 - Skills + Streamlit + README

Responsable de Skills, app final, documentacion y video demo.

### Entregables

- [ ] `.claude/skills/executor_skill.json`
- [ ] `.claude/skills/evaluator_skill.json`
- [ ] `app.py`
- [ ] `src/utils.py`
- [ ] `README.md`
- [ ] `requirements.txt`
- [ ] `docs/evaluator_report.md`
- [ ] `video/link.txt`
- [ ] Reporte final: `docs/reportes/persona_3_skills_app.md`

### Checklist de trabajo

- [ ] Crear rama `feature/executor-dashboard-draft`.
- [ ] Definir `executor_skill.json` con soporte para periodos tipo `period 2025-12`.
- [ ] Definir `evaluator_skill.json` con validacion, cache y reporte de QA.
- [ ] Implementar helpers de logging en `src/utils.py`.
- [ ] Completar `requirements.txt` con `paddleocr`, `streamlit`, `fastmcp`, `pandas`, `plotly`.
- [ ] Completar README con setup, arquitectura, ejecucion y regeneracion.
- [ ] Crear rama `feature/evaluator-qa-refinement`.
- [ ] Definir contrato de columnas esperadas para 2025 y 1964 antes de cargar visualizaciones.
- [ ] Implementar fallback claro si faltan archivos procesados, sin romper toda la app.
- [ ] Construir `app.py` con exactamente 4 tabs.
- [ ] Tab 1: KPIs 2025 y seccion 1964 independiente.
- [ ] Tab 1: incluir al menos 2 graficos de datos 1964.
- [ ] Tab 1: mostrar nota de calidad OCR basada en `ocr_quality_1964.csv`.
- [ ] Tab 2: distribucion territorial/geoespacial 2025.
- [ ] Tab 2: validar que los departamentos tengan nombres/codigos consistentes antes del mapa.
- [ ] Tab 3: peores ejecutores con `PIM > 1M`. (umbral ajustado por Persona 1 — ver reporte P1)
- [ ] Tab 3: incluir filtros por region/departamento, tipo de gobierno, funcion/categoria y periodo si esas columnas existen.
- [ ] Tab 4: audit log del evaluator y playground de periodo.
- [ ] Escribir el audit log final en `docs/evaluator_report.md`.
- [ ] Agregar `@st.cache_data` para cargas y agregaciones con `ttl` o `max_entries` definidos.
- [ ] Usar `st.cache_resource` solo para recursos pesados compartidos, como modelos o clientes, si se cargan dentro de la app.
- [ ] Evitar mutar DataFrames devueltos directamente por cache sin hacer copia local.
- [ ] Manejar `PIM = 0` sin division por cero.
- [ ] Formatear montos PEN y porcentajes de forma consistente.
- [ ] Verificar que no haya comparaciones numericas 2025 vs 1964.
- [ ] Medir render inicial y rerender despues de cache para reportar benchmark en el video.
- [ ] Correr smoke tests de app y JSON.
- [ ] Completar reporte individual con archivos usados, limitaciones y mejoras.
- [ ] Guardar link de video en `video/link.txt`.
- [ ] Abrir PR.

### Depende de

- [x] `data/processed/presupuesto_2025.parquet` de Persona 1. (listo, 76 filas, PIM > 1M)
- [ ] `data/processed/historical_1964.csv` de Persona 2.
- [ ] `data/processed/ocr_quality_1964.csv` de Persona 2.
- [ ] `docs/evaluator_report.md` generado por el evaluator.

## Checklist de video

- [ ] Maximo 5 minutos.
- [ ] Usar 3 a 4 slides, no walkthrough de codigo.
- [ ] Explicar construccion de Skills.
- [ ] Explicar arquitectura MCP y estrategia anti-context flooding.
- [ ] Explicar pipeline PaddleOCR 1964.
- [ ] Explicar asignacion de tools MCP.
- [ ] Explicar optimizaciones de eficiencia.
- [ ] Indicar benchmarks antes/despues.
- [ ] Explicar impacto del Evaluator.
- [ ] Mostrar Streamlit funcionando.
- [ ] Mostrar los 4 tabs.
- [ ] Explicar hallazgos 1964 y sus 2 graficos.
- [ ] Explicar limitaciones y siguientes mejoras.
- [ ] Pegar link final en `video/link.txt`.

## Definition of Done del equipo

- [ ] Estructura de repo coincide con el enunciado.
- [ ] MCP server corre y consulta CKAN.
- [x] Datos 2025 procesados existen y son pequenos. (76 filas, parquet < 50KB)
- [ ] PDF 1964 existe en `data/raw_pdfs/`.
- [ ] OCR procesa exactamente 15 paginas.
- [ ] `historical_1964.csv` existe y tiene datos utiles.
- [ ] `ocr_quality_1964.csv` existe y permite defender calidad/limitaciones OCR.
- [ ] La seleccion de paginas 1964 tiene cobertura documental, no solo paginas faciles.
- [ ] Skills JSON son validos.
- [ ] Streamlit tiene exactamente 4 tabs.
- [ ] App usa cache con limites de duracion o tamano.
- [ ] App tiene pruebas de contrato para columnas, tabs y fallbacks.
- [ ] README permite correr el sistema desde cero.
- [ ] Reportes individuales estan completos.
- [ ] Video esta linkeado.
- [ ] PRs revisados y mergeados.
