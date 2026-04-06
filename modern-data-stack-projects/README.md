# 🚀 Modern Data Stack Lab: Evidence + DuckDB + Supabase

This project is a high-performance, **BI-as-Code** laboratory designed to demonstrate the integration of modern data tools for agile analytics. It moves away from traditional drag-and-drop BI to a more scalable, version-controlled approach.

## 🛠️ The Stack

* **Storage:** [Supabase](https://supabase.com/) (PostgreSQL) as the cloud data warehouse.
* **Processing Engine:** [DuckDB](https://duckdb.org/) for lightning-fast local analytical processing and data transformation.
* **Visualization:** [Evidence.dev](https://evidence.dev/) for building scorched-earth fast, SQL-based data products.
* **Language:** SQL & Markdown.

---

## 🏗️ Architecture

The pipeline follows a modern "Lite" architecture:
1.  **Ingestion:** Raw data is hosted in **Supabase** (PostgreSQL).
2.  **Transformation:** **DuckDB** connects to the source to perform complex aggregations and filtering locally, ensuring high speed and low cloud costs.
3.  **Reporting:** **Evidence** renders the final insights using a "BI-as-Code" approach, allowing the entire dashboard to be version-controlled via Git.

---

## 🌟 Key Features

* **Zero-Latency Dashboards:** Leveraging DuckDB's columnar storage for instant reporting.
* **SQL-First Workflow:** All business logic is defined in pure SQL, ensuring transparency and reusability.
* **Version Control:** Unlike traditional `.pbix` files, the entire project consists of plain text files, making code reviews and collaboration seamless.
* **Automated Deployment:** CI/CD ready for platforms like Vercel or Netlify.
