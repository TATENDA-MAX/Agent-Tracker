import pandas as pd
import os
from db_manager import init_db, add_sales, add_receipts, get_all_sales, get_all_receipts, clear_db

def test_db():
    init_db()
    clear_db()

    # Test Sales
    sales_df = pd.DataFrame({
        'Date': ['2023-10-01'],
        'Agent': ['John Doe'],
        'Client': ['Client A'],
        'Amount': [1000]
    })
    add_sales(sales_df)

    # Test Receipts
    receipts_df = pd.DataFrame({
        'Date': ['2023-10-07'],
        'Agent': ['John Doe'],
        'Amount': [500]
    })
    add_receipts(receipts_df)

    # Verify
    all_sales = get_all_sales()
    all_receipts = get_all_receipts()

    assert len(all_sales) == 1
    assert len(all_receipts) == 1
    assert all_sales.iloc[0]['Amount'] == 1000

    # Test Append
    add_sales(sales_df)
    assert len(get_all_sales()) == 2

    print("Database tests passed!")

if __name__ == "__main__":
    test_db()
