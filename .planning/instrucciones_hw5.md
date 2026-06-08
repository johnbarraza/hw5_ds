# Homework Assignment: Public Expenditure Auditing via Multi-Agent Systems, Claude Code Skills, and Local MCP

**Topic:** Applied AI Architecture / AI Engineering

**Total Score:** 20 points

* Technical Implementation: **12 points**
* Presentation Video: **8 points**

**Deadline:** Sunday — 11:59 PM

---

## Description

The goal of this assignment is to build a complete, production-grade **Local Multi-Agent Analytics Pipeline** that interfaces directly with the Peruvian Open Data Portal (`datosabiertos.gob.pe`). You will build a localized architecture using **Claude Code (CLI) Skills** and the **Model Context Protocol (MCP)** to process, audit, and visualize complex, high-volume public budget data from the Ministry of Economy and Finance (MEF) and the Integrated Financial Management System (SIAF) for the **Fiscal Period 2025**.

Additionally, to master advanced unstructured document parsing, your pipeline will feature an independent data-capture track using **PaddleOCR** to extract financial logs from the **1964** historical fiscal archive. You will configure a cooperative dual-agent framework consisting of an **Executor Skill** and an **Evaluator/Optimizer Skill**. Together, they will generate a highly polished, interactive **Streamlit Dashboard** that splits into a dual-era opening summary page and a deep-dive modern 2025 analytical suite.

---

## Core Project Focus: Modern Subnational Bottlenecks & 1964 Historical Digitization

Your multi-agent architecture will handle two separate, independent analytical pipelines without forcing cross-epoch numerical comparisons, as the historical and modern recording frameworks carry completely different data structures.

* **Modern Track (Fiscal Year 2025):** Identifying regional and local governments with budgets over 10 million Soles (PEN) executing less than critical fiscal thresholds, mapping spending patterns, and quantifying unspent "Frozen Capital".
* **Historical Track (Fiscal Year 1964):** Students must isolate the **1964 accounting record** from the official collection portal: [[Fuentes Históricas del Perú — Presupuesto, Balance y Cuenta General de la República](https://fuenteshistoricasdelperu.com/2021/08/12/ministerio-de-hacienda-y-comercio-presupuesto-balance-y-cuenta-general-de-la-republica/)](https://fuenteshistoricasdelperu.com/2021/08/12/ministerio-de-hacienda-y-comercio-presupuesto-balance-y-cuenta-general-de-la-republica/).
* **OCR Text Volume Rule:** The pipeline must ingest and pass **at least 15 distinct pages** of tabular or textual matrices from this 1964 document through PaddleOCR. The agent must parse this unstructured data to extract meaningful historical conclusions and build dedicated statistical visualizations.

---

## Main Objective

Build an autonomous multi-skill pipeline that:

1. Interfaces with `datosabiertos.gob.pe` via a local MCP Server to safely extract and stream 2025 budget slices.
2. Manages heavy 2025 analytics using isolated local Python data processing scripts to bypass context window saturation.
3. Ingests the 1964 *Ministerio de Hacienda* PDF, using **PaddleOCR** over a minimum of 15 selected pages to systematically reconstruct text or table arrays.
4. Co-creates an advanced 4-tab Streamlit Application where **Tab 1** presents independent opening summaries for both 2025 and 1964, while **Tabs 2, 3, and 4** focus exclusively on the 2025 subnational infrastructure logic.
5. Employs user-driven arguments via the Claude Code CLI to dynamically refresh or re-route operational reporting periods on demand.

---

## Expected Repository Structure

Create a local workspace named exactly: `mef_subnational_efficiency_mcp`

Your repository must match this exact layout:

```bash
mef_subnational_efficiency_mcp/
│
├── app.py                             # Polished 4-tab Streamlit application
├── README.md                          # Production-grade system documentation
├── requirements.txt                   # Explicit project dependencies (must include paddleocr)
│
├── .claude/                           # Claude Code skills definitions
│   └── skills/
│       ├── executor_skill.json        # Data processing and app composition engine
│       └── evaluator_skill.json       # Structural validation, UX polish, and QA engine
│
├── src/
│   ├── mcp_server.py                  # Local MCP Server script exposing tools
│   ├── data_pipeline.py               # Auto-generated lightweight local worker scripts
│   ├── ocr_engine.py                  # PaddleOCR engine parsing at least 15 pages of the 1964 document
│   ├── analytical_engine.py           # Core metric and data grouping modules
│   └── utils.py                       # Helpers and system logging
│
├── data/
│   ├── raw_pdfs/                      # Downloaded 1964 PDF document from the source URL
│   ├── snapshots/                     # Schema layouts and top-10 line samples
│   └── processed/                     # Clean 2025 data fragments and extracted 1964 dataframes
│
└── video/
    └── link.txt                       # 5-minute pitch video URL

```

---

## Required Pipeline & Architecture Rules

### 🚨 CRITICAL RULE 1: Anti-Context Flooding Strategy (No Raw Ingestion)

> **⚠️ WARNING:** It is strictly forbidden to instruct your Claude Code Skills to read or ingest entire raw CSV/JSON datasets from the State portal into the LLM context windows. These datasets easily exceed 200MB to 1GB. Attempting to feed whole files directly into the context window will break the pipeline and result in immediate penalization.
> **The Mandatory Protocol:** Your agent must use the schema inspection tool to take a minimal **Snapshot** (the first 5–10 rows) to map columns, types, and labels. It must then write an external, optimized local script (`pandas`, `polars`, or `duckdb`) to download, filter, compute aggregations, and save a microscopic footprint (e.g., an optimized Parquet or small CSV file) inside `data/processed/`. The Streamlit app will read *only* this highly reduced file.

### 🔄 CRITICAL RULE 2: Period-Driven CLI Updates

Your system must not be hardcoded to static dates or periods. It must be built as an interactive Skill executable via **Claude Code CLI** where the user controls the pipeline execution by parsing time variables.

* **Expected CLI Invocations:** `claude "run executor_skill for period 2025-12"` or `claude "execute mef_update for 2025-Q4"`.
* Upon reception, the agent must trigger its local python infrastructure, scrape the matching dataset chunk from the state portal, re-run local transformations, and update the UI data state seamlessly. Leave it strictly configured for direct runtime query routing.

---

## Recommended MCP Toolkit

Your local MCP Server can expose the following tools to Claude Code. While these tools are highly recommended for standard portal interactions, you have total freedom to augment, combine, or rewrite them to optimize agent execution:

1. `buscar_datasets`: Queries the portal using keyword strings via the CKAN native endpoint (`/api/3/action/package_search?q={query}`).
2. `obtener_detalle_dataset`: Extracts direct download URLs for data resources via dataset IDs.
3. `descargar_documento_1964`: Downloads the historical 1964 text PDF locally into `data/raw_pdfs/`.
4. `listar_entidades_publicas`: Fetches lists of active public ministries, regional configurations, and municipal codes.
5. `listar_categorias_tematicas`: Maps high-level data groups across public domains.
6. `obtener_ultimas_actualizaciones`: Feeds chronological changes or recently added data blocks to the agent.
7. `inspeccionar_esquema_csv`: Opens a partial stream of a target CSV resource to capture headers and sample rows without heavy downloads.
8. `consultar_datastore_filtrado`: Performs remote SQL-like queries directly on the server database via native datastore APIs when available.
9. `procesar_ocr_paginas_1964`: Triggers local PaddleOCR routines over at least 15 selected pages of the 1964 document to extract unstructured financial matrix blocks.
10. `descargar_y_analizar_estadisticas`: Runs light local aggregations to feed descriptive statistical summaries back to the model context.

---

## Analytical Metrics Framework

### Reference Baseline Metrics (Modern Period 2025)

Your pipeline must calculate at least these baseline financial management indicators for the modern datasets:

* **Execution Rate (Avance %):**

$$
Avance = \left( \frac{\text{Devengado}}{\text{PIM}} \right) \times 100
$$

* **Unexecuted Budget (Presupuesto Paralizado):**

$$
\text{Saldo No Devengado} = \text{PIM} - \text{Devengado}
$$

*(Where `PIM` = Presupuesto Institucional Modificado, and `Devengado` = Funds formally spent).*

### Historical Extracted Information Metrics (1964 Track)

For the 15+ pages compiled through PaddleOCR, the pipeline must compute descriptive summaries based strictly on what is written in the historical source, such as:

* Total quantified items or structural revenue/expenditure categories visible across those pages.
* Asset distribution percentages or department listings captured by the OCR line parser.

---

## Dual-Skill Collaborative Architecture

### 🧠 Skill 1: The Executor (Data Engineering & Production Engine)

This agent acts as the core worker. It reads dataset structures via MCP, handles background data extraction scripts, runs local transformations to prevent context flooding, triggers `src/ocr_engine.py` to process at least 15 pages of the 1964 file via PaddleOCR, constructs the independent statistical plots for both eras, and writes the baseline draft of the Streamlit application (`app.py`).

### ⚖️ Skill 2: The Evaluator & Optimizer (Auditor Senior & UX Master)

This agent acts as a perfectionist peer reviewer. It does **not** simply print critique text; it must actively run validation processes and modify code. Its specific tasks are:

1. **Data Inconsistency Auditing:** It must use the MCP independently to sample raw source streams and cross-verify that the Executor's aggregations haven't introduced calculation or extraction drift.
2. **Performance Optimization:** It will optimize `app.py` by forcing caching layout configurations (`@st.cache_data`) ensuring sub-second visual renders.
3. **UI/UX Master Polish:** It will inject CSS styles, handle division-by-zero layout errors, and fix plot configurations.
4. **Quality Diff Generation:** It must write a structured markdown file inside the dashboard containing a breakdown of all bugs found, optimizations completed, and structural changes introduced to elevate the application.

---

## Streamlit Application Specifications

Your final `app.py` dashboard must contain **exactly 4 tabs**, organized as follows:

### Tab 1 — Executive Macro Summary & Dual-Era Opening Dashboard

* **2025 Section:** High-level modern KPI metric blocks (`st.metric`) rendering Total 2025 PIM, Devengado, and National Execution Rate, alongside an AI Advisor narrative detailing modern fiscal bottlenecks.
* **1964 Historical Section:** A standalone historical review container displaying clear text conclusions drawn from the 15+ pages parsed via PaddleOCR. It must feature **at least 2 graphics** visualizing the extracted historical numbers, detailing exactly what those metrics meant for that specific era.
* *Note: No cross-epoch comparison formulas are allowed here; the two eras are presented as separate, independent data summaries on this opening tab.*

### Tab 2 — Territorial Distribution & Geospatial Analysis

* *Built exclusively using 2025 information.*
* Interactive geographic charts (`st.map`, `plotly`, or `altair`) illustrating 2025 spending performance across departments.
* Visual heatmaps highlighting regions where modern budget stagnation correlates with extreme social vulnerability.

### Tab 3 — The Budget "Hall of Shame" & Anomaly Explorer

* *Built exclusively using 2025 information.*
* Interactive, sortable data matrices (`st.dataframe`) showing the worst-performing 2025 executing units with budgets exceeding 10M PEN.
* Visual categorization breakdown of what specific spending lines (e.g., concrete infrastructure, machinery acquisition) are blocked.

### Tab 4 — Multi-Agent Audit Log & Live Playgrounds

* *Built exclusively using 2025 information.*
* The raw output of the **Evaluator & Optimizer Skill Report**, showcasing the evolution from the Executor’s draft to the finished app.
* An interactive playground interface enabling live switches between modern periods requested via the CLI execution.

---

## Explanatory Video & Presentation Requirements

Create a presentation video of **maximum 5 minutes**. Put the accessible video link directly inside `video/link.txt`.

> ❌ **CRITICAL WARNING:** The presentation is **NOT** a line-by-line code walkthrough. Do not record your IDE scrolling through python code or config files.
> Instead, you must use a short PowerPoint or PDF presentation presentation (**3 to 4 slides max**) to explain your technical design decisions, followed directly by showing the finished, working product live in action.

Your presentation video must comprehensively address the following two parts. Use these checklists to ensure you cover every required point:

### 📊 Part I: Technical Architecture & Skill Design (Slide-Based, 3-4 Slides Max)

This section must use your 3-4 slides to explain your high-level engineering choices without displaying raw code files.

* [ ] **Skill Construction:** Explain your logic when writing prompt templates and configuration files for both the *Executor* and *Evaluator* skills.
* [ ] **Core Architecture Innovation:** Detail what makes your multi-agent architecture innovative and how the agents cooperate dynamically.
* [ ] **PaddleOCR Pipeline for 1964 Documents:** Detail how your engine was constructed to target the 1964 text sheets. Explain your approach to processing **at least 15 pages** of low-contrast, raw scanned historical material without hitting memory caps.
* [ ] **MCP Tool Allocation:** Explain how and why you arrived at your final number of tools. What criteria did you use to isolate or separate tool responsibilities?
* [ ] **Efficiency Optimizations:** Detail the specific strategies implemented to improve extraction speed, avoid memory leaks, and minimize raw document processing latency.
* [ ] **Performance Benchmarks:** Explicitly state how long the pipeline execution takes now versus your initial baseline tests.
* [ ] **The Evaluator Impact:** Explain why the evaluation skill dramatically improves the final system output. What is the definitive operational difference between the Executor's raw layout draft and the Evaluator's verified, cached product?

### 🚀 Part II: Problem Definition, Product Demonstration & Results (Live System Showroom)

This section must showcase the actual running Streamlit application and its business/analytical implications.

* [ ] **Problem Definition:** Articulate the real-world transparency gaps, structural data isolation, and macroeconomic performance bottlenecks in modern public expenditure that your tool exposes.
* [ ] **The Product Solution:** Explain how your specific multi-agent application solves this bottleneck for an end-user (e.g., a fiscal auditor or policy analyst).
* [ ] **Results Showroom:** Walk through the 4 tabs of your live Streamlit dashboard, showing the 2025 metrics layout, the independent 1964 historical extraction panels, and the application's visual smoothness.
* [ ] **Historical Insight Interpretation:** Walk through the text conclusions and the **at least 2 graphics** derived from the 1964 document on Tab 1. Explain what that data means and how it stands as an independent historical record.
* [ ] **System Helpfulness:** Defend why this specific solution is valuable and how it transforms manual document gathering and legacy records scanning into automated, actionable intelligence.
* [ ] **System Limitations & Next Steps:** Honestly address the current limitations of your system and provide concrete, actionable suggestions for future architectural improvements.

---

## GitHub Workflow (MANDATORY)

❌ Never commit directly to the `main` branch.

✅ Build on feature-isolated development tracks.

✅ Document step-by-step progress using explicit commits.

✅ Merge code reviews solely through descriptive Pull Requests.

Example branch paths:

```bash
feature/mcp-server-core
feature/data-snapshot-pipeline
feature/historical-1964-paddle-ocr
feature/executor-dashboard-draft
feature/evaluator-qa-refinement

```

---

## Grading Rubric

### Technical Implementation — 12 points

| Criteria                                           | Description                                                                                                                   | Points |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------ |
| **Local MCP Server Architecture**            | Reliable connection, tool mapping, and safe execution of recommended/custom tools.                                            | 2 pts  |
| **Data Ingestion Engineering**               | Flawless snapshot strategy avoiding context flooding via isolated local scripts.                                              | 2 pts  |
| **1964 PaddleOCR Digitization**              | Successful parsing of at least 15 distinct pages from the 1964 historical archive to isolate unstructured data lines.         | 2 pts  |
| **Dual Skill Cooperation Workflow**          | Evident structural orchestration between Executor and Evaluator Skills within the CLI.                                        | 2 pts  |
| **Analytical Rigor & Independent Reporting** | Implementation of baseline 2025 metrics alongside independent text conclusions and 2+ graphics for the 1964 record on Tab 1.  | 2 pts  |
| **Streamlit Core Interface**                 | Flawless execution of the 4 specified tabs, ensuring Tabs 2-4 focus exclusively on 2025 information, with sub-second caching. | 2 pts  |

### Presentation Video — 8 points

| Criteria                                        | Description                                                                                                             | Points |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------ |
| **Technical Design & Pitch Presentation** | Clear explanation of architectural choices, explicit adherence to Part I & Part II checklists, and zero code scrolling. | 8 pts  |

---

## Submission Checklist

* [ ] Repository matches the exact folder structure.
* [ ] The local MCP server runs seamlessly without requiring privileged authentication for reading data.
* [ ] The system architecture implements the local script-generation strategy to completely prevent context flooding.
* [ ] Local processing loops leverage `src/ocr_engine.py` using PaddleOCR to process a minimum of 15 pages from the 1964 historical PDF.
* [ ] At least 2 distinct Skills (`.json` configurations) exist inside the `.claude/skills/` directory.
* [ ] Tab 1 of the Streamlit application independently presents the modern 2025 analysis and the 1964 historical results (featuring text conclusions and at least 2 charts).
* [ ] Tabs 2, 3, and 4 are driven exclusively by modern 2025 information.
* [ ] App loading processes leverage `@st.cache_data` decorators.
* [ ] The presentation video link is saved inside `video/link.txt` and fulfills all criteria listed under the Part I (3-4 slides checklist) and Part II presentation checklists.
* [ ] Commit history confirms the correct use of development branches and Pull Requests.
