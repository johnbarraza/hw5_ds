"""2025 data snapshot and processing pipeline.

Persona 1 owns the implementation. This script must write small outputs only.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_DIR = PROJECT_ROOT / "data" / "snapshots"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def create_schema_snapshot(period: str = "2025") -> Path:
    raise NotImplementedError("Persona 1: write schema sample to data/snapshots/.")


def build_processed_budget(period: str = "2025") -> Path:
    raise NotImplementedError("Persona 1: write reduced 2025 output to data/processed/.")


if __name__ == "__main__":
    build_processed_budget()
