from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Step 1: Define the default arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Step 2: Initialize the DAG
dag = DAG(
    "simple_dag",  # DAG ID
    default_args=default_args,
    description="A simple DAG example",
    schedule_interval=timedelta(days=1),  # Runs daily
    start_date=datetime(2024, 1, 1),  # Start date
    catchup=False,  # Prevent backfilling
)


# Step 3: Define Python functions for tasks
def task_1():
    print("Task 1 executed!")


def task_2():
    print("Task 2 executed!")


# Step 4: Add tasks to the DAG
task1 = PythonOperator(
    task_id="task_1",  # Unique ID for the task
    python_callable=task_1,  # Function to execute
    dag=dag,  # Reference to the DAG
)

task2 = PythonOperator(
    task_id="task_2",
    python_callable=task_2,
    dag=dag,
)

# Step 5: Define task dependencies
task1 >> task2  # task1 runs before task2
