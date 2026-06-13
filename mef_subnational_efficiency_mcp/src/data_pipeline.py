"""2025 data snapshot and processing pipeline.

Persona 1 owns the implementation. This script must write small outputs only.
"""

from __future__ import annotations

import io
import json
import os
import pathlib
import requests
import pandas as pd

PROJECT_ROOT = pathlib.Path(os.getenv("PROJECT_ROOT", "/content/hw5_ds/mef_subnational_efficiency_mcp"))
SNAPSHOT_DIR = PROJECT_ROOT / "data" / "snapshots"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

CSV_URL = os.getenv("CSV_URL", "https://fs.datosabiertos.mef.gob.pe/datastorefiles/comparativo_gastos_2022_2026.csv")
PIM_COL = "PIM_2025"
DEVENGADO_COL = "DEVENGADO_2025"
PIM_THRESHOLD = 1_000_000
NIVEL_GOB_COL = "NIVEL_GOBIERNO_NOMBRE"
NIVEL_GOB_VALUES = ["GOBIERNOS REGIONALES", "GOBIERNOS LOCALES"]
COLS_KEEP = ["EJECUTORA_NOMBRE", "DEPARTAMENTO_EJECUTORA_NOMBRE", NIVEL_GOB_COL, PIM_COL, DEVENGADO_COL]

_SESSION = requests.Session()
_SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})


def create_schema_snapshot() -> pathlib.Path:
    """Download first 500KB of CSV, read 10 rows, save schema to data/snapshots/."""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Fetching schema snapshot from {CSV_URL} ...")
    resp = _SESSION.get(CSV_URL, stream=True, timeout=60)
    resp.raise_for_status()
    contenido = b""
    for chunk in resp.iter_content(chunk_size=1024):
        contenido += chunk
        if len(contenido) > 500_000:
            break
    resp.close()
    df = pd.read_csv(io.BytesIO(contenido), encoding="utf-8-sig", on_bad_lines="skip", nrows=10)
    out_csv = SNAPSHOT_DIR / "schema_snapshot_2025.csv"
    out_json = SNAPSHOT_DIR / "schema_2025.json"
    df.to_csv(out_csv, index=False)
    schema = {
        "source": CSV_URL,
        "columns": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "key_columns": {
            "PIM": PIM_COL,
            "DEVENGADO": DEVENGADO_COL,
            "NIVEL_GOBIERNO": NIVEL_GOB_COL,
            "REGION": "DEPARTAMENTO_EJECUTORA_NOMBRE",
            "ENTIDAD": "EJECUTORA_NOMBRE"
        },
        "threshold": f"{PIM_COL} > {PIM_THRESHOLD}",
        "sample_rows": df.head(3).to_dict(orient="records"),
    }
    out_json.write_text(json.dumps(schema, ensure_ascii=False, indent=2))
    print(f"Schema snapshot guardado: {out_csv}  ({len(df)} rows x {len(df.columns)} cols)")
    return out_json


def build_processed_budget() -> pathlib.Path:
    """Filter PIM_2025 > 1M and regional/local govs, compute metrics, write Parquet."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Descargando 50MB de {CSV_URL} ...")
    resp = _SESSION.get(CSV_URL, stream=True, timeout=120)
    resp.raise_for_status()
    contenido = b""
    for chunk in resp.iter_content(chunk_size=4096):
        contenido += chunk
        if len(contenido) > 50_000_000:
            break
    resp.close()
    print(f"Descargados {len(contenido)/1_000_000:.1f} MB")

    df = pd.read_csv(io.BytesIO(contenido), encoding="utf-8-sig", on_bad_lines="skip", nrows=47000)
    print(f"Filas cargadas: {len(df)}")

    df[PIM_COL] = pd.to_numeric(df[PIM_COL], errors="coerce").fillna(0)
    df[DEVENGADO_COL] = pd.to_numeric(df[DEVENGADO_COL], errors="coerce").fillna(0)

    mask = (df[PIM_COL] > PIM_THRESHOLD) & (df[NIVEL_GOB_COL].isin(NIVEL_GOB_VALUES))
    df_filtered = df[mask].copy()
    print(f"Filas filtradas: {len(df_filtered)}")

    if df_filtered.empty:
        raise RuntimeError("Ninguna fila paso el filtro. Revisar datos.")

    df_filtered["Avance"] = df_filtered.apply(
        lambda r: round((r[DEVENGADO_COL] / r[PIM_COL]) * 100, 2) if r[PIM_COL] > 0 else 0.0,
        axis=1
    )
    df_filtered["Saldo_No_Devengado"] = df_filtered[PIM_COL] - df_filtered[DEVENGADO_COL]

    cols_final = COLS_KEEP + ["Avance", "Saldo_No_Devengado"]
    df_filtered = df_filtered[[c for c in cols_final if c in df_filtered.columns]]

    out = PROCESSED_DIR / "presupuesto_2025.parquet"
    df_filtered.to_parquet(out, index=False)
    print(f"Parquet guardado: {out}  ({len(df_filtered)} filas)")
    return out


if __name__ == "__main__":
    create_schema_snapshot()
    build_processed_budget()
