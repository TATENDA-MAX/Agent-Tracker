import streamlit as st
import pandas as pd
from tracker_logic import process_data, get_agent_summary, get_overdue_tracker

st.set_page_config(page_title="Insurance Agent Debt Tracker", layout="wide")

st.title("Insurance Agent Debt Tracker")

st.sidebar.header("Upload Data")
sales_file = st.sidebar.file_uploader("Upload Sales Report (CSV)", type=["csv"])
receipts_file = st.sidebar.file_uploader("Upload Receipts (CSV)", type=["csv"])

if sales_file and receipts_file:
    sales_df = pd.read_csv(sales_file)
    receipts_df = pd.read_csv(receipts_file)

    try:
        processed_df = process_data(sales_df, receipts_df)

        st.header("Agent Summary")
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
    st.info("Please upload both Sales Report and Receipts CSV files to begin.")

    with st.expander("See Sample Format"):
        st.write("### Sales Report")
        st.code("Date,Agent,Client,Amount\n2023-10-01,John Doe,Client A,1000")
        st.write("### Receipts")
        st.code("Date,Agent,Amount\n2023-10-07,John Doe,1200")
