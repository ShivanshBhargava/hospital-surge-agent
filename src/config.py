import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HOSPITAL_DB_URL = os.getenv("HOSPITAL_DB_URL")
POLLUTION_API_KEY = os.getenv("POLLUTION_API_KEY")
