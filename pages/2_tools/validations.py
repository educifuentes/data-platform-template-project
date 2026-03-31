import streamlit as st

from tests.test_clientes import validate_clientes
from tests.test_censos import validate_censos, df as censos_df
from tests.test_bases_ccu import validate_bases_ccu, df as bases_df

# --- Page Config & Header ---
st.set_page_config(page_title="Validaciones", layout="wide")
st.title(":material/fact_check: Validaciones")
st.markdown("Chequeos automáticos sobre las tablas fuente para asegurar la integridad de los reportes.")

# --- Tab Layout ---
tab1, tab2, tab3 = st.tabs([
    ":material/sports_bar: Clientes",
    ":material/checklist_rtl: Censos",
    ":material/assignment: Bases CCU"
])

with tab1:
    validate_clientes()

with tab2:
    periodos_censos = sorted(censos_df["periodo"].dropna().unique(), reverse=True)
    selected_periodo_censos = st.selectbox(
        "Filtrar por periodo",
        options=["Todos"] + list(periodos_censos),
        key="periodo_censos",
    )
    validate_censos(periodo=selected_periodo_censos if selected_periodo_censos != "Todos" else None)

with tab3:
    periodos_bases = sorted(bases_df["periodo"].dropna().unique(), reverse=True)
    selected_periodo_bases = st.selectbox(
        "Filtrar por periodo",
        options=["Todos"] + list(periodos_bases),
        key="periodo_bases",
    )
    validate_bases_ccu(periodo=selected_periodo_bases if selected_periodo_bases != "Todos" else None)
