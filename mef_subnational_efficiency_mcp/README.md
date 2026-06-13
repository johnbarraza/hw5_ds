# MEF Subnational Efficiency MCP

## Project Overview

This project audits Peruvian subnational public spending efficiency using a multi-agent MCP pipeline.
It combines MEF 2025 budget execution data (SIAF) with historical 1964 records from the Ministerio
de Hacienda, processed via PaddleOCR, and surfaces insights through an interactive Streamlit dashboard.
Two data tracks — 2025 and 1964 — are kept strictly independent throughout the pipeline.

## Architecture

```
┌─────────────┐
│  MCP Server │  ← fastmcp, datosabiertos.gob.pe
└──────┬──────┘
       │
       ▼
┌───────────────┐
│ Data Pipeline │  ← SIAF 2025, PIM / Devengado by ejecutora
└──────┬────────┘
       │
       ▼
┌────────────┐
│ OCR Engine │  ← PaddleOCR on 1964 Ministerio de Hacienda PDFs
└──────┬─────┘
       │
       ▼
┌──────────────────┐
│ Analytical Engine│  ← Avance%, Saldo No Devengado, regional aggregations
└──────┬───────────┘
       │
       ▼
┌──────────────┐
│ Streamlit App│  ← 4-tab dashboard (Persona 3)
└──────────────┘
```

## Installation

```bash
pip install -r requirements.txt
```

## CLI Usage

```bash
# Run executor skill for a specific monthly period
claude "run executor_skill for period 2025-12"

# Trigger full MEF data update for Q4
claude "execute mef_update for 2025-Q4"

# Launch Streamlit dashboard
streamlit run app.py
```

## Data Sources

| Source | URL | Contents |
|--------|-----|----------|
| Datos Abiertos MEF | datosabiertos.gob.pe | SIAF 2025 budget execution (PIM, Devengado, Certificado) |
| Fuentes Históricas del Perú | fuenteshistoricasdelperu.com | 1964 Ministerio de Hacienda budget PDFs |

## Team Roles

| Persona | Responsibilities |
|---------|-----------------|
| Persona 1 | MCP Server + Data Pipeline (2025 SIAF ingestion and processing) |
| Persona 2 | OCR Engine + Analytical Engine (1964 historical PDF extraction and analysis) |
| Persona 3 | Skills + Streamlit Dashboard + README + Video |

## Known Limitations

- The 2025 parquet dataset is a reduced sample (3 rows) for demonstration; full dataset requires a complete MCP pipeline run.
- PaddleOCR accuracy on 1964 scanned documents averages ~80% confidence; manual review recommended for `parser_confidence < 0.75` rows.
- The dashboard does not connect to the SIAF real-time API; data is static from `data/processed/`.
- Cross-era (1964 vs 2025) monetary comparisons are intentionally excluded due to denomination changes (soles oro vs nuevos soles).
- The `period` CLI argument routes the data refresh path but does not re-trigger the full OCR pipeline.
