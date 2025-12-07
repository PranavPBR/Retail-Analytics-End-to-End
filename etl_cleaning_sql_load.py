import pandas as pd
import sqlite3

# -------------------------------
# Load the Online Retail dataset
# -------------------------------
df = pd.read_excel("online_retail.xlsx")   # Update file name if needed

# -------------------------------
# Data Cleaning
# -------------------------------

# Remove rows without CustomerID
df = df.dropna(subset=["CustomerID"]).copy()

# Remove duplicates
df = df.drop_duplicates().copy()

# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

# -------------------------------
# Feature Engineering
# -------------------------------
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["Week"] = df["InvoiceDate"].dt.isocalendar().week
df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
df["Quarter"] = df["InvoiceDate"].dt.quarter

# Compute total price (Line-level revenue)
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# -------------------------------
# Rename columns for SQL compatibility
# -------------------------------
df.columns = df.columns.str.lower().str.replace(" ", "_")

# -------------------------------
# Save to SQLite database
# -------------------------------
conn = sqlite3.connect("online_retail_clean.db")
df.to_sql("retail_data", conn, index=False, if_exists="replace")
conn.close()

print("ETL Process Completed: Data cleaned and loaded into SQLite database.")
