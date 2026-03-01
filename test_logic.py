import pandas as pd
from tracker_logic import process_data, get_agent_summary, get_overdue_tracker
from datetime import datetime, timedelta

def test_process_data():
    sales_data = {
        'Date': ['2023-10-01', '2023-10-05'],
        'Agent': ['John Doe', 'John Doe'],
        'Client': ['Client A', 'Client B'],
        'Amount': [1000, 2000]
    }
    receipts_data = {
        'Date': ['2023-10-07'],
        'Agent': ['John Doe'],
        'Amount': [1200]
    }

    sales_df = pd.DataFrame(sales_data)
    receipts_df = pd.DataFrame(receipts_data)

    processed_df = process_data(sales_df, receipts_df)

    # John Doe Owed: 500 (from 1000) + 1000 (from 2000) = 1500
    # John Doe Paid: 1200
    # FIFO: 500 paid for Client A, 700 paid for Client B.
    # Balance: Client A: 0, Client B: 300.

    john_doe_b = processed_df[processed_df['Client'] == 'Client B'].iloc[0]
    assert john_doe_b['Balance'] == 300

    john_doe_a = processed_df[processed_df['Client'] == 'Client A'].iloc[0]
    assert john_doe_a['Balance'] == 0

    print("test_process_data passed!")

def test_aging():
    today = datetime.now().date()
    yesterday = (today - timedelta(days=1)).isoformat()
    three_days_ago = (today - timedelta(days=3)).isoformat()

    sales_data = {
        'Date': [three_days_ago, yesterday],
        'Agent': ['John Doe', 'John Doe'],
        'Client': ['Client A', 'Client B'],
        'Amount': [1000, 1000]
    }
    receipts_data = {
        'Date': [today.isoformat()],
        'Agent': ['John Doe'],
        'Amount': [0]
    }

    sales_df = pd.DataFrame(sales_data)
    receipts_df = pd.DataFrame(receipts_data)

    processed_df = process_data(sales_df, receipts_df)

    # Client A underwritten 3 days ago. Due 2 days ago. Overdue by 2 days.
    client_a = processed_df[processed_df['Client'] == 'Client A'].iloc[0]
    assert client_a['DaysOverdue'] == 2

    # Client B underwritten yesterday. Due today. Overdue by 0 days.
    client_b = processed_df[processed_df['Client'] == 'Client B'].iloc[0]
    assert client_b['DaysOverdue'] == 0

    print("test_aging passed!")

if __name__ == "__main__":
    test_process_data()
    test_aging()
