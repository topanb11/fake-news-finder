import datetime
import utils.topic as topic


def convert_to_datetime(iso: str) -> datetime.datetime:
    iso = iso.replace('Z', '+00:00')
    return datetime.datetime.fromisoformat(iso)


def clean_article_source(source: dict) -> str:
    cleaned_source = source['name']
    return cleaned_source if cleaned_source != '[Removed]' else 'INDIVIDUAL'


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
        cleaned_article = {
            # TODO: Replace with actual algorithm to determine topic later
            'topic': topic.determine_article_topic(
                title=article['title'],
                description=article['description'],
            ),
            'title': article['title'],
            'description': article['description'],
            'source_id': cleaned_source.lower(),
            'source_name': cleaned_source,
            'author': article['author'],
            'published_date': convert_to_datetime(article['publishedAt']),
        }
        cleaned_articles.append(cleaned_article)

    kwargs['ti'].xcom_push(
        key='cleaned_headlines', value=cleaned_articles
    )
    print('[LOG] Finished transforming articles')
