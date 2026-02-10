import json
import logging
import feedparser
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    with open('config/settings.json', 'r') as f:
        return json.load(f)

CONFIG = load_config()

def parse_alert_feed(url):
    try:
        logging.info(f"Ingesting Google Alert Feed: {url}")
        feed = feedparser.parse(url)

        if feed.bozo:
            logging.warning(f"Feed parser reported error for {url}: {feed.bozo_exception}")

        jobs = []
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            summary = entry.summary
            published = entry.published

            # Google Alerts format titles like: "Keyword - Source" or just "Title"
            # We try to extract cleaner title if possible, or just use raw.
            # Usually titles are HTML bolded in summary, but feed title is plain text.

            # Basic filtering on title/summary
            if is_target_job(title) or is_target_job(summary):
                jobs.append({
                    "title": title, # Raw title from alert
                    "company": "Google Alert", # Hard to extract reliably without scraping link
                    "location": "Unknown", # Alerts don't always have location
                    "link": link,
                    "source": "Google Alerts",
                    "published": published
                })

        logging.info(f"Found {len(jobs)} potential jobs in alert feed.")
        return jobs

    except Exception as e:
        logging.error(f"Error parsing Google Alert feed {url}: {e}")
        return []

def is_target_job(text):
    if not text:
        return False

    text_lower = text.lower()

    # Check Keywords (Title + Domain)
    # Since alerts are user-configured, they might already be filtered.
    # But we double-check to be safe.

    has_title = any(t.lower() in text_lower for t in CONFIG['keywords']['titles'])
    has_domain = any(d.lower() in text_lower for d in CONFIG['keywords']['domains'])

    return has_title and has_domain

def run():
    all_jobs = []

    alerts_config = CONFIG.get('google_alerts', {})
    if not alerts_config.get('enabled', False):
        logging.info("Google Alerts ingestion disabled in config.")
        return []

    feed_urls = alerts_config.get('feed_urls', [])
    if not feed_urls:
        logging.info("No Google Alert feed URLs configured.")
        return []

    for url in feed_urls:
        jobs = parse_alert_feed(url)
        all_jobs.extend(jobs)

    return all_jobs

if __name__ == "__main__":
    # Test with dummy feed if no config
    # In real usage, user puts URL in config
    jobs = run()
    print(json.dumps(jobs, indent=2))
