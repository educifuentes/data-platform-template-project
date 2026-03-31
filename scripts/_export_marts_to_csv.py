import os
import sys
import pandas as pd

# Add the project root to sys.path to allow importing from helpers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers.utilities.find_model import find_model

def export_models_to_csv():
    """
    Exports specified marts models to CSV files in the 'exports' directory.
    """
    # 1. Define the models to export
    models_to_export = [
        "_fct_censos",
        "_fct_bases_ccu",
        "_dim_clientes"
    ]

    # 2. Ensure the exports directory exists
    export_dir = os.path.join("seeds", "outputs")
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
        print(f"Created directory: {export_dir}")

    # 3. Export each model
    for model_name in models_to_export:
        print(f"Exporting model: {model_name}...")
        try:
            df = find_model(model_name)
            if df is not None and isinstance(df, pd.DataFrame):
                output_path = os.path.join(export_dir, f"{model_name}.csv")
                df.to_csv(output_path, index=False)
                print(f"SUCCESS: Exported to {output_path}")
            else:
                print(f"FAILURE: Could not retrieve DataFrame for model {model_name}")
        except Exception as e:
            print(f"ERROR: Failed to export model {model_name}: {e}")

if __name__ == "__main__":
    export_models_to_csv()