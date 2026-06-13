# Reporte Persona 2 - OCR 1964 + Analytical Engine

## Estado

- [x] En progreso
- [x] Terminado
- [x] Smoke tests aprobados (9/9 en tests/test_ocr_engine.py y tests/test_analytical_engine.py)
- [x] PR abierto (#3, ajustes post-merge en #5)

## Que hice

- Implemente `src/ocr_engine.py` (verificacion de PDF local, render 300dpi via PyMuPDF, OCR con PaddleOCR, parseo a CSV) y `src/analytical_engine.py` (metricas 2025, top peores ejecutores, resumen 1964).
- Coloque el documento 1964 oficial, seleccione 15 paginas con cobertura balanceada y genere manifest, evidencia OCR cruda, csv de calidad y CSV final historico.

## Fuente del documento 1964

Documento: **"Cuenta General de la Republica - Ano 1964" (Ministerio de Hacienda y Comercio)**, fuente oficial indicada en `instrucciones_hw5.md` (linea 27), via [Fuentes Historicas del Peru](https://fuenteshistoricasdelperu.com/2021/08/12/ministerio-de-hacienda-y-comercio-presupuesto-balance-y-cuenta-general-de-la-republica/) (Google Books id `9YkbAQAAMAAJ`), 1073 paginas.

El portal no expone un enlace directo de descarga del PDF (solo un visor embebido de Google Books), por lo que el documento se descargo manualmente y se coloco en `data/raw_pdfs/presupuesto_1964.pdf`. `descargar_documento_1964()` solo verifica que el archivo exista localmente y lanza `FileNotFoundError` con instrucciones si falta.

Nota: una version anterior de este pipeline (commit `d13bad8`) uso como sustituto la Memoria del BCRP 1964 (snippet de Google Books inaccesible en ese momento). Esa version fue reemplazada por completo: nuevo PDF, nuevas 15 paginas, nuevo manifest y nuevo CSV historico.

## Archivos creados o modificados

- `src/ocr_engine.py`
- `src/analytical_engine.py`
- `data/raw_pdfs/presupuesto_1964.pdf`
- `data/snapshots/ocr_page_selection_1964.csv`
- `data/processed/ocr_pages_1964/page_XXX.png` y `.json` (15 paginas, evidencia cruda)
- `data/processed/ocr_quality_1964.csv`
- `data/processed/historical_1964.csv`
- `tests/test_ocr_engine.py`, `tests/test_analytical_engine.py`
- `requirements.txt` (cambiado `pdf2image` -> `pymupdf`, ya usado para render de paginas)

## Datos usados

- Fuente PDF: Cuenta General de la Republica 1964, Ministerio de Hacienda y Comercio (ver seccion anterior).
- Paginas procesadas exactamente 15: 38, 100, 190, 226, 272, 358, 421, 532, 644, 854, 1003, 1031, 1037, 1066, 1068.
- Criterio de seleccion de paginas: cobertura balanceada entre ingresos (2), egresos por ministerio (3), pliego/presupuesto funcional (3), deuda publica (1), inversion/obras/departamentos (3), resumen general (2) y egresos del pliego inicial (1). Detalle y razon por pagina en `data/snapshots/ocr_page_selection_1964.csv`.
- Archivo manifest: `data/snapshots/ocr_page_selection_1964.csv`
- Campos extraidos: `page_number, source_line, category, concept, amount_raw, amount_numeric, parser_confidence`.
- Resolucion usada para convertir PDF a imagen: 300 DPI (PyMuPDF, `zoom = 300/72`).
- Preprocesamiento aplicado: ninguno adicional (renderizado directo a PNG en escala de grises del PDF original); PaddleOCR `lang="es"`, clasificadores de orientacion/unwarp desactivados, `enable_mkldnn=False` (workaround de un bug de paddlepaddle 3.x con oneDNN en CPU).

## Como regenerar

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
# Descargar manualmente "Cuenta General de la Republica - Ano 1964" desde
# https://fuenteshistoricasdelperu.com/2021/08/12/ministerio-de-hacienda-y-comercio-presupuesto-balance-y-cuenta-general-de-la-republica/
# y colocarlo en data/raw_pdfs/presupuesto_1964.pdf
.venv/Scripts/python -c "
import sys; sys.path.insert(0,'src')
import ocr_engine as oe
paginas = [38,100,190,226,272,358,421,532,644,854,1003,1031,1037,1066,1068]
oe.exportar_historical_1964(paginas)
"
.venv/Scripts/python -m pytest tests/test_ocr_engine.py tests/test_analytical_engine.py
```

Nota: `_ocr_page` cachea la salida cruda en `data/processed/ocr_pages_1964/page_XXX.json`; borrar ese archivo fuerza re-OCR de esa pagina.

## Validaciones realizadas

- [x] PDF existe y no esta vacio (32.8MB, 1073 paginas).
- [x] OCR proceso exactamente 15 paginas.
- [x] Ninguna pagina devolvio texto vacio (todas > 50 caracteres).
- [x] Existe `data/snapshots/ocr_page_selection_1964.csv`.
- [x] Existe salida cruda por pagina en `data/processed/ocr_pages_1964/` (PNG + JSON).
- [x] Existe `data/processed/ocr_quality_1964.csv`.
- [x] Cada monto en `historical_1964.csv` conserva `amount_raw` y `page_number`.
- [x] Paginas con baja confianza estan marcadas (columna `manual_review_required`); 7 de 15 paginas (38, 190, 226, 272, 358, 532, 854) dieron `True` (avg_confidence 0.757-0.998, ver Notas de calidad OCR).
- [x] CSV 1964 tiene filas utiles (783 filas, 78 categorias, 445 montos numericos, 43.2% nulos en columnas de monto).
- [x] Resumen 1964 devuelve metricas numericas (`resumir_1964()` -> `total_categorias`, `total_montos`, `calidad_ocr`, etc.; `avg_confidence_promedio` 0.8943, `porcentaje_revision_manual` 46.67%).
- [x] `pytest tests/test_ocr_engine.py tests/test_analytical_engine.py` -> 9/9 passed.

## Limitaciones

- PaddleOCR detecta cada fragmento de texto como una linea independiente segun su caja delimitadora; en tablas, la etiqueta (concepto) y su monto suelen quedar en lineas/cajas separadas. El parser actual no agrupa por fila (coordenada Y), por lo que en muchas filas `concept` cae en la categoria de seccion (fallback) en vez del texto contiguo real, aunque `amount_raw`/`amount_numeric`/`page_number`/`source_line` siguen siendo correctos y trazables.
- Titulos de seccion en mayusculas ("MINISTERIO DE...", "CAPITULO...", "TOTAL GENERAL...") suelen quedar fragmentados por el OCR en multiples "categorias" ruidosas (ej. `MINEIRIO`, `MINIEIO`, `MINIIRIO`, `OMACION`, `T�OUT AAUDO`, `TOUTAL LAUDO`). Es la misma clase de problema documentado en la version anterior del pipeline (ahi era "AN E X O"), agravado aqui porque el escaneo de "Cuenta General 1964" tiene tipografia mas pequena/densa que la Memoria BCRP usada antes. Mitigacion aplicada: `_is_header_line` ahora ignora (sin cambiar `current_category`) lineas-encabezado de menos de `MIN_HEADER_CATEGORY_LEN=6` caracteres (ej. `OMACO`, `ECDO`, `RADO`), que eran el grueso del ruido de un solo token; esto bajo `total_categorias` de 97 a 78 sin tocar filas/montos. Quedan fragmentos mas largos (7+ caracteres, ej. `MINEIRIO`, `OMACION`) que requieren la normalizacion/dedup mencionada en Mejoras posibles.
- El escaneo original de varias paginas (38, 190, 226, 272, 358, 532, 854) tiene resolucion/contraste bajos, lo que produce `avg_confidence` entre 0.76 y 0.81 y marca esas paginas como `manual_review_required`.

## Mejoras posibles

- Capturar `rec_polys` (bounding boxes) del OCR y agrupar fragmentos por banda Y para reconstruir filas tabulares concepto+monto reales.
- Normalizar/deduplicar categorias fragmentadas (similitud de string contra una lista conocida de encabezados: "MINISTERIO DE...", "TOTAL GENERAL...", "CAPITULO...") antes de evaluar `_is_header_line`. No implementado: muchos pares de categorias con alta similitud de string son semanticamente opuestos (ej. `INGRESOS` vs `EGRESOS` difieren en distancia de edicion 2, igual que `MINEIRIO`/`MINIIRIO`), por lo que un dedup automatico por similitud arriesga fusionar ingresos con egresos. Requiere lista curada manual, no heuristica generica.
- Usar PP-StructureV3 (table recognition) para las paginas mas tabulares y de baja confianza (38, 190, 226, 272, 358, 532, 854).

## Adiciones post-PR (Tab 1 graficos)

- `resumir_1964(top_n=10)` ahora tambien devuelve `top_categorias_monto` (top-N categorias por monto, listo para grafico de barras sin las 78 categorias ruidosas) y `calidad_ocr["por_pagina"]` (lista `page_number`/`avg_confidence`/`manual_review_required` por pagina, listo para grafico de calidad OCR). 9/9 tests (`test_resumir_1964_top_categorias_y_calidad_por_pagina`).

## Ajustes post-merge (rama fix_part23)

- Persona 1 cambio el filtro 2025 de `PIM > 10M` a `PIM > 1M` (76 entidades, ver `docs/reportes/persona_1_mcp_pipeline.md`). El schema del parquet no cambio (`PIM_2025`, `DEVENGADO_2025`, `Avance`, `Saldo_No_Devengado`, etc.), asi que `analytical_engine.py` sigue funcionando sin cambios estructurales. Se actualizo:
  - `tests/test_analytical_engine.py::test_top_peores_ejecutores_2025`: el assert `PIM_2025 >= 10_000_000` fallaba con el nuevo dataset (min real ~1.0M); cambiado a `>= 1_000_000`.
  - Docstring de `top_peores_ejecutores_2025` ahora dice "PIM > 1M" en vez de "PIM > 10M".
- Fix de calidad para los graficos de Tab 1: la pagina 1066 ("Operaciones Realizadas") repite los totales de EGRESOS/INGRESOS bajo etiquetas casi-duplicadas generadas por fragmentacion de OCR (`TOTAL GENERAL DE LOS EGRESOS`, `TOTAL DE LOS EGRESOS`, `TOTAL GENERAL DE LOS INGRESOS`, `TOTAL DE LOS INGRESOS`, las 4 con el mismo monto que `EGRESOS`/`INGRESOS`). Antes, estas 4 etiquetas duplicadas inflaban `total_monto` (~99B en vez de ~41B) y dominaban/diluian `distribucion_porcentual_categoria` y `top_categorias_monto`. Se agrego `_REDUNDANT_TOTAL_LABELS` en `analytical_engine.py` para excluirlas solo de los campos usados en graficos (`top_categorias_monto`, `distribucion_porcentual_categoria`); `distribucion_por_categoria` y `categorias` (78 categorias) quedan intactos para trazabilidad/auditoria. Resultado: `top_categorias_monto` ahora encabeza con `EGRESOS` (15.03B, 36.9%) e `INGRESOS` (14.07B, 34.5%), seguidos de `LOCAL:` (7.93B) y `DEFICIT POR COMPARACION` (961M) — esta ultima es `EGRESOS - INGRESOS` y es un buen dato narrativo (deficit fiscal de 1964).
- `LOCAL:` sigue siendo una etiqueta poco informativa (suma de 57 lineas de proyectos municipales distintos en la pagina 1037, "Inversiones Indirectas - Gobiernos Locales"); no se renombro porque requeriria mapear cada linea a su municipio (`concept` de la linea anterior), fuera de alcance para esta correccion. Queda documentado como limitacion existente.
- 9/9 tests siguen pasando (`pytest tests/test_analytical_engine.py tests/test_ocr_engine.py`).

## Notas de calidad OCR

- Paginas con mejor extraccion (avg_confidence > 0.97): 421 (0.9909), 644 (0.9764), 854 (0.9976), 1003 (0.9952), 1031 (0.9939), 1037 (0.9914), 1066 (0.9705), 1068 (0.9916).
- Paginas marcadas para revision manual (`manual_review_required=True`): 38 (0.7571), 190 (0.7874), 226 (0.7917), 272 (0.7953), 358 (0.7797), 532 (0.7841) por baja confianza/alto conteo de tokens de baja confianza; 854 (0.9976) por `numeric_token_count=0` (pagina de sumario de deuda sin montos al final de linea detectados por el regex).
- Errores comunes observados: caracteres acentuados (ñ/í/ó) y simbolos de moneda mal reconocidos; titulos en mayusculas fragmentados en multiples cajas OCR (ver Limitaciones).
- Riesgo de interpretacion historica: los totales por categoria son sumas de montos individuales detectados linea por linea; al no estar agrupados por fila de tabla, una misma cifra (ej. un subtotal "Vienen...") puede coexistir con el detalle, por lo que `distribucion_por_categoria` debe leerse como "monto total mencionado en esa seccion", no como suma estrictamente no-redundante.
