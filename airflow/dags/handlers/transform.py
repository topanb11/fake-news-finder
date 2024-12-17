import datetime
import hashlib
import utils.topic as topic
from textblob import TextBlob


def hash_article_id(title: str) -> str:
    hash_obj = hashlib.sha256()
    hash_obj.update(title.encode('utf-8'))
    return hash_obj.hexdigest()


def convert_to_datetime(iso: str) -> datetime.datetime:
    iso = iso.replace('Z', '+00:00')
    return datetime.datetime.fromisoformat(iso)


def clean_article_source(source: dict) -> str:
    cleaned_source = source['name']
    return cleaned_source if cleaned_source != '[Removed]' else 'INDIVIDUAL'

def get_article_sentiment_analysis(title: str, description: str):
    # Polarity [-1.0 - 1.0]:
    #   -1 = negative
    #    0 = neutral
    #    1 = positive
    # Subjectivity [0.0 - 1.0]:
    #    0 = objective
    #    1 = subjective
    blob = TextBlob(title)
    polarity, subjectivity = blob.sentiment  # Returns a tuple (polarity, subjectivity)
    return polarity, subjectivity

def transform_articles(**kwargs):
    print("[LOG] Transforming articles...")

    api_data = kwargs["ti"].xcom_pull(task_ids="fetch_articles", key="news_data")

    all_headlines = api_data['articles']
    cleaned_articles = []
    for article in all_headlines:
        # skip over removed articles
        if article['title'] == '[Removed]':
            continue

        cleaned_source = clean_article_source(article['source'])
        polarity, subjectivity = get_article_sentiment_analysis(article['title'], article['description'])
        cleaned_article = {
            "article_id": hash_article_id(article["title"]),
            "topic": topic.determine_article_topic(
                title=article["title"],
                description=article["description"],
            ),
            "title": article["title"],
            "description": article["description"],
            "source_id": cleaned_source.lower(),
            "source_name": cleaned_source,
            "author": article["author"],
            "published_date": convert_to_datetime(article["publishedAt"]),
            "polarity": polarity,
            "subjectivity": subjectivity
        }
        cleaned_articles.append(cleaned_article)

    kwargs['ti'].xcom_push(
        key='cleaned_headlines', value=cleaned_articles
    )
    print('[LOG] Finished transforming articles')
