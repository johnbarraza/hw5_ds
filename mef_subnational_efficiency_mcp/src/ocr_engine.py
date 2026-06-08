"""PaddleOCR pipeline for the 1964 historical fiscal archive.

Persona 2 owns the implementation.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = PROJECT_ROOT / "data" / "raw_pdfs" / "presupuesto_1964.pdf"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "historical_1964.csv"


def descargar_documento_1964() -> Path:
    raise NotImplementedError("Persona 2: download the 1964 PDF to data/raw_pdfs/.")


def procesar_ocr_paginas_1964(paginas: list[int]):
    if len(paginas) != 15:
        raise ValueError("The OCR pipeline must process exactly 15 pages.")
    raise NotImplementedError("Persona 2: run PaddleOCR on the selected pages.")


def exportar_historical_1964(paginas: list[int]) -> Path:
    raise NotImplementedError("Persona 2: write parsed OCR output to historical_1964.csv.")
