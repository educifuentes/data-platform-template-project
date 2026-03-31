import streamlit as st
import pandas as pd

from models.marts.gsheets._dim_clientes_gsheets import dim_clientes_gsheets

from helpers.ui_components.ui_components import render_troubled_rows
from helpers.ui_components.ui_icons import ICONS
from helpers.constants.gsheets_ids import SHEETS_IDS

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
df = dim_clientes_gsheets()


def validate_clientes():
    st.header("Clientes")

    total_filas = len(df)
    if total_filas == 0:
        st.warning("La tabla Dim Clientes está vacía.")
        return

    # 1. cliente_id
    st.markdown("### 1. `cliente_id`")

    nulos_id = df[df["cliente_id"].isna()]
    if not nulos_id.empty:
        st.error(f"{ICONS['close']} Detectados {len(nulos_id)} clientes sin ID (None o en Blanco)")
        render_troubled_rows(nulos_id[["cliente_id", "razon_social", "fuente", "row_index"]], source="gsheets", gid=SHEETS_IDS["clientes"])
    else:
        st.success(f"{ICONS['check']} Todos los clientes tienen ID")

    non_numeric = df[pd.to_numeric(df["cliente_id"], errors="coerce").isna() & df["cliente_id"].notna()]
    if not non_numeric.empty:
        st.error(f"{ICONS['close']} Detectados {len(non_numeric)} IDs que no se pueden convertir a número")
        render_troubled_rows(
            non_numeric[["cliente_id", "razon_social", "row_index"]], source="gsheets", gid=SHEETS_IDS["clientes"])

    non_null_df = df[df["cliente_id"].notna()]
    total_non_null = len(non_null_df)
    ids_unicos = non_null_df["cliente_id"].nunique()

    if ids_unicos == total_non_null:
        st.success(f"{ICONS['check']} IDs únicos ({total_non_null} registros con ID)")
    else:
        st.error(f"{ICONS['close']} Se detectaron {total_non_null - ids_unicos} IDs duplicados")
        dupes = non_null_df[non_null_df.duplicated("cliente_id", keep=False)].sort_values("cliente_id")
        render_troubled_rows(dupes[["cliente_id", "razon_social", "row_index"]], source="gsheets", gid=SHEETS_IDS["clientes"])

    # 2. Razón Social
    st.markdown("### 2. `razon_social`")

    nulos_rs = df[df["razon_social"].isna()]
    if not nulos_rs.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_rs)} clientes sin Razón Social")
        render_troubled_rows(nulos_rs[["cliente_id", "razon_social", "row_index"]], source="gsheets", gid=SHEETS_IDS["clientes"])
    else:
        st.success(f"{ICONS['check']} Todos los clientes tienen Razón Social")

    non_null_rs = df[df["razon_social"].notna()]
    dupes_rs = non_null_rs[non_null_rs.duplicated("razon_social", keep=False)].sort_values("razon_social")
    if not dupes_rs.empty:
        st.warning(f"{ICONS['warning']} Se detectaron {len(dupes_rs)} filas con Razón Social compartida")
        render_troubled_rows(dupes_rs[["cliente_id", "razon_social", "rut", "fuente", "row_index"]], source="gsheets", gid=SHEETS_IDS["clientes"])
    else:
        st.success(f"{ICONS['check']} No se encontraron Razones Sociales duplicadas")

    # 3. RUT
    st.markdown("### 3. `rut`")
    nulos_rut = df[df["rut"].isna()]
    if not nulos_rut.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_rut)} clientes sin RUT")
        render_troubled_rows(nulos_rut[["cliente_id", "razon_social", "rut", "row_index"]], source="gsheets", gid=SHEETS_IDS["clientes"])
    else:
        st.success(f"{ICONS['check']} Todos los clientes tienen RUT")

    # 4. Dirección
    st.markdown("### 4. `direccion`")
    nulos_dir = df[df["direccion"].isna()]
    if not nulos_dir.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_dir)} clientes sin Dirección")
        render_troubled_rows(nulos_dir[["cliente_id", "razon_social", "direccion", "row_index"]], source="gsheets", gid=SHEETS_IDS["clientes"])
    else:
        st.success(f"{ICONS['check']} Todos los clientes tienen Dirección")

    non_null_dir = df[df["direccion"].notna()].copy()
    non_null_dir["direccion_std"] = (
        non_null_dir["direccion"].astype(str).str.lower().str.strip().str.replace(r"\s+", " ", regex=True)
    )
    dupes_dir = non_null_dir[non_null_dir.duplicated("direccion_std", keep=False)].sort_values("direccion_std")
    if not dupes_dir.empty:
        st.warning(f"{ICONS['warning']} Se detectaron {len(dupes_dir)} filas con Dirección duplicada")
        render_troubled_rows(dupes_dir[["cliente_id", "razon_social", "direccion", "row_index"]], source="gsheets", gid=SHEETS_IDS["clientes"])
    else:
        st.success(f"{ICONS['check']} No se encontraron Direcciones duplicadas")

    # 5. Región
    st.markdown("### 5. `region`")
    nulos_reg = df[df["region"].isna()]
    if not nulos_reg.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_reg)} clientes sin Región")
        render_troubled_rows(nulos_reg[["cliente_id", "razon_social", "region", "row_index"]], source="gsheets", gid=SHEETS_IDS["clientes"])
    else:
        st.success(f"{ICONS['check']} Todos los clientes tienen Región")

    # 6. Comuna
    st.markdown("### 6. `comuna`")
    nulos_comuna = df[df["comuna"].isna()]
    if not nulos_comuna.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_comuna)} clientes sin comuna")
        render_troubled_rows(nulos_comuna[["cliente_id", "razon_social", "comuna", "row_index"]], source="gsheets", gid=SHEETS_IDS["clientes"])
    else:
        st.success(f"{ICONS['check']} Todos los clientes tienen comuna")
