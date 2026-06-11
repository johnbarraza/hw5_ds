"""PaddleOCR pipeline for the 1964 historical fiscal archive.

Persona 2 owns the implementation.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import fitz  # PyMuPDF
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = PROJECT_ROOT / "data" / "raw_pdfs" / "presupuesto_1964.pdf"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "historical_1964.csv"
PAGES_DIR = PROJECT_ROOT / "data" / "processed" / "ocr_pages_1964"
QUALITY_PATH = PROJECT_ROOT / "data" / "processed" / "ocr_quality_1964.csv"
PAGE_SELECTION_PATH = PROJECT_ROOT / "data" / "snapshots" / "ocr_page_selection_1964.csv"

# Official 1964 source named in instrucciones_hw5.md: "Cuenta General de la
# Republica - Ano 1964" (Ministerio de Hacienda y Comercio), via the
# Fuentes Historicas del Peru portal (Google Books id 9YkbAQAAMAAJ):
# https://fuenteshistoricasdelperu.com/2021/08/12/ministerio-de-hacienda-y-comercio-presupuesto-balance-y-cuenta-general-de-la-republica/
# The portal does not expose a direct downloadable PDF URL (Google Books
# embed only), so the 1073-page PDF must be placed manually at PDF_PATH.
SOURCE_URL = "https://fuenteshistoricasdelperu.com/2021/08/12/ministerio-de-hacienda-y-comercio-presupuesto-balance-y-cuenta-general-de-la-republica/"

DPI = 300
LOW_CONFIDENCE_THRESHOLD = 0.80
MIN_CHARS_PER_PAGE = 50
MIN_NUMERIC_TOKENS = 3

_AMOUNT_PATTERN = re.compile(r"(?:S/\.?\s*)?\d[\d.,']*\d|\d", re.UNICODE)


def descargar_documento_1964() -> Path:
    """Verify the 1964 fiscal archive PDF is present at PDF_PATH.

    The official source (SOURCE_URL) is a Fuentes Historicas del Peru blog
    post embedding a Google Books viewer with no direct PDF download link,
    so the document must be downloaded manually from that page and placed
    at PDF_PATH.
    """
    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    if PDF_PATH.exists() and PDF_PATH.stat().st_size > 100_000:
        return PDF_PATH

    raise FileNotFoundError(
        f"{PDF_PATH} not found. Download the 'Cuenta General de la Republica - "
        f"Ano 1964' PDF manually from {SOURCE_URL} and place it at this path."
    )


def _render_page_image(page_number: int) -> Path:
    """Render a 1-indexed PDF page to a 300 DPI PNG, cached under ocr_pages_1964/."""
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    image_path = PAGES_DIR / f"page_{page_number:03d}.png"
    if image_path.exists():
        return image_path

    doc = fitz.open(PDF_PATH)
    try:
        zoom = DPI / 72
        matrix = fitz.Matrix(zoom, zoom)
        pixmap = doc[page_number - 1].get_pixmap(matrix=matrix)
        pixmap.save(image_path)
    finally:
        doc.close()
    return image_path


_OCR_ENGINE = None


def _get_ocr_engine():
    global _OCR_ENGINE
    if _OCR_ENGINE is None:
        from paddleocr import PaddleOCR

        _OCR_ENGINE = PaddleOCR(
            lang="es",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            enable_mkldnn=False,
        )
    return _OCR_ENGINE


def _extract_lines(results) -> list[dict]:
    """Normalize PaddleOCR output (predict() or legacy ocr() shapes) to {text, confidence}."""
    lines: list[dict] = []
    for result in results:
        if isinstance(result, dict) and "rec_texts" in result:
            texts = result["rec_texts"]
            scores = result.get("rec_scores") or [1.0] * len(texts)
            for text, score in zip(texts, scores):
                text = text.strip()
                if text:
                    lines.append({"text": text, "confidence": float(score)})
        elif isinstance(result, list):
            for item in result:
                _box, (text, score) = item
                text = text.strip()
                if text:
                    lines.append({"text": text, "confidence": float(score)})
    return lines


def _ocr_page(page_number: int) -> dict:
    """Run PaddleOCR on a single rendered page, caching raw output as JSON."""
    raw_path = PAGES_DIR / f"page_{page_number:03d}.json"
    if raw_path.exists():
        return json.loads(raw_path.read_text(encoding="utf-8"))

    image_path = _render_page_image(page_number)
    engine = _get_ocr_engine()
    results = engine.predict(str(image_path))
    lines = _extract_lines(results)

    payload = {
        "page_number": page_number,
        "text": "\n".join(line["text"] for line in lines),
        "lines": lines,
    }
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def procesar_ocr_paginas_1964(paginas: list[int]) -> list[dict]:
    """Run PaddleOCR over exactly 15 page numbers, returning per-page text and lines."""
    if len(paginas) != 15:
        raise ValueError("The OCR pipeline must process exactly 15 pages.")
    descargar_documento_1964()
    return [_ocr_page(page_number) for page_number in paginas]


def _is_header_line(text: str) -> bool:
    """Heuristic: long, mostly-uppercase lines are section/anexo titles, not data rows."""
    letters = [c for c in text if c.isalpha()]
    if len(letters) < 4:
        return False
    upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    if upper_ratio < 0.8:
        return False
    return (not any(c.isdigit() for c in text)) or len(text) > 20


def _normalize_amount(raw: str) -> float | None:
    """Parse Peruvian-style amounts (e.g. S/. 19'139,289.41 -> 19139289.41)."""
    cleaned = re.sub(r"^[S/\.>\s]*", "", raw).strip()
    cleaned = cleaned.rstrip(".")
    if not cleaned or not any(c.isdigit() for c in cleaned):
        return None

    decimal_match = re.match(r"^(.*?)([.,])(\d{1,2})$", cleaned)
    if decimal_match:
        integer_part = re.sub(r"[.,']", "", decimal_match.group(1))
        number_str = f"{integer_part}.{decimal_match.group(3)}" if integer_part else f"0.{decimal_match.group(3)}"
    else:
        number_str = re.sub(r"[.,']", "", cleaned)

    try:
        return float(number_str)
    except ValueError:
        return None


def _clean_concept(text: str) -> str:
    return re.sub(r"[.\s·]+$", "", text).strip()


def exportar_historical_1964(paginas: list[int]) -> Path:
    """Parse OCR output for the 15 selected pages into historical_1964.csv + quality report."""
    if len(paginas) != 15:
        raise ValueError("The OCR pipeline must process exactly 15 pages.")

    pages_data = procesar_ocr_paginas_1964(paginas)

    if PAGE_SELECTION_PATH.exists():
        manifest = pd.read_csv(PAGE_SELECTION_PATH).set_index("page_number")
    else:
        manifest = pd.DataFrame()

    rows: list[dict] = []
    quality_rows: list[dict] = []

    for page_data in pages_data:
        page_number = page_data["page_number"]
        lines = page_data["lines"]

        default_category = (
            str(manifest.loc[page_number, "content_type"])
            if page_number in manifest.index
            else "general"
        )
        current_category = default_category

        confidences: list[float] = []
        low_confidence_count = 0
        numeric_token_count = 0
        page_text_len = sum(len(item["text"]) for item in lines)

        for source_line, item in enumerate(lines, start=1):
            text = item["text"]
            confidence = item["confidence"]
            confidences.append(confidence)
            if confidence < LOW_CONFIDENCE_THRESHOLD:
                low_confidence_count += 1

            if _is_header_line(text):
                current_category = text.strip()
                continue

            match = None
            for match in _AMOUNT_PATTERN.finditer(text):
                pass  # keep last match (rightmost numeric token on the line)

            amount_raw = None
            amount_numeric = None
            concept_source = text
            if match and match.end() == len(text.rstrip()):
                amount_raw = match.group(0).strip()
                amount_numeric = _normalize_amount(amount_raw)
                if amount_numeric is not None:
                    numeric_token_count += 1
                concept_source = text[: match.start()]

            concept = _clean_concept(concept_source) or current_category

            rows.append(
                {
                    "page_number": page_number,
                    "source_line": source_line,
                    "category": current_category,
                    "concept": concept,
                    "amount_raw": amount_raw,
                    "amount_numeric": amount_numeric,
                    "parser_confidence": round(confidence, 4),
                }
            )

        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        manual_review = (
            page_text_len < MIN_CHARS_PER_PAGE
            or avg_confidence < LOW_CONFIDENCE_THRESHOLD
            or numeric_token_count < MIN_NUMERIC_TOKENS
        )
        quality_rows.append(
            {
                "page_number": page_number,
                "line_count": len(lines),
                "numeric_token_count": numeric_token_count,
                "avg_confidence": round(avg_confidence, 4),
                "low_confidence_count": low_confidence_count,
                "manual_review_required": manual_review,
            }
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUTPUT_PATH, index=False)
    pd.DataFrame(quality_rows).to_csv(QUALITY_PATH, index=False)
    return OUTPUT_PATH
