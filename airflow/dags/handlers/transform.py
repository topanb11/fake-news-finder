import datetime
import utils.topic as topic
from pprint import pprint

def convert_to_datetime(iso: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(iso)


def clean_article_source(source: dict) -> str:
    cleaned_source = source['name']
    return cleaned_source if cleaned_source != '[Removed]' else 'INDIVIDUAL'
        

def transform_articles(**kwargs):
    print("[LOG] Transforming articles...")
    
    api_data = kwargs["ti"].xcom_pull(
        task_ids="fetch_top_headlines", key="top_headlines"
    )
    
    all_articles = api_data['articles']
    
    cleaned_articles = []
    for article in all_articles:
        # skip over removed articles
        if article['title'] == '[Removed]':
            continue
        
        cleaned_article = {
            # TODO: Replace with actual algorithm to determine topic later
            'topic': topic.determine_article_topic(
                title=article['title'],
                description=article['description'],
            ),
            'title': article['title'],
            'description': article['description'],
            'source': clean_article_source(article['source']),
            'author': article['author'],
            'published_date': convert_to_datetime(article['publishedAt']),
        }
        cleaned_articles.append(cleaned_article)
    
    kwargs['ti'].xcom_push(
        key='cleaned_trending_data', value=cleaned_articles
    )
    print('[LOG] Finished transforming articles')
