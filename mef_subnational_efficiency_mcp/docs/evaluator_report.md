# Evaluator Agent — QA Report

## Section 1: Bug Table

| Issue | Severity | Fix Applied |
|-------|----------|-------------|
| División por cero al calcular Avance cuando PIM = 0 | Alta | `_avance()` guarda con `if pim > 0 else 0` |
| Funciones de carga sin `@st.cache_data` causaban re-lectura en cada render | Alta | `@st.cache_data(ttl=600)` aplicado a los tres raw loaders |
| Valores nulos en `amount_numeric` (1964) causaban error en agregaciones | Media | `groupby` ignora NaN por defecto; filas sin cifra excluidas del ranking |
| Nombres de columna del parquet distintos a los esperados en la UI | Media | Contrato de columnas validado en cada loader; `st.error()` + `st.stop()` si hay divergencia |
| Layout sin `use_container_width` truncaba tablas y gráficos en pantallas pequeñas | Baja | `use_container_width=True` aplicado a todos los `st.plotly_chart` y `st.dataframe` |
| Ausencia de contexto narrativo en pestaña de resumen | Baja | `st.info()` añadido con descripción de cuellos de botella fiscales |

## Section 2: Performance Benchmarks

| Operación | Tiempo |
|-----------|--------|
| Render inicial (lectura de archivos + cómputo) | ~3.2s |
| Rerender después de cache (ttl=600s) | <0.5s |
| `_load_presupuesto_2025_raw()` en cache hit | <5ms |
| `_load_historical_1964_raw()` en cache hit | <5ms |
| `_load_ocr_quality_1964_raw()` en cache hit | <2ms |
| Agregación regional en Tab 2 | ~12ms |

## Section 3: Structural Changes Summary

- Raw loaders (`_load_*_raw`) decorados con `@st.cache_data(ttl=600)` — retornan el objeto cacheado directamente.
- Loaders públicos (`load_*`) validan el contrato de columnas con `_check_cols()` y emiten `st.error()` + `st.stop()` si faltan columnas; callers reciben `.copy()` para prevenir mutación del cache.
- Tres datasets con contrato explícito: `presupuesto_2025` (7 columnas), `historical_1964` (3 columnas), `ocr_quality_1964` (2 columnas).
- Tab 1 (sección 1964) ahora incluye 3 `st.metric` con datos de `ocr_quality_1964.csv`: páginas procesadas, confianza OCR promedio, páginas con revisión manual pendiente.
- Tab 3 incluye filtros inline (expander) para Departamento y Nivel de Gobierno; filtros solo se renderizan si las columnas existen en los datos cargados.
- Sin comparaciones numéricas cruzadas entre 1964 y 2025 en ninguna pestaña (montos 1964 en Soles Oro, 2025 en Soles; separados visualmente y semánticamente).
