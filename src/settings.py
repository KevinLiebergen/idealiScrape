import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Settings
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

IDEALISTA_API_KEY = os.getenv("IDEALISTA_API_KEY")
IDEALISTA_API_SECRET = os.getenv("IDEALISTA_API_SECRET")

# Validation
if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    print("[-] Warning: Telegram credentials not found in .env")

if not IDEALISTA_API_KEY or not IDEALISTA_API_SECRET:
    print("[-] Warning: Idealista API credentials not found in .env")
