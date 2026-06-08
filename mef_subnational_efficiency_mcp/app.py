"""Streamlit dashboard entrypoint.

This scaffold keeps the final file name stable for the team. Persona 3 should
replace placeholder content after Persona 1 and Persona 2 publish processed data.
"""

from pathlib import Path


try:
    import streamlit as st
except ModuleNotFoundError:  # Allows smoke import before dependencies are installed.
    st = None


PROJECT_ROOT = Path(__file__).resolve().parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_PATH = PROJECT_ROOT / "docs" / "evaluator_report.md"


def main() -> None:
    if st is None:
        print("Streamlit is not installed. Run: pip install -r requirements.txt")
        return

    st.set_page_config(
        page_title="MEF Subnational Efficiency MCP",
        page_icon="",
        layout="wide",
    )

    st.title("MEF Subnational Efficiency MCP")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Executive Summary",
            "Territorial Analysis",
            "Anomaly Explorer",
            "Audit Log",
        ]
    )

    with tab1:
        st.header("2025 and 1964 Independent Summaries")
        st.info("TODO: Persona 3 conecta KPIs 2025 y graficos historicos 1964.")

    with tab2:
        st.header("2025 Territorial Distribution")
        st.info("TODO: Persona 3 conecta mapas y heatmaps 2025.")

    with tab3:
        st.header("2025 Worst Executing Units")
        st.info("TODO: Persona 3 conecta tabla interactiva PIM > 10M.")

    with tab4:
        st.header("Evaluator Audit Log and Period Playground")
        st.info("TODO: Persona 3 conecta reporte del evaluator y selector de periodo.")


if __name__ == "__main__":
    main()
