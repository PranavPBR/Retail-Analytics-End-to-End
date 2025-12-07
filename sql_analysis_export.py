# SQL ANALYSIS + PREP FOR POWER BI

import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("online_retail_clean.db")

# ----------------------------------------
# 1️⃣ Sales Summary
# ----------------------------------------
query1 = """
    SELECT 
        invoice_no,
        customerid,
        stockcode,
        description,
        country,
        year,
        month,
        week,
        quantity AS total_quantity,
        unitprice,
        totalprice AS total_revenue,
        invoicedate
    FROM retail_data
    WHERE quantity > 0
"""
sales_summary = pd.read_sql_query(query1, conn)

# ----------------------------------------
# 2️⃣ Products by Quantity
# ----------------------------------------
query2 = """
    SELECT 
        stockcode,
        description,
        SUM(quantity) AS total_quantity
    FROM retail_data
    WHERE quantity > 0
    GROUP BY stockcode, description
    ORDER BY total_quantity DESC
"""
products_by_quantity = pd.read_sql_query(query2, conn)

# ----------------------------------------
# 3️⃣ Customer Activity / LTV
# ----------------------------------------
query3 = """
    SELECT 
        customerid,
        SUM(totalprice) AS total_spent,
        COUNT(DISTINCT invoice_no) AS invoice_count,
        MAX(invoicedate) AS last_purchase_date,
        COUNT(DISTINCT year || '-' || month) AS active_months
    FROM retail_data
    WHERE quantity > 0
    GROUP BY customerid
    ORDER BY total_spent DESC
"""
customer_activity = pd.read_sql_query(query3, conn)

# ----------------------------------------
# 4️⃣ Returns Summary
# ----------------------------------------
query4 = """
    SELECT 
        invoice_no,
        customerid,
        stockcode,
        description,
        country,
        year,
        month,
        week,
        quantity AS return_quantity,
        totalprice AS return_value,
        invoicedate
    FROM retail_data
    WHERE quantity < 0
"""
returns_summary = pd.read_sql_query(query4, conn)

# Close DB connection
conn.close()

# ----------------------------------------
# Export all datasets to CSV
# ----------------------------------------
sales_summary.to_csv("sales_summary.csv", index=False)
products_by_quantity.to_csv("products_by_quantity.csv", index=False)
customer_activity.to_csv("customer_activity.csv", index=False)
returns_summary.to_csv("returns_summary.csv", index=False)

print("SQL analysis completed and CSV files exported successfully.")
