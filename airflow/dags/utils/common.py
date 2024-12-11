import os
from dotenv import load_dotenv

def get_news_api_key():
    load_dotenv()
    return os.getenv("NEWS_API_KEY")
