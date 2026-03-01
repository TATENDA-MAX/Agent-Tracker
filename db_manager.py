import sqlite3
import pandas as pd

DB_NAME = "insurance_tracker.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        Agent TEXT,
        Client TEXT,
        Amount REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        Agent TEXT,
        Amount REAL
    )
    ''')

    conn.commit()
    conn.close()

def add_sales(df):
    conn = sqlite3.connect(DB_NAME)
    df.to_sql('sales', conn, if_exists='append', index=False)
    conn.close()

def add_receipts(df):
    conn = sqlite3.connect(DB_NAME)
    df.to_sql('receipts', conn, if_exists='append', index=False)
    conn.close()

def get_all_sales():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql('SELECT Date, Agent, Client, Amount FROM sales', conn)
    conn.close()
    return df

def get_all_receipts():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql('SELECT Date, Agent, Amount FROM receipts', conn)
    conn.close()
    return df

def clear_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sales')
    cursor.execute('DELETE FROM receipts')
    conn.commit()
    conn.close()
