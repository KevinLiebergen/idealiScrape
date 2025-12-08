from telegram import Bot
import asyncio
from .logger import logger

from telegram.request import HTTPXRequest

async def send_message(token, chat_id, message):
    """Send a message to Telegram channel."""
    if not token or not chat_id:
        logger.error("Telegram token or chat_id missing.")
        return

    # Ignore environment variables (proxies)
    request = HTTPXRequest(httpx_kwargs={"trust_env": False})
    bot = Bot(token=token, request=request)
    try:
        async with bot:
            await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
