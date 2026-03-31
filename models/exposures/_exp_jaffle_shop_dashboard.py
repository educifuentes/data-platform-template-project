import pandas as pd
from models.marts.jaffle_shop._dim_customers import dim_customers
from models.marts.jaffle_shop._fct_orders import fct_orders

def exp_jaffle_shop_dashboard():
    """Final exposure model meant to feed an end-user dashboard (e.g., Streamlit)."""
    customers = dim_customers()
    orders = fct_orders()

    # Just an example of an executive summary roll-up that a BI Engine could consume
    agg = orders.groupby('status').agg(
        total_orders=('id', 'count'),
        total_revenue=('amount', 'sum')
    ).reset_index()

    return agg
