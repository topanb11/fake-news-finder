from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from handlers.extract import fetch_top_headlines, fetch_recent_articles
from handlers.load_s3 import load_s3_with_raw_articles
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
    task_id="fetch_articles",
    python_callable=fetch_recent_articles,
    dag=dag,
)

load_s3_task = PythonOperator(
    task_id="load_s3_with_raw_articles",
    python_callable=load_s3_with_raw_articles,
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
extract_task >> load_s3_task >> transform_task >> load_task  # fetch articles before transforming
