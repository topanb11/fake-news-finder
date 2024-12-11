from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from handlers.extract import fetch_top_headlines
from handlers.load import load_articles
from handlers.transform import transform_articles

# Define default arguments
default_args = {
    "owner": "airflow", 
    "depends_on_past": False, # task can run even if prev instance has not completed
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1, # num of retries for task if it fails
    "retry_delay": timedelta(minutes=5),
}

# Initialize the DAG
dag = DAG(
    "trending_news_dag",  # DAG ID
    default_args=default_args,
    description="DAG used to for ETL of trending news articles daily",
    schedule_interval=timedelta(days=1),  # run DAG daily
    start_date=datetime(2024, 1, 1),  # when to start DAG
    catchup=False, # don't backfill data
)

# Add tasks to the DAG
extract_task = PythonOperator(
    task_id="fetch_top_headlines",
    python_callable=fetch_top_headlines,
    dag=dag,
)

transform_task = PythonOperator(
    task_id="transform_articles",
    python_callable=transform_articles,
    dag=dag,
)

load_task = PythonOperator(
    task_id="load_articles",
    python_callable=load_articles,
    dag=dag,
)

# Define task dependencies
extract_task >> transform_task >> load_task  # fetch articles before transforming
