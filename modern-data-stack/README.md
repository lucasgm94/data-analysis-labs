# 📊 Modern Data Stack: Sales Analytics Dashboard
### **Developed by Lucas Martinez** 🚀

This project demonstrates a full-spectrum Data Engineering and Analytics pipeline. It covers everything from raw data ingestion to a high-performance interactive dashboard, transforming scattered information into actionable business insights using modern tools.

---

## 🏗️ Project Architecture

The data workflow is organized into four main stages:

1.  **Ingestion & Local Processing:** Leveraging **DuckDB** for high-performance SQL processing of raw files, consolidating them into a local analytical database.
2.  **ETL Orchestration:** Python-based scripts for data cleaning, transformation, and normalization.
3.  **Cloud Data Warehouse:** Processed data is synced to **Supabase (PostgreSQL)** to ensure cloud availability and scalability.
4.  **Business Intelligence:** An interactive dashboard built with **Streamlit** and **Plotly**, featuring real-time metrics and dynamic filtering.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **OLAP Engine:** [DuckDB](https://duckdb.org/) (In-process analytical database).
* **Cloud Database:** [Supabase](https://supabase.com/) (PostgreSQL).
* **Visualization:** [Streamlit](https://streamlit.io/) & [Plotly](https://plotly.com/python/).
* **Data Manipulation:** Pandas.
* **Environment Management:** `python-dotenv` for secure credential handling.

---

## 🚀 Key Features

* **Executive Metrics:** Instant visibility of Total Records, Total Sales, and Units Sold.
* **Interactive Filtering:** Sidebar-controlled filters for **Region** and **Date Range**.
* **Advanced Visuals:** * Dynamic bar charts with consistent regional color-coding.
    * Donut charts showing percentage market share per region.
* **Customer Rankings:** Automated Top 10 Customers list (Name, Last Name, and Revenue).
* **Granular Data Access:** Full data table sorted by sales volume (Units).

---

## 📂 Repository Structure

Based on the [Modern Data Stack] framework:

```text
modern-data-stack/
├── duckdb/              # Local database storage (.db files)
├── queries/             # SQL transformation scripts
├── screenshots/         # Visual documentation of the dashboard
├── scripts/             # Python ETL logic (Extraction, Transformation, Loading)
├── sources/             # Raw data files (CSV, JSON, etc.)
├── streamlit/           # Frontend dashboard code (app.py)
├── supabase/            # Cloud configuration and schema logs
├── .env                 # Environment variables (API Keys, DB URLs) - [HIDDEN]
├── .gitignore           # Git exclusion rules
└── requirements.txt     # Project dependencies
