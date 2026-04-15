markdown# 🔄 Data Engineering Pipeline — Olist E-Commerce

ETL pipeline built with Apache Airflow, Pandas and PostgreSQL using the 
Brazilian E-Commerce dataset (Olist, 2016–2018).

## 🏗️ Architecture
CSV Files (9 tables)
↓
Apache Airflow (orchestration)
↓
extract() → transform() → load()
↓
PostgreSQL (data warehouse)
↓
SQL Analysis (JOINs, Window Functions, CTEs)

## 🛠️ Tech Stack

- **Orchestration:** Apache Airflow 2.9
- **Data processing:** Python, Pandas
- **Storage:** PostgreSQL
- **Infrastructure:** Docker, Docker Compose
- **Analysis:** SQL (Window Functions, CTEs, JOINs)

## 📁 Project Structure
├── airflow/
│   └── dags/
│       └── etl_olist.py      # Airflow DAG (extract → transform → load)
├── notebooks/
│   ├── 01_ETL.ipynb          # ETL development and exploration
│   ├── 02_sql_queries.ipynb  # SQL study guide
│   └── 03_sql_analysis.ipynb # Business analysis queries
├── data/
│   └── raw/                  # Source CSVs (not included in repo)
└── README.md

## ⚙️ Setup

### Prerequisites
- Docker Desktop
- PostgreSQL
- Python 3.9+

### Run the pipeline

```bash
# 1. Clone the repository
git clone https://github.com/tu_usuario/data-engineering-olist.git
cd data-engineering-olist

# 2. Start Airflow
cd airflow
docker compose up -d

# 3. Open Airflow UI
http://localhost:8080 (user: airflow / pass: airflow)

# 4. Trigger the DAG manually or wait for daily schedule
```

## 📊 Analysis highlights

- **96,478** delivered orders analyzed
- Average delivery time: **12 days**
- Worst performing state: **Amazonas (AM)** with 26 days average
- Payment method breakdown: 76% credit card
- Black Friday 2017 peak: **+2,811 orders** vs previous month

## 📂 Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)