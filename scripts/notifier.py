import logging
import os
import requests
import json
import asyncio
from telegram import Bot

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def send_telegram_digest(jobs):
    if not jobs:
        logging.info("No new jobs to notify.")
        return

    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    if not bot_token or not chat_id:
        logging.warning("Telegram Bot Token or Chat ID missing. Notification skipped.")
        logging.info("Check README for setup instructions.")
        return

    message = "🔔 *New Director-Level Jobs Detected*\n\n"

    # Telegram has a message length limit (4096 chars). Split if necessary.
    # For now, we'll just take the top 10 to be safe, or split logic can be added.

    count = 0
    for job in jobs:
        if count >= 15: # Limit per run to avoid spam/limits
            message += f"\n...and {len(jobs) - count} more."
            break

        item = f"*{count + 1}. {job.get('title')}*\n"
        if job.get('company') and job.get('company') != 'Unknown':
            item += f"   Company: {job.get('company')}\n"
        item += f"   Source: {job.get('source')}\n"
        item += f"   [Link]({job.get('link')})\n\n"

        if len(message) + len(item) > 4000:
            # Send current chunk and start new
            await _send_raw(bot_token, chat_id, message)
            message = ""

        message += item
        count += 1

    if message:
        await _send_raw(bot_token, chat_id, message)

async def _send_raw(token, chat_id, text):
    try:
        # Using requests directly or python-telegram-bot
        # Since python-telegram-bot is async, let's use requests for simplicity if we don't need complex bot features
        # Or use the library properly.

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logging.info("Telegram notification sent.")
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {e}")

def notify(jobs):
    # Wrapper for sync calls
    asyncio.run(send_telegram_digest(jobs))

if __name__ == "__main__":
    # Test notification
    test_jobs = [
        {"title": "Director of Engineering", "source": "Test", "link": "http://example.com"}
    ]
    notify(test_jobs)
