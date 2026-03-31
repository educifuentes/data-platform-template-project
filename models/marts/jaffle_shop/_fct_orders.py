import pandas as pd
from models.staging.jaffle_shop._stg_jaffle_shop__orders import stg_jaffle_shop__orders
from models.staging.payments._stg_payments__transactions import stg_payments__transactions

def fct_orders():
    """Mart model for facts around orders, joining with specific transactions for amounts."""
    orders = stg_jaffle_shop__orders()
    payments = stg_payments__transactions()

    # Sum payments per order
    order_payments = payments.groupby('order_id').agg(
        amount=('amount', 'sum')
    ).reset_index()
    
    # Merge order details with their total paid amounts
    fct_ord = orders.merge(order_payments, left_on='id', right_on='order_id', how='left')
    fct_ord['amount'] = fct_ord['amount'].fillna(0)
    
    # Drop redundancy
    fct_ord.drop(columns=['order_id'], inplace=True, errors='ignore')

    return fct_ord
