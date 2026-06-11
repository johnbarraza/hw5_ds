# Reporte Persona 2 - OCR 1964 + Analytical Engine

## Estado

- [x] En progreso
- [ ] Terminado
- [x] Smoke tests aprobados (8/8 en tests/test_ocr_engine.py y tests/test_analytical_engine.py)
- [ ] PR abierto

## Que hice

- Implemente `src/ocr_engine.py` (descarga PDF, render 300dpi via PyMuPDF, OCR con PaddleOCR, parseo a CSV) y `src/analytical_engine.py` (metricas 2025, top peores ejecutores, resumen 1964).
- Descargue el documento 1964, seleccione 15 paginas con cobertura balanceada y genere manifest, evidencia OCR cruda, csv de calidad y CSV final historico.

## Cambio de fuente del documento 1964 (IMPORTANTE)

El enlace de `instrucciones_hw5.md` (fuenteshistoricasdelperu.com -> Google Books id `9YkbAQAAMAAJ`) es de solo vista previa ("snippet"): no permite descargar el PDF ni paginas individuales (la API de imagenes de Google Books devuelve "image not available").

Se uso como sustituto un documento oficial real y descargable: **Memoria del Banco Central de Reserva del Peru, ejercicio 1964** (`https://www.bcrp.gob.pe/docs/Publicaciones/Memoria/Memoria-BCRP-1964.pdf`, 111 paginas). Contiene "Presupuesto de Egresos Ejecutado durante el Ano 1964" y 39 anexos estadisticos (balance del banco, comercio exterior, produccion, etc.), cumpliendo el espiritu del enunciado (matrices financieras 1964 para OCR).

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

- Fuente PDF: Memoria BCRP 1964 (ver seccion anterior).
- Paginas procesadas exactamente 15: 52, 53, 54, 55, 57, 58, 61, 66, 69, 76, 79, 86, 87, 97, 103.
- Criterio de seleccion de paginas: cobertura balanceada entre presupuesto de egresos ejecutado 1964, balance general del BCR, indicadores monetarios, comercio exterior, produccion y balanza de pagos. Detalle y razon por pagina en `data/snapshots/ocr_page_selection_1964.csv`.
- Archivo manifest: `data/snapshots/ocr_page_selection_1964.csv`
- Campos extraidos: `page_number, source_line, category, concept, amount_raw, amount_numeric, parser_confidence`.
- Resolucion usada para convertir PDF a imagen: 300 DPI (PyMuPDF, `zoom = 300/72`).
- Preprocesamiento aplicado: ninguno adicional (renderizado directo a PNG en escala de grises del PDF original); PaddleOCR `lang="es"`, clasificadores de orientacion/unwarp desactivados, `enable_mkldnn=False` (workaround de un bug de paddlepaddle 3.x con oneDNN en CPU).

## Como regenerar

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python -c "
import sys; sys.path.insert(0,'src')
import ocr_engine as oe
paginas = [52,53,54,55,57,58,61,66,69,76,79,86,87,97,103]
oe.exportar_historical_1964(paginas)
"
.venv/Scripts/python -m pytest tests/test_ocr_engine.py tests/test_analytical_engine.py
```

Nota: `_ocr_page` cachea la salida cruda en `data/processed/ocr_pages_1964/page_XXX.json`; borrar ese archivo fuerza re-OCR de esa pagina.

## Validaciones realizadas

- [x] PDF existe y no esta vacio (5.3MB).
- [x] OCR proceso exactamente 15 paginas.
- [x] Ninguna pagina devolvio texto vacio (todas > 50 caracteres).
- [x] Existe `data/snapshots/ocr_page_selection_1964.csv`.
- [x] Existe salida cruda por pagina en `data/processed/ocr_pages_1964/` (PNG + JSON).
- [x] Existe `data/processed/ocr_quality_1964.csv`.
- [x] Cada monto en `historical_1964.csv` conserva `amount_raw` y `page_number`.
- [x] Paginas con baja confianza estan marcadas (columna `manual_review_required`); las 15 paginas dieron `False` (avg_confidence 0.886-0.999).
- [x] CSV 1964 tiene filas utiles (2800 filas, 43 categorias, 2136 montos numericos, 23.7% nulos en columnas de monto).
- [x] Resumen 1964 devuelve metricas numericas (`resumir_1964()` -> `total_categorias`, `total_montos`, `calidad_ocr`, etc.).

## Limitaciones

- PaddleOCR detecta cada fragmento de texto como una linea independiente segun su caja delimitadora; en tablas, la etiqueta (concepto) y su monto suelen quedar en lineas/cajas separadas. El parser actual no agrupa por fila (coordenada Y), por lo que en muchas filas `concept` cae en la categoria de seccion (fallback) en vez del texto contiguo real, aunque `amount_raw`/`amount_numeric`/`page_number`/`source_line` siguen siendo correctos y trazables.
- Algunos titulos de seccion ("ANEXO ...") quedan fragmentados por el OCR en mas de una "categoria" (ej. "AN E X O" vs "ANEXO"), generando categorias duplicadas/ruidosas en `total_categorias`.
- El documento usado es la Memoria BCRP 1964 (sustituto), no la "Cuenta General de la Republica 1964" mencionada literalmente en el enunciado (esa fuente es inaccesible vía Google Books).

## Mejoras posibles

- Capturar `rec_polys` (bounding boxes) del OCR y agrupar fragmentos por banda Y para reconstruir filas tabulares concepto+monto reales.
- Normalizar/deduplicar categorias de "ANEXO" fusionando fragmentos OCR contiguos antes de evaluar `_is_header_line`.
- Usar PP-StructureV3 (table recognition) para las paginas mas tabulares (Anexos XII, XXIX, XXX) en vez de OCR de lineas sueltas.

## Notas de calidad OCR

- Paginas con mejor extraccion (avg_confidence > 0.99): 58, 61, 69, 76, 79, 86, 87, 97 (anexos estadisticos, tipografia tabular limpia).
- Paginas que requieren revision manual: ninguna marcada automaticamente, pero 54 (0.8866), 103 (0.9096) y 52/53/55 (~0.90-0.91) tienen mas ruido tipografico (texto antiguo con ñ/í mal codificados en la capa original).
- Errores comunes observados: simbolos de "ditto" (`>`, `》`) interpretados como caracteres sueltos; titulos en mayusculas fragmentados en multiples cajas OCR.
- Riesgo de interpretacion historica: los totales por categoria son sumas de montos individuales detectados linea por linea; al no estar agrupados por fila de tabla, una misma cifra (ej. un subtotal "Vienen...") puede coexistir con el detalle, por lo que `distribucion_por_categoria` debe leerse como "monto total mencionado en esa seccion", no como suma estrictamente no-redundante.
