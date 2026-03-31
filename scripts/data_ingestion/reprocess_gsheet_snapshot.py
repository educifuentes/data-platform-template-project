"Cambios en estructura de datos conversadis Feb 19 2026"

import pandas as pd

from models.intermediate.bases_ccu._int_bases_ccu__base_2026_q1 import int_bases_ccu__base_2026_q1_contratos_imagen, int_bases_ccu__base_2026_q1_activos
from models.intermediate.bases_ccu._int_bases_ccu__base_2024_q1 import int_reportes_ccu_base_2024_q1

from helpers.transformations.date_parsing import parse_spanish_month_year

path = "seeds/gsheets_snapshots/2026-02-20 - Activos CCU.xlsx"


def process_contratos(filepath: str) -> pd.DataFrame:
    """Solo dejar columnas locales_id y folio y que tiene cliente imagen"""
    df = int_bases_ccu__base_2026_q1_contratos_imagen()
    return df

def process_bases_ccu(filepath: str) -> pd.DataFrame:
    """Se agrega fecha_suscripcion_comodato, fecha_termino_comodato, activos_entregados"""

    df_2026 = int_bases_ccu__base_2026_q1_activos()
    df_2024 = int_reportes_ccu_base_2024_q1() 

    df = pd.concat([df_2026, df_2024], ignore_index=True)
    
    return df



def reprocessed_sheets():
    """Clean the sheets and return DataFrames processing each sheet separately."""
    # df_censos = process_censos(path)
    df_bases_ccu = process_bases_ccu(path)
    df_contratos = process_contratos(path)

    # # put dates column from contratos to bases_ccu based on periodo
    # if "periodo" in df_bases_ccu.columns:
    #     mask_2026 = df_bases_ccu["periodo"] == "2026-Q1"
    #     mask_2024 = df_bases_ccu["periodo"] == "2024-Q1"

    #     df_bases_ccu.loc[mask_2026, "fecha_inicio"] = df_contratos["fecha_inicio"]
    #     df_bases_ccu.loc[mask_2026, "fecha_termino"] = df_contratos["fecha_termino"]
    #     df_bases_ccu.loc[mask_2026, "activos_entregados"] = df_contratos["activos_entregados"]

    #     df_bases_ccu.loc[mask_2024, "fecha_inicio"] = pd.to_datetime("2024-01-01").date()
    #     df_bases_ccu.loc[mask_2024, "fecha_termino"] = pd.NA
    #     df_bases_ccu.loc[mask_2024, "activos_entregados"] = pd.NA

    # # drop those in contratos
    # # drop those in contratos
    # cols_to_drop = ["fecha_inicio", "fecha_termino", "activos_entregados"]
    # df_contratos = df_contratos.drop(columns=[c for c in cols_to_drop if c in df_contratos.columns], errors="ignore")

    return df_bases_ccu, df_contratos


if __name__ == "__main__":
    import os
    print("Reprocessing sheets...")
    df_bases_ccu, df_contratos = reprocessed_sheets()
    
    out_dir = "seeds/gsheets_snapshots/outputs"
    os.makedirs(out_dir, exist_ok=True)
    
    bases_ccu_path = f"{out_dir}/2026-02-20 - Activos CCU - bases_ccu.csv"
    contratos_path = f"{out_dir}/2026-02-20 - Activos CCU - contratos.csv"
    
    print(f"Exporting to {bases_ccu_path}...")
    df_bases_ccu.to_csv(bases_ccu_path, index=False)
    
    print(f"Exporting to {contratos_path}...")
    df_contratos.to_csv(contratos_path, index=False)
    
    print("Done!")