import os

from dotenv import load_dotenv
from newsapi import NewsApiClient
from pprint import pprint

load_dotenv()

news_api_key = os.environ.get('NEWS_API_KEY')
news_api_client = NewsApiClient(api_key=news_api_key)

all_articles = news_api_client.get_everything(
  q='apple',
  language='en',
)

pprint(all_articles)
