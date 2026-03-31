import pandas as pd

def stg_payments__transactions():
    """Staging model for transactions logic, supplying 20 boilerplate rows."""
    data = [
        {"id": 1, "order_id": 1, "payment_method": "credit_card", "amount": 1000},
        {"id": 2, "order_id": 2, "payment_method": "credit_card", "amount": 2000},
        {"id": 3, "order_id": 3, "payment_method": "coupon", "amount": 100},
        {"id": 4, "order_id": 4, "payment_method": "bank_transfer", "amount": 3000},
        {"id": 5, "order_id": 5, "payment_method": "credit_card", "amount": 1500},
        {"id": 6, "order_id": 6, "payment_method": "credit_card", "amount": 2500},
        {"id": 7, "order_id": 7, "payment_method": "gift_card", "amount": 500},
        {"id": 8, "order_id": 8, "payment_method": "bank_transfer", "amount": 4000},
        {"id": 9, "order_id": 9, "payment_method": "credit_card", "amount": 1200},
        {"id": 10, "order_id": 10, "payment_method": "credit_card", "amount": 2200},
        {"id": 11, "order_id": 11, "payment_method": "bank_transfer", "amount": 3200},
        {"id": 12, "order_id": 12, "payment_method": "credit_card", "amount": 1800},
        {"id": 13, "order_id": 13, "payment_method": "credit_card", "amount": 2800},
        {"id": 14, "order_id": 14, "payment_method": "gift_card", "amount": 800},
        {"id": 15, "order_id": 15, "payment_method": "bank_transfer", "amount": 5000},
        {"id": 16, "order_id": 16, "payment_method": "credit_card", "amount": 1100},
        {"id": 17, "order_id": 17, "payment_method": "credit_card", "amount": 2100},
        {"id": 18, "order_id": 18, "payment_method": "coupon", "amount": 200},
        {"id": 19, "order_id": 19, "payment_method": "bank_transfer", "amount": 3300},
        {"id": 20, "order_id": 20, "payment_method": "credit_card", "amount": 1600},
    ]
    df = pd.DataFrame(data)
    # Generic cleaning
    df['amount'] = pd.to_numeric(df['amount']) / 100 # converting cents to dollars
    return df
