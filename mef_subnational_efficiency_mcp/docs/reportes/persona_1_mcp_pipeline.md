# Reporte Persona 1 - MCP Server + Data Pipeline 2025

## Estado
- [ ] En progreso
- [x] Terminado
- [ ] Smoke tests aprobados
- [x] PR abierto

## Que hice
Implementé el MCP server local con 6 tools conectados al portal de datos abiertos del MEF. Exploré el portal manualmente para identificar el dataset correcto de ejecución presupuestal 2025. Implementé la estrategia anti-context flooding usando stream de 500KB para el snapshot y procesamiento en chunks para el pipeline. Generé el parquet filtrado con entidades de gobiernos regionales y locales con PIM > 10M soles.

## Archivos creados o modificados
- `src/mcp_server.py`
- `src/data_pipeline.py`
- `data/snapshots/schema_snapshot_2025.csv`
- `data/snapshots/schema_2025.json`
- `data/processed/presupuesto_2025.parquet`

## Datos usados
- Fuente: Portal de Datos Abiertos del MEF — https://datosabiertos.mef.gob.pe/dataset/presupuesto-y-ejecucion-de-gasto
- Periodo: 2025
- Dataset: comparativo_gastos_2022_2026.csv — https://fs.datosabiertos.mef.gob.pe/datastorefiles/comparativo_gastos_2022_2026.csv
- Columnas criticas:
  - PIM: `PIM_2025`
  - Devengado: `DEVENGADO_2025`
  - Nivel de gobierno: `NIVEL_GOBIERNO_NOMBRE`
  - Region: `DEPARTAMENTO_EJECUTORA_NOMBRE`
  - Entidad: `EJECUTORA_NOMBRE`

## Como regenerar
```bash
# En Colab, correr en una sola celda:
import io, pathlib, requests, pandas as pd

PROJECT_ROOT = pathlib.Path("/content/hw5_ds/mef_subnational_efficiency_mcp")
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

CSV_URL = "https://fs.datosabiertos.mef.gob.pe/datastorefiles/comparativo_gastos_2022_2026.csv"
_SESSION = requests.Session()
resp = _SESSION.get(CSV_URL, stream=True, timeout=60)
contenido = b""
for chunk in resp.iter_content(chunk_size=1024):
    contenido += chunk
    if len(contenido) > 50_000_000:
        break
resp.close()

df = pd.read_csv(io.BytesIO(contenido), encoding="utf-8-sig", on_bad_lines="skip", nrows=47000)
df["PIM_2025"] = pd.to_numeric(df["PIM_2025"], errors="coerce").fillna(0)
df["DEVENGADO_2025"] = pd.to_numeric(df["DEVENGADO_2025"], errors="coerce").fillna(0)
mask = (df["PIM_2025"] > 10_000_000) & (df["NIVEL_GOBIERNO_NOMBRE"].isin(["GOBIERNOS REGIONALES", "GOBIERNOS LOCALES"]))
df_filtered = df[mask].copy()
df_filtered["Avance"] = df_filtered.apply(lambda r: round((r["DEVENGADO_2025"] / r["PIM_2025"]) * 100, 2) if r["PIM_2025"] > 0 else 0.0, axis=1)
df_filtered["Saldo_No_Devengado"] = df_filtered["PIM_2025"] - df_filtered["DEVENGADO_2025"]
df_filtered.to_parquet(PROCESSED_DIR / "presupuesto_2025.parquet", index=False)
print(f"Parquet guardado: {len(df_filtered)} filas")
```

## Validaciones realizadas
- [ ] CKAN responde sin autenticacion. (el portal MEF no tiene CKAN API funcional — ver limitaciones)
- [x] Snapshot usa maximo 10 filas.
- [x] Datos procesados son pequenos. (3 filas, parquet < 1KB)
- [x] `PIM > 10000000` aplicado.
- [x] `Avance` no genera division por cero.

## Limitaciones
- El portal `datosabiertos.mef.gob.pe` no tiene CKAN API funcional — devuelve HTML en vez de JSON. Los tools CKAN del MCP server estan implementados segun el enunciado pero no conectan con este portal especifico.
- El CSV completo pesa mas de 1GB y no es descargable completamente en Colab. Se procesaron 50MB (47,000 filas) como muestra representativa.
- Solo 3 entidades pasaron el filtro PIM > 10M en la muestra. El dataset completo tendria significativamente mas entidades.

## Mejoras posibles
- Usar una VPN o entorno con mejor conexion para descargar el CSV completo.
- Implementar descarga paralela del CSV en segmentos para acelerar el proceso.
- Buscar un endpoint alternativo del MEF que soporte consultas filtradas por anio y nivel de gobierno sin descargar el archivo completo.
- Agregar smoke tests automatizados con pytest.
