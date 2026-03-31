import streamlit as st
import pandas as pd

from models.marts.gsheets._fct_bases_ccu_gsheets import fct_bases_ccu_gsheets
from models.marts.gsheets._dim_clientes_gsheets import dim_clientes_gsheets

from helpers.ui_components.ui_components import render_troubled_rows
from helpers.ui_components.ui_icons import ICONS
from helpers.constants.gsheets_ids import SHEETS_IDS

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
df = fct_bases_ccu_gsheets()
df_locales = dim_clientes_gsheets()


def validate_bases_ccu(periodo=None):
    st.header("Bases CCU")

    _df = df[df["periodo"] == periodo] if periodo else df
    total_filas = len(_df)
    if total_filas == 0:
        st.warning("La tabla Bases CCU está vacía.")
        return

    # 1. cliente_id + periodo
    st.markdown("### 1. `cliente_id` + `periodo`")
    _df["key"] = _df["cliente_id"].astype(str) + "_" + _df["periodo"].astype(str)
    ids_unicos = _df["key"].nunique()

    if ids_unicos == total_filas:
        st.success(f"{ICONS['check']} Registros únicos ({total_filas} filas)")
    else:
        st.error(f"{ICONS['close']} Se detectaron {total_filas - ids_unicos} duplicados")
        dupes = _df[_df.duplicated("key", keep=False)].sort_values(["cliente_id", "periodo"])
        render_troubled_rows(dupes[["cliente_id", "periodo", "row_index"]], source="gsheets", gid=SHEETS_IDS["bases_ccu"])

    # 1.1 Check Foreign Key (cliente_id exists in Clientes)
    st.markdown("### 1.1 cliente_id de Bases CCU no presente en tabla Clientes")
    ids_maestros = set(df_locales["cliente_id"].unique())
    ids_bases = set(_df["cliente_id"].unique())
    ids_faltantes = ids_bases - ids_maestros

    if not ids_faltantes:
        st.success(f"{ICONS['check']} Todos los `cliente_id` existen en la tabla Clientes")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(ids_faltantes)} `cliente_id` que NO existen en Clientes")
        missing_df = _df[_df["cliente_id"].isin(ids_faltantes)]
        render_troubled_rows(missing_df[["cliente_id", "periodo", "row_index"]].drop_duplicates(), source="gsheets", gid=SHEETS_IDS["bases_ccu"])

    # 2. Validez de Identificadores
    st.markdown("### 2. Validez de Identificadores")
    non_numeric = _df[pd.to_numeric(_df["cliente_id"], errors="coerce").isna()]
    if non_numeric.empty:
        st.success(f"{ICONS['check']} Todos los IDs son numéricos válidos.")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(non_numeric)} IDs no numéricos.")
        render_troubled_rows(non_numeric[["cliente_id", "periodo", "row_index"]], source="gsheets", gid=SHEETS_IDS["bases_ccu"])

    # 3. Activos Vacíos en 2024-Q1
    st.markdown("### 3. Activos Vacíos en 2024-Q1")
    df_2024 = _df[_df["periodo"] == "2024-Q1"]
    empty_activos = df_2024[
        df_2024["schoperas_ccu"].isna() &
        df_2024["coolers"].isna() &
        df_2024["salidas"].isna()
    ]

    if empty_activos.empty:
        st.success(f"{ICONS['check']} Todos los registros de 2024-Q1 tienen al menos un activo válido.")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(empty_activos)} registros en 2024-Q1 sin ningún activo reportado.")
        render_troubled_rows(empty_activos[["cliente_id", "periodo", "schoperas_ccu", "coolers", "salidas", "row_index"]], source="gsheets", gid=SHEETS_IDS["bases_ccu"])

    # 4. Contratos
    st.markdown("### 4. Contratos")

    nulos_id = _df[_df["cliente_id"].isna()]
    if not nulos_id.empty:
        st.error(f"{ICONS['close']} Detectados {len(nulos_id)} filas sin cliente_id")
        render_troubled_rows(nulos_id[["cliente_id", "folio", "row_index"]], source="gsheets", gid=SHEETS_IDS["bases_ccu"])
    else:
        st.success(f"{ICONS['check']} Todos los registros tienen cliente_id")

    nulos_folio = _df[_df["folio"].isna()]
    if not nulos_folio.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_folio)} registros sin Folio")
        render_troubled_rows(nulos_folio[["cliente_id", "folio", "row_index"]], source="gsheets", gid=SHEETS_IDS["bases_ccu"])
    else:
        st.success(f"{ICONS['check']} Todos los registros tienen Folio")
