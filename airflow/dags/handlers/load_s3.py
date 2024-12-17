import boto3
import json

from datetime import datetime
from utils.common import get_env_variable

def load_s3_with_raw_articles(**kwargs):
  print("[LOG] Loading data into S3...")

  api_data = kwargs["ti"].xcom_pull(task_ids="fetch_articles", key="news_data")
  all_headlines = api_data['articles']
  
  aws_access_key_id = get_env_variable('AWS_ACCESS_KEY_ID')
  aws_secret_access_key = get_env_variable('AWS_SECRET_ACCESS_KEY')
  region = 'us-east-1'

  s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region,
  )
  
  bucket_name = 'trend-finder-article-bucket'
  now = datetime.now()
  now_string = now.strftime('%Y-%m-%d %I:%M: %p')
  # adding today's date to make file names unique
  file_name = f'raw articles - {now_string}'
  
  s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(all_headlines))
  
  print(f'[LOG] Done loading data into S3 bucket: {bucket_name}')
