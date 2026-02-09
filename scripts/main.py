import logging
import json
import os
import pytz
from datetime import datetime
import asyncio
import sys

# Add the parent directory (project root) to sys.path so we can import 'scripts'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.google_xray import run as run_google
from scripts.bing_xray import run as run_bing
from scripts.career_crawler import run as run_crawler
from scripts.dedupe import deduplicate
from scripts.notifier import send_telegram_digest

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'settings.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def check_time_window(config):
    try:
        tz = pytz.timezone(config.get('timezone', 'UTC'))
        now = datetime.now(tz)

        schedule = config.get('schedule_window', {})
        start = schedule.get('start_hour', 9)
        end = schedule.get('end_hour', 23)

        logging.info(f"Checking time window: Now {now.hour}:{now.minute} ({tz}). Allowed: {start}-{end}")

        if start <= now.hour < end:
            return True

        logging.info("Outside active window. Exiting.")
        return False
    except Exception as e:
        logging.error(f"Time check failed: {e}. Defaulting to proceed.")
        return True

async def orchestrate():
    config = load_config()

    # Time window check
    if not check_time_window(config):
        logging.info("Current time is outside the active window. Exiting.")
        return

    all_jobs = []

    # 1. Google X-Ray
    try:
        logging.info("Starting Google X-Ray...")
        google_jobs = run_google()
        logging.info(f"Google X-Ray found {len(google_jobs)} jobs.")
        all_jobs.extend(google_jobs)
    except Exception as e:
        logging.error(f"Google X-Ray failed: {e}")

    # 2. Bing X-Ray
    try:
        logging.info("Starting Bing X-Ray...")
        bing_jobs = run_bing()
        logging.info(f"Bing X-Ray found {len(bing_jobs)} jobs.")
        all_jobs.extend(bing_jobs)
    except Exception as e:
        logging.error(f"Bing X-Ray failed: {e}")

    # 3. Career Site Crawler
    try:
        logging.info("Starting Career Site Crawler...")
        site_jobs = run_crawler()
        logging.info(f"Career Site Crawler found {len(site_jobs)} jobs.")
        all_jobs.extend(site_jobs)
    except Exception as e:
        logging.error(f"Career Site Crawler failed: {e}")

    logging.info(f"Total raw jobs found: {len(all_jobs)}")

    # 4. Deduplicate
    unique_jobs = deduplicate(all_jobs)

    if not unique_jobs:
        logging.info("No new unique jobs found.")
        return

    # 5. Notify
    try:
        logging.info(f"Sending notification for {len(unique_jobs)} new jobs...")
        await send_telegram_digest(unique_jobs)
    except Exception as e:
        logging.error(f"Notification failed: {e}")

    logging.info("Orchestration Run Complete.")

def main():
    asyncio.run(orchestrate())

if __name__ == "__main__":
    main()
