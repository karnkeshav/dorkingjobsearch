import logging
import os
import requests
import json
import asyncio

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

    count = 0
    for job in jobs:
        if count >= 15: # Limit per run to avoid spam/limits
            message += f"\n...and {len(jobs) - count} more."
            break

        # Clean title and handle potential None values
        title = job.get('title', 'Unknown Role')
        company = job.get('company', 'Unknown Company')
        source = job.get('source', 'Unknown Source')
        link = job.get('link', '#')

        item = f"*{count + 1}. {title}*\n"
        item += f"   Company: {company}\n"
        item += f"   Source: {source}\n"
        item += f"   [Link]({link})\n\n"

        # Check message length limit (Telegram max is 4096)
        if len(message) + len(item) > 4000:
            await _send_raw(bot_token, chat_id, message)
            message = ""

        message += item
        count += 1

    if message:
        await _send_raw(bot_token, chat_id, message)

async def _send_raw(token, chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        # Using requests synchronously inside async wrapper is fine for this scale
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
        {"title": "Director of Engineering", "company": "Test Corp", "source": "Test", "link": "http://example.com"}
    ]
    notify(test_jobs)
