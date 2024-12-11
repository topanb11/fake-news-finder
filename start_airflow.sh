export AIRFLOW_HOME="$(pwd)/airflow"
export NO_PROXY="*" # Necessary fix for M1 mac
airflow standalone