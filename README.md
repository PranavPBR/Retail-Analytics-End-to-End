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

`df1 = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2009-2010")
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
`

