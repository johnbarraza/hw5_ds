# Reporte Persona 2 - OCR 1964 + Analytical Engine

## Estado

- [ ] En progreso
- [ ] Terminado
- [ ] Smoke tests aprobados
- [ ] PR abierto

## Que hice

TODO.

## Archivos creados o modificados

- `src/ocr_engine.py`
- `src/analytical_engine.py`
- `data/raw_pdfs/presupuesto_1964.pdf`
- `data/processed/historical_1964.csv`

## Datos usados

- Fuente PDF:
- Paginas procesadas exactamente 15:
- Criterio de seleccion de paginas:
- Archivo manifest: `data/snapshots/ocr_page_selection_1964.csv`
- Campos extraidos:
- Resolucion usada para convertir PDF a imagen:
- Preprocesamiento aplicado:

## Como regenerar

```bash
TODO
```

## Validaciones realizadas

- [ ] PDF existe y no esta vacio.
- [ ] OCR proceso exactamente 15 paginas.
- [ ] Ninguna pagina devolvio texto vacio.
- [ ] Existe `data/snapshots/ocr_page_selection_1964.csv`.
- [ ] Existe salida cruda por pagina en `data/processed/ocr_pages_1964/`.
- [ ] Existe `data/processed/ocr_quality_1964.csv`.
- [ ] Cada monto en `historical_1964.csv` conserva `amount_raw` y `page_number`.
- [ ] Paginas con baja confianza estan marcadas para revision manual.
- [ ] CSV 1964 tiene filas utiles.
- [ ] Resumen 1964 devuelve metricas numericas.

## Limitaciones

TODO.

## Mejoras posibles

TODO.

## Notas de calidad OCR

- Paginas con mejor extraccion:
- Paginas que requieren revision manual:
- Errores comunes observados:
- Riesgo de interpretacion historica:
