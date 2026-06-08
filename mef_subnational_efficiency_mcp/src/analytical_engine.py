"""Shared analytical functions for processed 2025 and 1964 data.

Persona 2 owns this module, with Persona 3 consuming it from app.py.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def calcular_metricas_2025():
    raise NotImplementedError("Persona 2: aggregate processed 2025 data.")


def top_peores_ejecutores_2025(limit: int = 20):
    raise NotImplementedError("Persona 2: return worst executors with PIM > 10M.")


def resumir_1964():
    raise NotImplementedError("Persona 2: summarize historical_1964.csv.")
