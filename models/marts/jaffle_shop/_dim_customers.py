import pandas as pd
from models.staging.jaffle_shop._stg_jaffle_shop__customers import stg_jaffle_shop__customers
from models.staging.jaffle_shop._stg_jaffle_shop__orders import stg_jaffle_shop__orders
from models.staging.payments._stg_payments__transactions import stg_payments__transactions

def dim_customers():
    """Mart model that builds a generic customer dimension, combining stats from orders and payments."""
    customers = stg_jaffle_shop__customers()
    orders = stg_jaffle_shop__orders()
    payments = stg_payments__transactions()

    # Aggregate orders per user
    customer_orders = orders.groupby('user_id').agg(
        first_order_date=('order_date', 'min'),
        most_recent_order_date=('order_date', 'max'),
        number_of_orders=('id', 'count')
    ).reset_index()

    # Join with payments
    order_payments = orders.merge(payments, left_on='id', right_on='order_id', how='left')
    customer_payments = order_payments.groupby('user_id')['amount'].sum().reset_index()
    customer_payments.rename(columns={'amount': 'lifetime_value'}, inplace=True)

    # Final dimension table
    dim_cust = customers.merge(customer_orders, left_on='id', right_on='user_id', how='left')
    dim_cust = dim_cust.merge(customer_payments, on='user_id', how='left')
    
    dim_cust['first_order_date'] = pd.to_datetime(dim_cust['first_order_date'])
    dim_cust['most_recent_order_date'] = pd.to_datetime(dim_cust['most_recent_order_date'])
    dim_cust['number_of_orders'] = dim_cust['number_of_orders'].fillna(0).astype(int)
    dim_cust['lifetime_value'] = dim_cust['lifetime_value'].fillna(0)

    # Drop redundant column
    dim_cust.drop(columns=['user_id'], inplace=True, errors='ignore')

    return dim_cust
