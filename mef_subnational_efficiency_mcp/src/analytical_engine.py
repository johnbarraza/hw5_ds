"""Shared analytical functions for processed 2025 and 1964 data.

Persona 2 owns this module, with Persona 3 consuming it from app.py.
Reads exclusively from data/processed/ — never touches raw sources.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PRESUPUESTO_2025_PATH = PROCESSED_DIR / "presupuesto_2025.parquet"
HISTORICAL_1964_PATH = PROCESSED_DIR / "historical_1964.csv"
OCR_QUALITY_1964_PATH = PROCESSED_DIR / "ocr_quality_1964.csv"

# 1964 category labels that are OCR-fragmented restatements of the same
# EGRESOS/INGRESOS grand totals on page 1066 (see resumir_1964).
_REDUNDANT_TOTAL_LABELS = {
    "TOTAL GENERAL DE LOS EGRESOS",
    "TOTAL DE LOS EGRESOS",
    "TOTAL GENERAL DE LOS INGRESOS",
    "TOTAL DE LOS INGRESOS",
}


def _load_2025() -> pd.DataFrame:
    if not PRESUPUESTO_2025_PATH.exists():
        raise FileNotFoundError(f"Missing {PRESUPUESTO_2025_PATH}; run data_pipeline.py first.")
    return pd.read_parquet(PRESUPUESTO_2025_PATH)


def calcular_metricas_2025() -> dict:
    """Aggregate 2025 execution metrics nationally, by department and government level."""
    df = _load_2025()

    total_pim = float(df["PIM_2025"].sum())
    total_devengado = float(df["DEVENGADO_2025"].sum())
    avance_nacional = (total_devengado / total_pim * 100) if total_pim > 0 else 0.0

    cols = ["PIM_2025", "DEVENGADO_2025", "Saldo_No_Devengado"]
    por_departamento = (
        df.groupby("DEPARTAMENTO_EJECUTORA_NOMBRE")[cols].sum().round(2).to_dict(orient="index")
    )
    por_nivel_gobierno = (
        df.groupby("NIVEL_GOBIERNO_NOMBRE")[cols].sum().round(2).to_dict(orient="index")
    )

    return {
        "n_entidades": int(len(df)),
        "total_pim": round(total_pim, 2),
        "total_devengado": round(total_devengado, 2),
        "total_saldo_no_devengado": round(float(df["Saldo_No_Devengado"].sum()), 2),
        "avance_nacional": round(avance_nacional, 2),
        "por_departamento": por_departamento,
        "por_nivel_gobierno": por_nivel_gobierno,
    }


def top_peores_ejecutores_2025(limit: int = 20) -> pd.DataFrame:
    """Return executing units (PIM > 1M, already filtered upstream) sorted by lowest Avance%."""
    df = _load_2025()
    return df.sort_values("Avance", ascending=True).head(limit).reset_index(drop=True)


def resumir_1964(top_n: int = 10) -> dict:
    """Summarize the OCR-extracted 1964 historical record: categories, amounts and OCR quality."""
    if not HISTORICAL_1964_PATH.exists():
        raise FileNotFoundError(
            f"Missing {HISTORICAL_1964_PATH}; run exportar_historical_1964 first."
        )

    df = pd.read_csv(HISTORICAL_1964_PATH)

    categorias = sorted(df["category"].dropna().unique().tolist())
    montos = pd.to_numeric(df["amount_numeric"], errors="coerce").dropna()

    distribucion_categoria = (
        df.assign(amount_numeric=pd.to_numeric(df["amount_numeric"], errors="coerce"))
        .dropna(subset=["amount_numeric"])
        .groupby("category")["amount_numeric"]
        .sum()
    )

    # Page 1066 ("Operaciones Realizadas") restates the EGRESOS/INGRESOS grand
    # totals under near-duplicate header labels (OCR-fragmented variants of
    # the same total line, e.g. "TOTAL GENERAL DE LOS EGRESOS" vs "TOTAL DE
    # LOS EGRESOS"). Drop them from the chart-facing distribution so the same
    # grand total isn't counted 2-3x in the category breakdown; the raw
    # per-label totals stay in distribucion_por_categoria for traceability.
    distribucion_grafico = distribucion_categoria.drop(
        labels=[c for c in _REDUNDANT_TOTAL_LABELS if c in distribucion_categoria.index]
    )
    total_monto = float(distribucion_grafico.sum())
    distribucion_pct = (
        (distribucion_grafico / total_monto * 100).round(2).to_dict() if total_monto > 0 else {}
    )
    top_categorias_monto = {
        k: round(v, 2) for k, v in distribucion_grafico.sort_values(ascending=False).head(top_n).to_dict().items()
    }

    resultado = {
        "total_paginas": int(df["page_number"].nunique()),
        "total_categorias": len(categorias),
        "categorias": categorias,
        "total_lineas": int(len(df)),
        "total_montos": int(montos.count()),
        "distribucion_por_categoria": {k: round(v, 2) for k, v in distribucion_categoria.to_dict().items()},
        "distribucion_porcentual_categoria": distribucion_pct,
        "top_categorias_monto": top_categorias_monto,
    }

    if OCR_QUALITY_1964_PATH.exists():
        quality = pd.read_csv(OCR_QUALITY_1964_PATH)
        resultado["calidad_ocr"] = {
            "paginas_procesadas": int(len(quality)),
            "lineas_extraidas_total": int(quality["line_count"].sum()),
            "avg_confidence_promedio": round(float(quality["avg_confidence"].mean()), 4),
            "paginas_revision_manual": int(quality["manual_review_required"].sum()),
            "porcentaje_revision_manual": round(
                float(quality["manual_review_required"].mean() * 100), 2
            ),
            "por_pagina": quality.sort_values("page_number")[
                ["page_number", "avg_confidence", "manual_review_required"]
            ].to_dict(orient="records"),
        }

    return resultado
