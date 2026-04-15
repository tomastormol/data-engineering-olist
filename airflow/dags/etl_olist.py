from datetime import datetime
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from io import StringIO
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

DATA_PATH = Path("/opt/airflow/data/raw")
DB_URL = "postgresql://tomas@host.docker.internal:5432/data_engineering"

def extract(ti):
    """Lee los CSVs UNA sola vez y los pasa a la siguiente tarea"""
    orders = pd.read_csv(DATA_PATH / "olist_orders_dataset.csv")
    customers = pd.read_csv(DATA_PATH / "olist_customers_dataset.csv")
    payments = pd.read_csv(DATA_PATH / "olist_order_payments_dataset.csv")

    # Pasar los datos a la siguiente tarea via XCom
    ti.xcom_push(key="orders", value=orders.to_json())
    ti.xcom_push(key="customers", value=customers.to_json())
    ti.xcom_push(key="payments", value=payments.to_json())

    print(f"✅ Extract: {len(orders):,} orders, {len(customers):,} customers, {len(payments):,} payments")

def transform(ti):
    """Recibe los datos de extract, limpia y transforma"""
    # Recuperar datos de la tarea anterior
    orders = pd.read_json(StringIO(ti.xcom_pull(key="orders", task_ids="extract")))

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for col in date_columns:
        orders[col] = pd.to_datetime(orders[col])

    orders_clean = orders[orders["order_status"] == "delivered"].copy()
    orders_clean["delivery_days"] = (
        orders_clean["order_delivered_customer_date"] -
        orders_clean["order_purchase_timestamp"]
    ).dt.days

    # Pasar datos limpios a load()
    ti.xcom_push(key="orders_clean", value=orders_clean.to_json())

    print(f"✅ Transform: {len(orders_clean):,} pedidos entregados")

def load(ti):
    """Recibe los datos limpios y los carga en PostgreSQL"""
    engine = create_engine(DB_URL)

    # Recuperar datos de las tareas anteriores
    orders_clean = pd.read_json(StringIO(ti.xcom_pull(key="orders_clean", task_ids="transform")))
    customers = pd.read_json(StringIO(ti.xcom_pull(key="customers", task_ids="extract")))
    payments = pd.read_json(StringIO(ti.xcom_pull(key="payments", task_ids="extract")))

    orders_clean.to_sql("orders", engine, if_exists="replace", index=False, chunksize=1000)
    customers.to_sql("customers", engine, if_exists="replace", index=False, chunksize=1000)
    payments.to_sql("payments", engine, if_exists="replace", index=False, chunksize=1000)

    print(f"✅ Load: tablas cargadas en PostgreSQL")

with DAG(
    dag_id="etl_olist",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["olist", "etl"],
) as dag:

    task_extract = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )

    task_transform = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )

    task_load = PythonOperator(
        task_id="load",
        python_callable=load,
    )

    task_extract >> task_transform >> task_load