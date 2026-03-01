import streamlit as st
import pandas as pd
from tracker_logic import process_data, get_agent_summary, get_overdue_tracker
from db_manager import init_db, add_sales, add_receipts, get_all_sales, get_all_receipts, clear_db

st.set_page_config(page_title="Insurance Agent Debt Tracker", layout="wide")

# Initialize Database
init_db()

st.title("Insurance Agent Debt Tracker")

st.sidebar.header("Upload Data")
sales_file = st.sidebar.file_uploader("Upload New Sales Report (CSV)", type=["csv"])
receipts_file = st.sidebar.file_uploader("Upload New Receipts (CSV)", type=["csv"])

if st.sidebar.button("Process Uploads"):
    if sales_file:
        new_sales = pd.read_csv(sales_file)
        add_sales(new_sales)
        st.sidebar.success("Sales added to database!")
    if receipts_file:
        new_receipts = pd.read_csv(receipts_file)
        add_receipts(new_receipts)
        st.sidebar.success("Receipts added to database!")

if st.sidebar.button("Clear Database"):
    clear_db()
    st.sidebar.warning("Database cleared!")
    st.rerun()

# Load all data from database
sales_df = get_all_sales()
receipts_df = get_all_receipts()

if not sales_df.empty:
    try:
        # If we have sales but no receipts, create an empty df with correct columns for receipts
        if receipts_df.empty:
            receipts_df = pd.DataFrame(columns=['Date', 'Agent', 'Amount'])

        processed_df = process_data(sales_df, receipts_df)

        st.header("Agent Summary (Cumulative)")
        summary_df = get_agent_summary(processed_df)
        st.dataframe(summary_df.style.format({"Total Owed": "${:.2f}", "Current Balance": "${:.2f}"}))

        st.header("Overdue Tracker")
        overdue_df = get_overdue_tracker(processed_df)

        if not overdue_df.empty:
            # Formatting for display
            display_overdue = overdue_df.copy()
            display_overdue['Date'] = display_overdue['Date'].dt.strftime('%Y-%m-%d')
            display_overdue['DueDate'] = display_overdue['DueDate'].dt.strftime('%Y-%m-%d')

            st.dataframe(display_overdue.style.format({
                "OwedToCompany": "${:.2f}",
                "Balance": "${:.2f}"
            }))

            # Additional analysis
            st.subheader("Time-based Metrics (Summary)")
            metrics = overdue_df.groupby('Agent').agg({
                'Balance': 'sum',
                'DaysOverdue': 'max'
            }).reset_index()
            metrics.columns = ['Agent', 'Total Overdue Balance', 'Oldest Overdue (Days)']
            st.table(metrics.style.format({"Total Overdue Balance": "${:.2f}"}))
        else:
            st.success("No overdue balances found!")

    except Exception as e:
        st.error(f"Error processing data: {e}")
        st.info("Please ensure your CSV files have the correct columns (Date, Agent, Client, Amount for Sales; Date, Agent, Amount for Receipts).")

else:
    st.info("The database is currently empty. Please upload Sales Report and Receipts CSV files and click 'Process Uploads'.")

    with st.expander("See Sample Format"):
        st.write("### Sales Report")
        st.code("Date,Agent,Client,Amount\n2023-10-01,John Doe,Client A,1000")
        st.write("### Receipts")
        st.code("Date,Agent,Amount\n2023-10-07,John Doe,1200")
