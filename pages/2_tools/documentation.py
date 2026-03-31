import streamlit as st
import os

from helpers.ui_components.render_docs import render_model_docs, render_metrics_docs
from helpers.ui_components.ui_icons import ICONS

st.set_page_config(page_title="Documentación", layout="wide")

st.title(f"{ICONS['documentation']} Documentación")

# Path resolution for cloud deployment
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

def get_path(relative_path):
    return os.path.join(PROJECT_ROOT, relative_path)

# Create tabs for organization
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    f"{ICONS['metrics']} Metricas",
    f"{ICONS['metrics']} Marcas",
    f"{ICONS['clientes']} Tabla - Clientes",
    f"{ICONS['censos']} Tabla - Censos",
    f"{ICONS['bases_ccu']} Tabla - Bases CCU",

])

with tab1:
    st.header("Métricas")
    fct_metricas_path = get_path("models/metrics/_metrics.yml")
    render_metrics_docs(fct_metricas_path)

with tab2:
    st.header("Marcas y sus Grupos")
    marcas_table_path = get_path("models/documentation/marcas_y_grupos.md")
    if os.path.exists(marcas_table_path):
        with open(marcas_table_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.warning(f"No se encontró el archivo de documentación de marcas en {marcas_table_path}")

with tab3:
    st.header("Clientes")

    dim_clientes_path = get_path("models/marts/dim_clientes.yml")
    render_model_docs(dim_clientes_path)

with tab4:  
    st.header("Censos")
    fct_censos_path = get_path("models/marts/fct_censos.yml")
    render_model_docs(fct_censos_path)

with tab5:
    st.header("Bases CCU")
    fct_bases_ccu_path = get_path("models/marts/fct_bases_ccu.yml")
    render_model_docs(fct_bases_ccu_path)



