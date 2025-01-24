from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
HF_KEY = os.getenv("HF_KEY")
