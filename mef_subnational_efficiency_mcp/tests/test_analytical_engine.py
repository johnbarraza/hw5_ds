import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import analytical_engine as ae  # noqa: E402


def test_calcular_metricas_2025():
    metricas = ae.calcular_metricas_2025()
    assert metricas["total_pim"] > 0
    assert 0 <= metricas["avance_nacional"] <= 100
    assert metricas["n_entidades"] > 0


def test_top_peores_ejecutores_2025():
    df = ae.top_peores_ejecutores_2025(limit=5)
    assert "Avance" in df.columns
    assert df["Avance"].is_monotonic_increasing
    assert (df["PIM_2025"] >= 10_000_000).all()


def test_resumir_1964():
    resultado = ae.resumir_1964()
    assert "total_categorias" in resultado
    assert resultado["total_categorias"] > 0
    assert resultado["total_paginas"] == 15
    assert resultado["total_montos"] > 0
    assert "calidad_ocr" in resultado
