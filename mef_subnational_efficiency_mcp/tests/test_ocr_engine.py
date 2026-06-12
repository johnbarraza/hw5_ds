import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import ocr_engine as oe  # noqa: E402

PAGINAS_1964 = [38, 100, 190, 226, 272, 358, 421, 532, 644, 854, 1003, 1031, 1037, 1066, 1068]


def test_pdf_descargado():
    assert oe.PDF_PATH.exists(), "PDF no descargado"
    assert oe.PDF_PATH.stat().st_size > 100_000, "PDF sospechosamente pequeno"


def test_ocr_exactamente_15_paginas():
    resultados = oe.procesar_ocr_paginas_1964(PAGINAS_1964)
    assert len(resultados) == 15, f"Se procesaron {len(resultados)} paginas, se esperaban 15"


def test_ocr_output_no_vacio():
    resultados = oe.procesar_ocr_paginas_1964(PAGINAS_1964)
    for r in resultados:
        assert len(r["text"].strip()) > 50, f"Pagina {r['page_number']} con texto muy corto"


def test_csv_1964_estructura():
    df = pd.read_csv(oe.OUTPUT_PATH)
    assert len(df) >= 10, "Muy pocas filas extraidas del OCR"
    assert df.isnull().mean().max() < 0.5, "Mas del 50% de nulos en alguna columna"
    expected_cols = {
        "page_number", "source_line", "category", "concept",
        "amount_raw", "amount_numeric", "parser_confidence",
    }
    assert expected_cols.issubset(df.columns)
    assert df["page_number"].nunique() == 15


def test_ocr_quality_csv():
    df = pd.read_csv(oe.QUALITY_PATH)
    assert len(df) == 15
    assert (df["line_count"] > 0).all(), "Pagina con cero lineas extraidas"
    expected_cols = {
        "page_number", "line_count", "numeric_token_count",
        "avg_confidence", "low_confidence_count", "manual_review_required",
    }
    assert expected_cols.issubset(df.columns)
