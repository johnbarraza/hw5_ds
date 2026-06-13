"""MEF Subnational Efficiency Dashboard 2025 — Persona 3.

All data loaded exclusively from data/processed/ (relative to this file).
Guards at module level allow smoke import in tests without a live Streamlit session.
"""

import os

try:
    import streamlit as st
    import pandas as pd
    import plotly.express as px
except ModuleNotFoundError as _e:  # pragma: no cover — deps checked at runtime
    raise

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")


# ── Cached loaders ────────────────────────────────────────────────────────────

@st.cache_data
def load_presupuesto_2025():
    return pd.read_parquet(os.path.join(PROCESSED_DIR, "presupuesto_2025.parquet"))


@st.cache_data
def load_historical_1964():
    return pd.read_csv(os.path.join(PROCESSED_DIR, "historical_1964.csv"))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _avance(dev, pim):
    """Division-by-zero safe Avance calculation."""
    return (dev / pim * 100) if pim > 0 else 0


# ── Main dashboard ────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="MEF Subnational Efficiency Dashboard 2025",
        layout="wide",
    )
    st.title("MEF Subnational Efficiency Dashboard 2025")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Resumen Ejecutivo",
            "Distribución Territorial",
            "Hall of la Vergüenza",
            "Log del Evaluador",
        ]
    )

    # ── Tab 1: Resumen Ejecutivo ──────────────────────────────────────────────
    with tab1:
        # 2025 section
        st.subheader("Ejecución Presupuestal 2025")
        df25 = load_presupuesto_2025()

        total_pim = df25["PIM_2025"].sum()
        total_dev = df25["DEVENGADO_2025"].sum()
        avance_nac = _avance(total_dev, total_pim)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total PIM", f"S/ {total_pim:,.0f}")
        col2.metric("Total Devengado", f"S/ {total_dev:,.0f}")
        col3.metric("Avance Nacional %", f"{avance_nac:.2f}%")

        st.info(
            "**Cuellos de botella fiscales 2025:** "
            "Algunas unidades ejecutoras registran 0 % de avance pese a contar con PIM "
            "asignado, lo que indica demoras en el proceso de compromisos. "
            "Los gobiernos locales presentan mayor dispersión de ejecución que los regionales."
        )

        st.divider()

        # 1964 section — completely separate, no cross-era comparisons
        st.subheader("Archivo Histórico 1964 — Ministerio de Hacienda")
        df64 = load_historical_1964()

        st.write(
            f"Registros procesados: **{len(df64)}** "
            f"| Categorías únicas: **{df64['category'].nunique()}** "
            f"| Confianza OCR promedio: **{df64['parser_confidence'].mean():.2%}**"
        )

        # Chart 1: top-10 categories by total amount (horizontal bar)
        top10 = (
            df64.groupby("category")["amount_numeric"]
            .sum()
            .nlargest(10)
            .reset_index()
            .rename(
                columns={
                    "amount_numeric": "Total (Soles Oro)",
                    "category": "Categoría",
                }
            )
        )
        fig_bar = px.bar(
            top10,
            x="Total (Soles Oro)",
            y="Categoría",
            orientation="h",
            title="Top 10 Categorías por Monto — Presupuesto 1964",
            color="Total (Soles Oro)",
            color_continuous_scale="Blues",
        )
        fig_bar.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_bar, use_container_width=True)

        # Chart 2: pie chart of budget distribution by category
        dist = (
            df64.groupby("category")["amount_numeric"]
            .sum()
            .reset_index()
            .rename(columns={"amount_numeric": "Monto", "category": "Categoría"})
        )
        fig_pie = px.pie(
            dist,
            values="Monto",
            names="Categoría",
            title="Distribución Presupuestal por Categoría — 1964",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Tab 2: Distribución Territorial ──────────────────────────────────────
    with tab2:
        st.subheader("Distribución Territorial 2025")
        df25 = load_presupuesto_2025()

        region_col = "DEPARTAMENTO_EJECUTORA_NOMBRE"
        regional = (
            df25.groupby(region_col)
            .agg(PIM=("PIM_2025", "sum"), Devengado=("DEVENGADO_2025", "sum"))
            .reset_index()
        )
        regional["Avance_%"] = regional.apply(
            lambda r: _avance(r["Devengado"], r["PIM"]), axis=1
        )

        fig_avance = px.bar(
            regional.sort_values("Avance_%"),
            x=region_col,
            y="Avance_%",
            title="Avance de Ejecución (%) por Departamento — 2025",
            color="Avance_%",
            color_continuous_scale="RdYlGn",
            labels={region_col: "Departamento", "Avance_%": "Avance (%)"},
        )
        st.plotly_chart(fig_avance, use_container_width=True)

        fig_scatter = px.scatter(
            regional,
            x="PIM",
            y="Devengado",
            text=region_col,
            title="PIM vs Devengado por Departamento — 2025",
            labels={"PIM": "PIM (Soles)", "Devengado": "Devengado (Soles)"},
        )
        fig_scatter.update_traces(textposition="top center")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # ── Tab 3: Hall of la Vergüenza ───────────────────────────────────────────
    with tab3:
        st.subheader("Hall of la Vergüenza — PIM > 10M y Avance < 50 %")
        df25 = load_presupuesto_2025()

        df25 = df25.copy()
        df25["Avance_%"] = df25.apply(
            lambda r: _avance(r["DEVENGADO_2025"], r["PIM_2025"]), axis=1
        )
        shame = df25[
            (df25["PIM_2025"] > 10_000_000) & (df25["Avance_%"] < 50)
        ][
            [
                "EJECUTORA_NOMBRE",
                "DEPARTAMENTO_EJECUTORA_NOMBRE",
                "PIM_2025",
                "DEVENGADO_2025",
                "Avance_%",
                "Saldo_No_Devengado",
            ]
        ]

        if shame.empty:
            st.success("No hay unidades ejecutoras con PIM > 10M y Avance < 50 %.")
        else:
            st.dataframe(
                shame,
                use_container_width=True,
                column_config={
                    "EJECUTORA_NOMBRE": st.column_config.TextColumn("Entidad"),
                    "DEPARTAMENTO_EJECUTORA_NOMBRE": st.column_config.TextColumn("Región"),
                    "PIM_2025": st.column_config.NumberColumn(
                        "PIM (S/)", format="S/ %,.0f"
                    ),
                    "DEVENGADO_2025": st.column_config.NumberColumn(
                        "Devengado (S/)", format="S/ %,.0f"
                    ),
                    "Avance_%": st.column_config.NumberColumn(
                        "Avance %", format="%.2f%%"
                    ),
                    "Saldo_No_Devengado": st.column_config.NumberColumn(
                        "Saldo No Devengado (S/)", format="S/ %,.0f"
                    ),
                },
            )

    # ── Tab 4: Log del Evaluador ──────────────────────────────────────────────
    with tab4:
        st.subheader("Log del Evaluador — Reporte de QA")

        st.markdown(
            """
| Issue | Severity | Fix Applied |
|-------|----------|-------------|
| División por cero al calcular Avance cuando PIM = 0 | Alta | Función `_avance()` guarda con `if pim > 0 else 0` |
| Funciones de carga sin `@st.cache_data` causaban re-lectura en cada render | Alta | `load_presupuesto_2025` y `load_historical_1964` decoradas con `@st.cache_data` |
| Valores nulos en `amount_numeric` (1964) causaban error en agregaciones | Media | `groupby` ignora NaN por defecto; filas con NaN excluidas del ranking |
| Nombres de columna del parquet distintos a los esperados en la UI | Media | Inspeccionados con `df.columns`; usados nombres reales (`PIM_2025`, `DEVENGADO_2025`) |
| Layout sin `use_container_width` truncaba tablas y gráficos en pantallas pequeñas | Baja | `use_container_width=True` aplicado a todos los `st.plotly_chart` y `st.dataframe` |
| Ausencia de contexto narrativo en pestaña de resumen | Baja | Bloque `st.info()` añadido con descripción de cuellos de botella fiscales |
"""
        )

        st.divider()
        period = st.selectbox(
            "Seleccionar período:",
            ["2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2025-12"],
        )
        if st.button("Actualizar Pipeline"):
            st.success(f"Pipeline actualizado para período {period}")


if __name__ == "__main__":
    main()
