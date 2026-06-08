
# HW5 — División de Trabajo + Smoke Tests

**Deadline: domingo 14, 11:59 PM**

---

## 👤 Persona 1 — MCP Server + Data Pipeline 2025

**Entregables:** `src/mcp_server.py`, `src/data_pipeline.py`, `data/snapshots/`, `data/processed/` (datos 2025)

### Pasos

**Día 8-9:**

- Crear el repo `mef_subnational_efficiency_mcp` con la estructura exacta del enunciado, primer commit en `main`
- Branch `feature/mcp-server-core` → `mcp_server.py` con tools: `buscar_datasets`, `obtener_detalle_dataset`, `inspeccionar_esquema_csv`, `consultar_datastore_filtrado`, `obtener_ultimas_actualizaciones`, `listar_entidades_publicas`
- Verificar que conecta con `datosabiertos.gob.pe` vía CKAN API sin autenticación

**Día 10:**

- Branch `feature/data-snapshot-pipeline` → `data_pipeline.py`: tomar solo 10 filas del CSV MEF/SIAF 2025, guardar schema en `data/snapshots/`
- Generar script que filtra PIM > 10M soles, calcula `Avance = (Devengado/PIM)*100` y `Saldo No Devengado = PIM - Devengado`
- ⚠️ Guardar resultado en `data/processed/` como Parquet o CSV pequeño — **Persona 3 lo necesita para arrancar el app**
- PR a main

**Día 11-12:** Buffer debugging + grabar segmento video (slides 1-2: arquitectura MCP y estrategia anti-context flooding)

### 🧪 Smoke Tests

```python
# tests/test_mcp_server.py

def test_mcp_conecta_ckan():
    """El servidor MCP responde y el endpoint CKAN está accesible."""
    resultado = buscar_datasets("presupuesto 2025")
    assert resultado is not None
    assert len(resultado) > 0, "CKAN no devolvió datasets"

def test_inspeccion_schema_no_descarga_completo():
    """inspeccionar_esquema_csv devuelve máximo 10 filas, nunca el CSV completo."""
    muestra = inspeccionar_esquema_csv(url_csv)
    assert len(muestra) <= 10, "⚠️ Está descargando más de 10 filas — riesgo de context flooding"
    assert "PIM" in muestra.columns, "Columna PIM no encontrada — puede haber cambio de schema"
    assert "DEVENGADO" in muestra.columns, "Columna DEVENGADO no encontrada"

def test_pipeline_columnas_criticas():
    """El processed data tiene las columnas necesarias y sin nulos críticos."""
    import pandas as pd
    df = pd.read_parquet("data/processed/presupuesto_2025.parquet")
    assert "PIM" in df.columns
    assert "DEVENGADO" in df.columns
    assert df["PIM"].isnull().sum() == 0, "Hay nulos en PIM"
    assert (df["PIM"] > 0).all(), "⚠️ Hay PIM = 0 — causará división por cero en Avance%"
    assert df["PIM"].min() >= 10_000_000, "Filtro PIM > 10M no se aplicó correctamente"

def test_metricas_avance():
    """Avance% está entre 0 y 100, Saldo No Devengado no es negativo."""
    import pandas as pd
    df = pd.read_parquet("data/processed/presupuesto_2025.parquet")
    df["Avance"] = (df["DEVENGADO"] / df["PIM"]) * 100
    df["Saldo"] = df["PIM"] - df["DEVENGADO"]
    assert df["Avance"].between(0, 100).all(), "⚠️ Avance% fuera de rango — revisar datos"
    assert (df["Saldo"] >= 0).all(), "⚠️ Saldo negativo detectado — Devengado > PIM en alguna fila"
```

---

## 👤 Persona 2 — OCR 1964 + Analytical Engine

**Entregables:** `src/ocr_engine.py`, `src/analytical_engine.py`, `data/raw_pdfs/`, `data/processed/` (datos 1964)

### Pasos

**Día 8-9:**

- Branch `feature/historical-1964-paddle-ocr` → descargar PDF histórico a `data/raw_pdfs/`
- Seleccionar exactamente **15 páginas** con tablas financieras (no más, indicación del profe)
- Correr PaddleOCR sobre esas 15 páginas, parsear output para extraer categorías de ingresos/gastos, departamentos, montos
- Guardar en `data/processed/historical_1964.csv`

**Día 10:**

- Branch `feature/analytical-engine` → `analytical_engine.py`: funciones de métricas 2025 (agrupaciones por región, top peores ejecutores) + resumen 1964 (totales por categoría, distribución porcentual)
- Todo opera sobre `data/processed/`, nunca sobre archivos raw
- ⚠️ Entregar `historical_1964.csv` limpio — **Persona 3 lo necesita para Tab 1**
- PR a main

**Día 11-12:** Buffer debugging + grabar segmento video (slides 3-4: OCR pipeline y hallazgos 1964)

### 🧪 Smoke Tests

```python
# tests/test_ocr_engine.py

def test_pdf_descargado():
    """El PDF histórico existe y no está vacío."""
    import os
    ruta = "data/raw_pdfs/presupuesto_1964.pdf"
    assert os.path.exists(ruta), "PDF no descargado"
    assert os.path.getsize(ruta) > 100_000, "PDF sospechosamente pequeño — puede estar corrupto"

def test_ocr_exactamente_15_paginas():
    """OCR procesa exactamente 15 páginas, ni más ni menos."""
    resultados = procesar_ocr_paginas_1964(paginas=[...])  # lista de 15 índices
    assert len(resultados) == 15, f"Se procesaron {len(resultados)} páginas, se esperaban 15"

def test_ocr_output_no_vacio():
    """Ninguna de las 15 páginas devuelve texto vacío (fallo silencioso de OCR)."""
    resultados = procesar_ocr_paginas_1964(paginas=[...])
    for i, texto in enumerate(resultados):
        assert len(texto.strip()) > 50, f"⚠️ Página {i} devolvió texto muy corto — posible fallo OCR"

def test_csv_1964_estructura():
    """El CSV histórico tiene columnas mínimas y filas suficientes."""
    import pandas as pd
    df = pd.read_csv("data/processed/historical_1964.csv")
    assert len(df) >= 10, "Muy pocas filas extraídas del OCR — revisar parser"
    assert df.isnull().mean().max() < 0.5, "⚠️ Más del 50% de nulos en alguna columna — OCR mal parseado"

def test_analytical_engine_1964():
    """Las funciones de resumen 1964 devuelven resultados numéricos válidos."""
    from src.analytical_engine import resumir_1964
    resultado = resumir_1964()
    assert "total_categorias" in resultado
    assert resultado["total_categorias"] > 0
```

> ℹ️ **Nota sobre data balanceada:** Para el track 1964 no aplica balanceo (no hay modelo ML), pero sí aplica verificar que el OCR no extraiga texto vacío de páginas difíciles — eso es el `test_ocr_output_no_vacio`.

---

## 👤 Persona 3 — Skills + Streamlit + README

**Entregables:** `.claude/skills/executor_skill.json`, `.claude/skills/evaluator_skill.json`, `app.py`, `src/utils.py`, `README.md`, `requirements.txt`

### Pasos

**Día 8-9 (no depende de nadie todavía):**

- Branch `feature/executor-dashboard-draft` → `executor_skill.json` con soporte para args CLI tipo `period 2025-12`
- `evaluator_skill.json`: verifica agregaciones, aplica `@st.cache_data`, corrige errores, genera markdown de bugs
- `src/utils.py` con helpers de logging
- `README.md` y `requirements.txt` (incluir `paddleocr`, `streamlit`, `fastmcp`, `pandas`, `plotly`)

**Día 10-11 (una vez que lleguen los `data/processed/` de P1 y P2):**

- Branch `feature/evaluator-qa-refinement` → construir `app.py` con los 4 tabs:
  - **Tab 1:** KPIs 2025 (`st.metric`) + sección 1964 independiente con texto OCR + 2 gráficos históricos
  - **Tab 2:** Mapa/heatmap departamentos 2025
  - **Tab 3:** Tabla interactiva peores ejecutores PIM > 10M
  - **Tab 4:** Log del evaluator + playground para cambiar período
- PR a main

**Día 12:** Buffer debugging + grabar segmento video (demo live de los 4 tabs)

### 🧪 Smoke Tests

```python
# tests/test_app.py

def test_processed_files_existen_antes_de_streamlit():
    """Los archivos que lee app.py existen antes de lanzar la app."""
    import os
    assert os.path.exists("data/processed/presupuesto_2025.parquet"), "Falta processed 2025"
    assert os.path.exists("data/processed/historical_1964.csv"), "Falta processed 1964"

def test_app_importa_sin_errores():
    """app.py se puede importar sin que explote (detecta errores de sintaxis y dependencias)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("app", "app.py")
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        assert False, f"app.py falla al importar: {e}"

def test_sin_division_por_cero_en_avance():
    """El cálculo de Avance% en app.py maneja PIM=0 sin romper la app."""
    import pandas as pd
    df = pd.DataFrame({"PIM": [0, 100, 200], "DEVENGADO": [0, 50, 180]})
    df["Avance"] = df.apply(
        lambda r: (r["DEVENGADO"] / r["PIM"] * 100) if r["PIM"] > 0 else 0, axis=1
    )
    assert df["Avance"].isnull().sum() == 0, "División por cero no manejada"

def test_skill_jsons_validos():
    """Los archivos JSON de skills son válidos y tienen los campos mínimos."""
    import json
    for skill in ["executor_skill.json", "evaluator_skill.json"]:
        with open(f".claude/skills/{skill}") as f:
            data = json.load(f)
        assert "name" in data, f"{skill} no tiene campo 'name'"
        assert "prompt" in data or "description" in data, f"{skill} sin prompt/description"
```

---

## 📅 Timeline general

| Día | P1                                            | P2                               | P3                   |
| ---- | --------------------------------------------- | -------------------------------- | -------------------- |
| 8-9  | MCP server + conexión CKAN                   | OCR 15 páginas                  | Skill JSONs + README |
| 10   | ⚠️ Entrega `processed/` 2025              | ⚠️ Entrega `processed/` 1964 | `app.py` arranca   |
| 11   | Buffer / debug + smoke tests                  | Buffer / debug + smoke tests     | `app.py` termina   |
| 12   | 🎥 Video slides 1-2                           | 🎥 Video slides 3-4              | 🎥 Video demo live   |
| 13   | Edición conjunta del video + revisión final |                                  |                      |
| 14   | **Entrega 11:59 PM** 🚀                 |                                  |                      |

---

## ⚠️ Reglas de oro

1. **Nunca subir datos crudos al contexto del LLM.** Todo lo pesado va a `data/processed/` primero mediante scripts locales.
2. **Nunca commitear directamente a `main`.** Todo por branches + PR.
3. **Correr los smoke tests antes de hacer el PR** — si alguno falla, no se mergea.
4. **Día 10 es el día crítico:** P1 y P2 deben entregar sus `data/processed/` sí o sí para que P3 no se bloquee.
