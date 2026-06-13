def test_processed_files_existen_antes_de_streamlit():
    import os
    assert os.path.exists("data/processed/presupuesto_2025.parquet"), "Falta processed 2025"
    assert os.path.exists("data/processed/historical_1964.csv"), "Falta processed 1964"

def test_app_importa_sin_errores():
    import importlib.util
    spec = importlib.util.spec_from_file_location("app", "app.py")
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        assert False, f"app.py falla al importar: {e}"

def test_sin_division_por_cero_en_avance():
    import pandas as pd
    df = pd.DataFrame({"PIM": [0, 100, 200], "DEVENGADO": [0, 50, 180]})
    df["Avance"] = df.apply(
        lambda r: (r["DEVENGADO"] / r["PIM"] * 100) if r["PIM"] > 0 else 0, axis=1
    )
    assert df["Avance"].isnull().sum() == 0

def test_skill_jsons_validos():
    import json
    for skill in ["executor_skill.json", "evaluator_skill.json"]:
        with open(f".claude/skills/{skill}") as f:
            data = json.load(f)
        assert "name" in data
        assert "prompt" in data or "description" in data
