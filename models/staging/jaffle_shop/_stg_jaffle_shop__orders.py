import pandas as pd

def stg_jaffle_shop__orders():
    """Staging model for Jaffle Shop orders, aligning with the 20 transaction records."""
    # For boilerplate, generate a matching order for every payment
    orders_data = []
    base_date = pd.to_datetime('2026-01-01')
    
    for i in range(1, 21):
        orders_data.append({
            "id": i,
            "user_id": (i % 5) + 1, # maps to 1-5 users consistently
            "order_date": (base_date + pd.Timedelta(days=i)).strftime('%Y-%m-%d'),
            "status": "completed" if i % 4 != 0 else "returned"
        })
        
    df = pd.DataFrame(orders_data)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df
