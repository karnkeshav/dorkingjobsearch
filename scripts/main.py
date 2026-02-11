import logging
import json
import os
import pytz
from datetime import datetime
import asyncio
import sys

# Add the parent directory (project root) to sys.path so we can import 'scripts'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imports for job discovery
from scripts.career_crawler import run as run_crawler
from scripts.google_alerts_ingest import run as run_alerts

from scripts.dedupe import deduplicate
from scripts.notifier import send_telegram_digest

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'settings.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def check_time_window(config):
    # ADDED: Manual trigger bypass for testing
    if os.environ.get('IGNORE_TIME_WINDOW') == 'true':
        logging.info("Manual trigger detected: Bypassing time window check.")
        return True

    try:
        tz = pytz.timezone(config.get('timezone', 'Asia/Kolkata'))
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

    # 1. Career Site Crawler (Primary Source)
    try:
        logging.info("Starting Career Site Crawler...")
        site_jobs = run_crawler()
        logging.info(f"Career Site Crawler found {len(site_jobs)} jobs.")
        all_jobs.extend(site_jobs)
    except Exception as e:
        logging.error(f"Career Site Crawler failed: {e}")

    # 2. Google Alerts Ingestion (Secondary Source)
    try:
        logging.info("Starting Google Alerts Ingestion...")
        alert_jobs = run_alerts()
        logging.info(f"Google Alerts found {len(alert_jobs)} jobs.")
        all_jobs.extend(alert_jobs)
    except Exception as e:
        logging.error(f"Google Alerts Ingestion failed: {e}")

    logging.info(f"Total raw jobs found: {len(all_jobs)}")

    # 3. Deduplicate
    unique_jobs = deduplicate(all_jobs)

    if not unique_jobs:
        logging.info("No new unique jobs found.")
        return

    # 4. Notify
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
