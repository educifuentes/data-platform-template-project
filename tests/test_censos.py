import streamlit as st
import pandas as pd

from models.marts.gsheets._fct_censos_gsheets import fct_censos_gsheets
from models.marts.gsheets._dim_clientes_gsheets import dim_clientes_gsheets

from helpers.ui_components.ui_components import render_troubled_rows
from helpers.ui_components.ui_icons import ICONS
from helpers.constants.gsheets_ids import SHEETS_IDS

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
df = fct_censos_gsheets()
df_clientes = dim_clientes_gsheets()


def validate_censos(periodo=None):
    st.header("Censos")

    _df = df[df["periodo"] == periodo] if periodo else df
    total_filas = len(_df)
    if total_filas == 0:
        st.warning("La tabla Censos está vacía.")
        return

    # 1. Generales
    st.markdown("### 1. Generales")

    # 1.1 Uniqueness
    st.markdown("#### 1.1 `cliente_id` + `periodo` duplicados")
    _df["key"] = _df["cliente_id"].astype(str) + "_" + _df["periodo"].astype(str)
    ids_unicos = _df["key"].nunique()

    if ids_unicos == total_filas:
        st.success(f"{ICONS['check']} Unicidad por Cliente y Periodo ({total_filas} registros)")
    else:
        st.error(f"{ICONS['close']} Se detectaron {total_filas - ids_unicos} registros duplicados (mismo Cliente y Periodo)")
        dupes = _df[_df.duplicated("key", keep=False)].sort_values(["cliente_id", "periodo"])
        render_troubled_rows(dupes[["cliente_id", "periodo", "schoperas_ccu", "row_index"]], source="gsheets", gid=SHEETS_IDS["censos"])

    # 1.2 Check Foreign Key (cliente_id exists in Clientes)
    st.markdown("#### 1.2 `cliente_id` de censos no presente en tabla Clientes")
    ids_maestros = set(df_clientes["cliente_id"].unique())
    ids_censos = set(_df["cliente_id"].unique())
    ids_faltantes = ids_censos - ids_maestros

    if not ids_faltantes:
        st.success(f"{ICONS['check']} Todos los `cliente_id` existen en la tabla Clientes")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(ids_faltantes)} `cliente_id` que NO existen en Clientes")
        missing_df = _df[_df["cliente_id"].isin(ids_faltantes)]
        render_troubled_rows(missing_df[["cliente_id", "periodo", "row_index"]].drop_duplicates(), source="gsheets", gid=SHEETS_IDS["censos"])

    # 2.1 Check for Negative Values
    st.markdown("#### 2.1 Valores negativos en `salidas`")
    negativos_sal = _df[_df["salidas"] < 0]
    if not negativos_sal.empty:
        st.error(f"{ICONS['close']} Se detectaron {len(negativos_sal)} registros con salidas negativas")
        render_troubled_rows(negativos_sal[["cliente_id", "periodo", "salidas", "row_index"]], source="gsheets", gid=SHEETS_IDS["censos"])
    else:
        st.success(f"{ICONS['check']} No hay valores negativos en salidas")

    # 3. Censo 2 (2025-S2) Validations
    st.markdown("### 3. Validaciones para Censo 2 - 2025-S2")
    df_2025 = _df[_df["periodo"] == "2025-S2"]

    if df_2025.empty:
        st.warning("No hay datos para el periodo 2025-S2")
    else:
        # 3.1 instalo
        st.markdown("#### 3.1 Nulos y negativos en `instalo`")

        nulos_ins = df_2025["instalo"].isna().sum()
        if nulos_ins > 0:
            st.warning(f"{ICONS['warning']} {nulos_ins} registros con 'instalo' nulo")
            render_troubled_rows(df_2025[df_2025["instalo"].isna()][["cliente_id", "periodo", "instalo", "row_index"]], source="gsheets", gid=SHEETS_IDS["censos"])
        else:
            st.success(f"{ICONS['check']} 'instalo': Sin nulos")

        negativos_ins = df_2025[df_2025["instalo"] < 0]
        if not negativos_ins.empty:
            st.error(f"{ICONS['close']} Se detectaron {len(negativos_ins)} registros con instalo negativos")
            render_troubled_rows(negativos_ins[["cliente_id", "periodo", "instalo", "row_index"]], source="gsheets", gid=SHEETS_IDS["censos"])
        else:
            st.success(f"{ICONS['check']} No hay valores negativos en instalo")

        # 3.2 disponibilizo
        st.markdown("#### 3.2 Nulos y negativos en `disponibilizo`")

        nulos_disp = df_2025["disponibilizo"].isna().sum()
        if nulos_disp > 0:
            st.warning(f"{ICONS['warning']} {nulos_disp} registros con 'disponibilizo' nulo")
            render_troubled_rows(df_2025[df_2025["disponibilizo"].isna()][["cliente_id", "periodo", "disponibilizo", "row_index"]], source="gsheets", gid=SHEETS_IDS["censos"])
        else:
            st.success(f"{ICONS['check']} 'disponibilizo': Sin nulos")

        negativos_disp = df_2025[df_2025["disponibilizo"] < 0]
        if not negativos_disp.empty:
            st.error(f"{ICONS['close']} Se detectaron {len(negativos_disp)} registros con disponibilizo negativos")
            render_troubled_rows(negativos_disp[["cliente_id", "periodo", "disponibilizo", "row_index"]], source="gsheets", gid=SHEETS_IDS["censos"])
        else:
            st.success(f"{ICONS['check']} No hay valores negativos en disponibilizo")
