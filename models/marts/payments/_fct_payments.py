import pandas as pd
from models.staging.payments._stg_payments__transactions import stg_payments__transactions

def fct_payments():
    """Mart layer directly exposing transactions. In complex scenarios, it would resolve currency, taxa and fx."""
    # A simple pass-through boilerplate example
    transactions = stg_payments__transactions()
    
    # Example logic: categorizing transactions
    def categorize_tier(amount):
        if amount > 25:
            return 'high_value'
        elif amount > 10:
            return 'medium_value'
        return 'low_value'

    transactions['payment_tier'] = transactions['amount'].apply(categorize_tier)
    
    return transactions
