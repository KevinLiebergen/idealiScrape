import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# src/settings.py -> src/ -> project_root
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

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
