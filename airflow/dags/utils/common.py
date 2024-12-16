import os
from dotenv import load_dotenv

def get_env_variable(key: str):
    load_dotenv()
    return os.environ.get(key)
