from utils.common import get_news_api_key
import requests

def fetch_top_headlines(**kwargs):
    print("Fetching top articles...")
    API_KEY = get_news_api_key()
    if API_KEY is None:
        print("[ERROR] API_KEY is not set.")
        return

    try:
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
        )

        if response.status_code != 200:
            print(f"[ERROR] error fetching articles: {response.status_code}")
            return

        data = response.json()
        kwargs["ti"].xcom_push(
            key="trending_data", value=data
        )  # push data to xcom for other tasks to access
    except requests.exceptions.RequestException as e:
        print("[ERROR] ", e)
