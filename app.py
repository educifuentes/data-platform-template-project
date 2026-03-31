import streamlit as st
import os

from helpers.utilities.app_version import get_app_version


# Page configuration

# Section - Reports
dashboard_page = st.Page("pages/1_reports/1_dashboard.py", title="Dashboard", icon=":material/dashboard:")

# Section - Tools
explore_page = st.Page("pages/2_tools/data_catalog.py", title="Catalog", icon=":material/search:")
validations_page = st.Page("pages/2_tools/validations.py", title="Validaciones", icon=":material/check_circle:")
documentation_page = st.Page("pages/2_tools/documentation.py", title="Documentación", icon=":material/book:")

# Navigation Logic
nav_dict = {
    "Vistas": [
        dashboard_page
    ],
    "Herramientas": [explore_page, validations_page, documentation_page],
}


# Only expose the development environment tabs locally
is_local = os.environ.get("ENVIRONMENT", "local").lower() == "local"
if is_local:
    nav_dict["Desarrollo"] = [
        st.Page("pages/3_dev/1_staging.py", title="Staging", icon=":material/dashboard:"),
        st.Page("pages/3_dev/2_intermediate.py", title="Intermediate", icon=":material/inventory_2:"),
        st.Page("pages/3_dev/3_marts.py", title="Marts", icon=":material/account_tree:"),
        st.Page("pages/3_dev/4_exposures.py", title="Exposures", icon=":material/visibility:"),
        st.Page("pages/3_dev/model_details.py", title="Model Details", icon=":material/info:")
    ]

# current page
pg = st.navigation(nav_dict)

with st.sidebar:
    if st.button("Actualizar Datos 🔄", width='stretch', help="Forzar la recarga de datos desde Google Sheets"):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    # Logo and version
    app_version = get_app_version()
    # st.image("utilities/assets/logo_gotomarket_solid.png", width='stretch')
    st.caption(f"Version: {app_version}")

pg.run()


