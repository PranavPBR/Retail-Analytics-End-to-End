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

The dataset contains two years of historical e-commerce transactions (2009–2010 and 2010–2011) from a UK-based online retailer. The original file includes:

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

    Import both sheets from the Excel file
    
    Combine the sheets into a unified DataFrame
    
    Remove nulls & duplicates
    
    Convert InvoiceDate into proper datetime
    
    Engineer time-based features:
        Year
        Month
        Week number
        Day of week
        Quarter
        
    Convert Customer ID to integer
    
    Standardize column names (snake_case)
    
    Store clean data in a SQLite database (online_retail_clean.db)

**Python ETL Code (Summary)**

```
df1 = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2009-2010")
df2 = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2010-2011")

df = pd.concat([df1, df2], ignore_index=True)
df = df.dropna().drop_duplicates().copy()

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["Week"] = df["InvoiceDate"].dt.isocalendar().week
df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
df["Quarter"] = df["InvoiceDate"].dt.quarter

df.columns = df.columns.str.lower().str.replace(" ", "_")

conn = sqlite3.connect("online_retail_clean.db")
df.to_sql("retail_data", conn, index=False, if_exists="replace")
conn.close()
```


**Part 2 — SQL Modeling & Analytical Outputs**

Using SQLite, the cleaned dataset is queried to produce structured domain-specific tables for Power BI.

1️⃣ Sales Summary

Contains transaction-level revenue, quantities, and date attributes for positive-quantity invoices.

```
SELECT customer_id, invoice, description, country, year, month, week,
       price, quantity AS total_quantity,
       quantity * price AS total_revenue,
       invoicedate
FROM retail_data
WHERE quantity > 0;
```

2️⃣ Top Products by Quantity

Ranks products based on sales volume.

```
SELECT invoice, stockcode, description,
       quantity AS total_quantity
FROM retail_data
WHERE quantity > 0
ORDER BY total_quantity DESC;
```

3️⃣ Customer Activity / Lifetime Value

Evaluates customer engagement patterns.

```
SELECT customer_id,
       invoice,
       quantity * price AS total_spent,
       MAX(invoicedate) AS last_purchase_date,
       COUNT(DISTINCT year || '-' || month) AS active_months
FROM retail_data
GROUP BY customer_id
ORDER BY total_spent DESC;
```

4️⃣ Returns Summary

Captures negative-quantity transactions.

```
SELECT customer_id, invoice, country, year, month, week,
       stockcode, description, price,
       quantity AS total_returns_quantity,
       quantity * price AS total_returns_value,
       invoicedate
FROM retail_data
WHERE quantity < 0;
```

**Part 3 — Power BI Dashboard**

Major Dashboard Sections

**KPI Bar (Top Panel)**
    Total Revenue
    Total Quantity Sold
    Revenue per Customer
    Returns %
    Total Returns Value
    Total Returns Count

**Revenue & Sales Trends**
    Month-over-Month and Year-over-Year revenue
    Weekly trend analysis

**Customer Insights**
    Active months
    Customer segmentation
    Total spend and LTV metrics

**Product & Pricing Behavior**
    Best-selling products
    AOV & Average price over time

**Returns Analysis**
    Returns by country
    Returns vs revenue

**Key DAX Measures Used**

```
Total Revenue = SUM(sales_summary[total_revenue])

Total Quantity Sold = SUM(sales_summary[total_quantity])

Total Invoices = DISTINCTCOUNT(sales_summary[invoice])

Revenue Per Customer = [Total Revenue] / DISTINCTCOUNT(customer_activity[customer_id])

Average Order Value = [Total Revenue] / [Total Invoices]

Total Returns Value = SUM(returns_summary[total_returns_value])

Returns Percentage = DIVIDE([Total Returns Value], [Total Revenue])

Products Count = COUNT(products_by_quantity[total_quantity])

Revenue Per Product = DIVIDE([Total Revenue], [Products Count])
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
