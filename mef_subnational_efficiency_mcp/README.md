# MEF Subnational Efficiency MCP

Proyecto HW5 para construir un pipeline local multi-agente de auditoria de gasto publico peruano, usando MCP, Skills, procesamiento local de datos 2025, OCR historico 1964 y dashboard Streamlit.

## Estructura

```text
app.py
requirements.txt
.claude/skills/
src/
data/raw_pdfs/
data/snapshots/
data/processed/
docs/reportes/
video/link.txt
```

## Flujo esperado

1. Persona 1 implementa MCP y genera datos 2025 reducidos en `data/processed/`.
2. Persona 2 ejecuta OCR sobre exactamente 15 paginas del PDF 1964 y genera `historical_1964.csv`.
3. Persona 3 conecta Skills, dashboard Streamlit, QA, README final y video.

## Reglas criticas

- Nunca cargar datasets crudos completos al contexto del LLM.
- Usar snapshots de 5 a 10 filas para inspeccion de schema.
- Procesar datos pesados con scripts locales.
- Mantener 2025 y 1964 como tracks independientes.
- Trabajar siempre en ramas feature y abrir PR.

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecucion

```bash
streamlit run app.py
```

## Pendiente

Completar esta documentacion con comandos reales cuando los scripts esten implementados.
