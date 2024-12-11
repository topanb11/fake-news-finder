def transform_articles(**kwargs):
    print("Transforming articles...")
    api_data = kwargs["ti"].xcom_pull(
        task_ids="fetch_top_headlines", key="trending_data"
    )
    print(api_data)
