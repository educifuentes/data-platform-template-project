import pandas as pd

def stg_jaffle_shop__customers():
    """Staging model for Jaffle Shop customers, providing basic dummy records."""
    data = [
        {"id": 1, "first_name": "Michael", "last_name": "P."},
        {"id": 2, "first_name": "Shawn", "last_name": "M."},
        {"id": 3, "first_name": "Kathleen", "last_name": "P."},
        {"id": 4, "first_name": "Gary", "last_name": "A."},
        {"id": 5, "first_name": "Julia", "last_name": "B."},
    ]
    return pd.DataFrame(data)
