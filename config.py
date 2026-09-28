import os

from dotenv import load_dotenv


load_dotenv(override=True)

BASE_URL = os.getenv("BASE_URL")
X_API_KEY = os.getenv("X_API_KEY")