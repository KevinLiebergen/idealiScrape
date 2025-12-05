from telegram import Bot
import asyncio

async def send_message(token, chat_id, message):
    """Send a message to Telegram channel."""
    if not token or not chat_id:
        print("Telegram token or chat_id missing.")
        return

    bot = Bot(token=token)
    try:
        async with bot:
            await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
