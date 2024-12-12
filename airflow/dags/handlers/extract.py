from utils.common import get_news_api_key
import requests
from newsapi import NewsApiClient
from datetime import datetime, timedelta

def formatDateString(date: datetime):
    return date.strftime("%Y-%m-%d")

def getTodayString():
    today = datetime.now()
    return formatDateString(today)

def getYesterdayString():
    yesterday = datetime.now() - timedelta(1)
    return formatDateString(yesterday)

def fetch_top_headlines(**kwargs):
    print("Fetching top articles...")
    API_KEY = get_news_api_key()
    if API_KEY is None:
        print("[ERROR] API_KEY is not set.")
        return

    try:
        newsapi = NewsApiClient(api_key=API_KEY)
        top_headlines = newsapi.get_top_headlines()
        if top_headlines["status"] != "ok":
            print(f"[ERROR] error fetching articles: {top_headlines.status}")
            return

        kwargs["ti"].xcom_push(
            key="top_headlines", value=top_headlines
        )  # push data to xcom for other tasks to access
    except requests.exceptions.RequestException as e:
        print("[ERROR] ", e)


def fetch_recent_articles(**kwargs):
    print("Fetching recent articles...")
    API_KEY = get_news_api_key()
    if API_KEY is None:
        print("[ERROR] API_KEY is not set.")
        return

    try:
        newsapi = NewsApiClient(api_key=API_KEY)
        recent_articles = newsapi.get_everything(
            from_param=getTodayString(),
            to=getYesterdayString(),
            language="en",
            sort_by="popularity",
        )
        if recent_articles["status"] != "ok":
            print(f"[ERROR] error fetching articles: {recent_articles.status}")
            return

        kwargs["ti"].xcom_push(
            key="recent_articles", value=recent_articles
        )  # push data to xcom for other tasks to access
    except requests.exceptions.RequestException as e:
        print("[ERROR] ", e)
