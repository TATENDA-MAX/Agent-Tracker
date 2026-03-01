import pandas as pd
from datetime import datetime, timedelta

def process_data(sales_df, receipts_df):
    # Ensure date columns are datetime objects
    sales_df['Date'] = pd.to_datetime(sales_df['Date'])
    receipts_df['Date'] = pd.to_datetime(receipts_df['Date'])

    # Sort sales by date for FIFO
    sales_df = sales_df.sort_values(by=['Agent', 'Date'])
    receipts_df = receipts_df.sort_values(by=['Agent', 'Date'])

    # Calculate amount owed to company (50% of sales)
    sales_df['OwedToCompany'] = sales_df['Amount'] * 0.5
    sales_df['Balance'] = sales_df['OwedToCompany']

    # Group receipts by agent
    agents = sales_df['Agent'].unique()

    for agent in agents:
        agent_sales = sales_df[sales_df['Agent'] == agent]
        agent_receipts = receipts_df[receipts_df['Agent'] == agent]

        total_paid = agent_receipts['Amount'].sum()

        # Apply total_paid to agent_sales using FIFO
        for idx, row in agent_sales.iterrows():
            if total_paid <= 0:
                break

            amount_to_apply = min(total_paid, row['Balance'])
            sales_df.at[idx, 'Balance'] -= amount_to_apply
            total_paid -= amount_to_apply

    # Calculate Overdue
    today = datetime.now()
    # "The due date for the agent to remit the money to the company is a day after the day the insurance was underwritten"
    sales_df['DueDate'] = sales_df['Date'] + timedelta(days=1)
    sales_df['DaysOverdue'] = (today - sales_df['DueDate']).dt.days
    sales_df['DaysOverdue'] = sales_df['DaysOverdue'].apply(lambda x: max(0, x))

    return sales_df

def get_agent_summary(processed_df):
    summary = processed_df.groupby('Agent').agg({
        'OwedToCompany': 'sum',
        'Balance': 'sum'
    }).reset_index()
    summary.rename(columns={'OwedToCompany': 'Total Owed', 'Balance': 'Current Balance'}, inplace=True)
    return summary

def get_overdue_tracker(processed_df):
    # Only show items with a balance > 0
    overdue = processed_df[processed_df['Balance'] > 0].copy()
    overdue = overdue[['Date', 'Agent', 'Client', 'OwedToCompany', 'Balance', 'DueDate', 'DaysOverdue']]
    return overdue
