**Retail-Analytics-End-to-End**

End-to-end Online Retail Analytics project using Python, SQL, and Power BI — includes ETL, data cleaning, SQL modeling, KPI calculations, and an interactive dashboard.

An end-to-end Retail Analytics project using Python, SQL, and Power BI

This repository presents a complete analytics workflow built on top of the Online Retail II dataset from the UCI Machine Learning Repository

**Dataset link:** [Retail data set](https://archive.ics.uci.edu/dataset/502/online+retail+ii)

The goal of this project is to demonstrate how raw retail data can be transformed into actionable business intelligence insights through a modern multi-tool pipeline. The workflow includes:

Python for ETL, cleaning, preprocessing, and feature engineering

SQLite + SQL for modeling, data slicing, and analytical exports

Power BI for interactive dashboards and KPI reporting

This mirrors how real analytics teams build reliable, scalable reporting systems across industries like E-commerce, Retail, and CPG.

**Dataset Description**

The dataset used in this project is the UCI Online Retail Dataset, containing over 540K transaction records from an online UK gift retailer.

The original file includes:

Invoice records

Product descriptions

Quantity and pricing

Customer IDs

Country information

Timestamps for each purchase

Each year exists as a separate sheet; both are combined during ETL.

**Part 1 — ETL & Data Cleaning (Python)**

All preprocessing steps are handled in Python to create a clean, analysis-ready dataset.

**Steps Performed**

    Import the raw Excel file (single sheet containing all transactions).
    
    Remove rows with missing CustomerID, since customer-level analysis depends on it.
    
    Drop duplicate records to avoid double-counting sales.
    
    Convert InvoiceDate to proper datetime for time-series analysis.
    
    Engineer new time-based columns:
    
        Year
        
        Month
        
        Week
        
        DayOfWeek
    
    Quarter
    
    Compute TotalPrice = Quantity × UnitPrice for revenue calculations.
    
    Standardize column names to snake_case for SQL and Power BI compatibility.
    
    Store the processed data in a local SQLite database (online_retail_clean.db).

**Python ETL Code (Summary)**

```
import pandas as pd
import sqlite3

# Load the Excel dataset (single sheet)
df = pd.read_excel("online_retail.xlsx")

# Remove rows without CustomerID
df = df.dropna(subset=["CustomerID"]).copy()

# Remove duplicates
df = df.drop_duplicates().copy()

# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

# Feature engineering
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["Week"] = df["InvoiceDate"].dt.isocalendar().week
df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
df["Quarter"] = df["InvoiceDate"].dt.quarter

# Total price per line (revenue)
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# Standardize column names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Save to SQLite
conn = sqlite3.connect("online_retail_clean.db")
df.to_sql("retail_data", conn, index=False, if_exists="replace")
conn.close()

```


**Part 2 — SQL Modeling & Analytical Outputs**

Using SQLite, the cleaned dataset is queried to produce structured domain-specific tables for Power BI.

1️⃣ Sales Summary

Contains transaction-level revenue, quantities, and date attributes for positive-quantity invoices.

```
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
WHERE quantity > 0;

```

2️⃣ Top Products by Quantity

Ranks products based on sales volume.

```
SELECT 
    stockcode,
    description,
    SUM(quantity) AS total_quantity
FROM retail_data
WHERE quantity > 0
GROUP BY stockcode, description
ORDER BY total_quantity DESC;

```

3️⃣ Customer Activity / Lifetime Value

Evaluates customer engagement patterns.

```
SELECT 
    customerid,
    COUNT(DISTINCT invoice_no) AS invoice_count,
    SUM(totalprice) AS total_spent,
    MAX(invoicedate) AS last_purchase_date,
    COUNT(DISTINCT year || '-' || month) AS active_months
FROM retail_data
WHERE quantity > 0
GROUP BY customerid
ORDER BY total_spent DESC;

```

4️⃣ Returns Summary

Captures negative-quantity transactions.

```
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
WHERE quantity < 0;

```

**Part 3 — Power BI Dashboard**

Major Dashboard Sections

**Dashboard Visuals Used**

**KPI Cards**
```
- Total Revenue (Card)
- Total Quantity Sold (Card)
- Total Invoices (Card)
- Total Customers (Card)
- Revenue per Customer (Card)
- Total Returns Value (Card)
- Returns Percentage (Card)
```

**Trend Charts**
```
- Line Chart: Total Revenue by Month Name
- Line Chart: Total Revenue by Week of Year
- Line Chart: Average Unit Price by Month Name
```

**Revenue Breakdown**
```
- Column Chart: Total Revenue by Quarter
- Bar Chart: Top 10 Quantity Sold by Description
- Bar Chart: Top 10 Revenue by Description
- Table: customerid vs Total Revenue
```

**Customer Analysis**
```
- Bar Chart: Total Customers by Country
```

**Returns Analysis**
```
- Bar Chart: Total Returns Value by Description
- Column Chart: Returns Percentage by Country
- Combo Chart: Total Returns Value and Total Revenue by Month Name
```

**Filters / Slicers**
```
- Country
- Year (2010, 2011)
- Month Name
```
**Key DAX Measures Used**

```
-- CORE SALES MEASURES

-- Total Revenue
Total Revenue =
SUM ( 'Online Retail'[totalprice] )

-- Total Quantity Sold
Total Quantity Sold =
SUM ( 'Online Retail'[Quantity] )

-- Total Invoices
Total Invoices =
DISTINCTCOUNT ( 'Online Retail'[invoice_no] )

-- Total Customers
Total Customers =
DISTINCTCOUNT ( 'Online Retail'[customerid] )

-- Revenue per Customer
Revenue per Customer =
DIVIDE ( [Total Revenue], [Total Customers] )

-- Average Order Value
Average Order Value =
DIVIDE ( [Total Revenue], [Total Invoices] )

-- RETURNS MEASURES

-- Total Returns Value
Total Returns Value =
SUM ( Returns[totalprice] )

-- Total Returns Count
Total Returns Count =
COUNT ( Returns[Quantity] )

-- Returns Percentage
Returns Percentage =
DIVIDE ( [Total Returns Value], [Total Revenue] )


-- CUSTOMER SEGMENTATION MEASURE

-- Customer Active Months (example pattern)
Customer Active Months =
CALCULATE (
    DISTINCTCOUNT ( 'Online Retail'[Month] ),
    ALLEXCEPT ( 'Online Retail', 'Online Retail'[customerid] )
)

-- Customer Type
Customer Type =
SWITCH (
    TRUE(),
    [Customer Active Months] <= 2, "Inactive",
    [Customer Active Months] <= 5, "Normal",
    "Active"
)

```

Business Insights Discovered

1. Customer Revenue Concentration

    A small segment of highly active customers contributes the majority of revenue

   Classic Pareto 80/20 behavior is observed

2. Returns Behavior

    Returns account for < 20% of total value — acceptably healthy

    Most returns originate from inactive or low-engagement customers

    The UK leads both revenue and returns (largest customer base)

3. Product Trends

    Some SKUs generate disproportionate revenue compared to others

    Seasonal spikes affect Average Order Value

4. Pricing Stability

    Individual product prices remain mostly stable

    Variations in AOV driven by basket size and seasonal buying patterns

**Conclusion**

This project encapsulates a powerful demonstration of:

Multi-tool analytics pipelines

Clean ETL practices

SQL-driven analytical modeling

Professional BI dashboard creation

Effective storytelling using real retail data

It showcases how raw spreadsheets can be transformed into insightful, interactive decision-making tools — the exact workflow used across modern data teams.
