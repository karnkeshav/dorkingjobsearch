import json
import logging
import os
import requests
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    with open('config/settings.json', 'r') as f:
        return json.load(f)

CONFIG = load_config()

def build_query():
    # site:linkedin.com/jobs (Director OR Head OR Principal) (Platform OR Cloud OR SRE OR DevOps) (India OR Remote)
    titles = " OR ".join([f'"{t}"' for t in CONFIG['keywords']['titles']])
    domains = " OR ".join([f'"{d}"' for d in CONFIG['keywords']['domains']])
    locations = " OR ".join([f'"{l}"' for l in CONFIG['keywords']['locations']])

    query = f'site:linkedin.com/jobs ({titles}) ({domains}) ({locations})'
    return query

def search_google_api(api_key, cx, query):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        # Fetch up to 20 results (2 pages)
        all_items = []
        for start_index in [1, 11]:
            res = service.cse().list(q=query, cx=cx, start=start_index).execute()
            items = res.get('items', [])
            all_items.extend(items)
            if len(items) < 10:
                break
        return all_items
    except HttpError as e:
        logging.error(f"Google API Error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected Google API Error: {e}")
        return None

def fallback_search(query):
    logging.warning("Falling back to HTML scraping (Not fully implemented to avoid bans, logging instruction).")
    logging.info("To enable robust fallback, consider using 'googlesearch-python' or similar libraries cautiously.")
    logging.info(f"Manual check link: https://www.google.com/search?q={requests.utils.quote(query)}")
    return []

def run():
    api_key = os.environ.get('GOOGLE_API_KEY')
    cx = os.environ.get('GOOGLE_CX_ID') # Or from config if not secret

    if not cx:
        # Fallback to config if not in env
        cx = CONFIG.get('search_config', {}).get('google_cx')

    query = build_query()
    logging.info(f"Google X-Ray Query: {query}")

    results = []

    if api_key and cx and cx != "YOUR_GOOGLE_CX_ID":
        logging.info("Using Google Custom Search API")
        api_results = search_google_api(api_key, cx, query)
        if api_results is not None:
            for item in api_results:
                results.append({
                    "title": item.get('title'),
                    "link": item.get('link'),
                    "snippet": item.get('snippet'),
                    "source": "Google X-Ray"
                })
        else:
            logging.warning("Google API failed, attempting fallback.")
            results.extend(fallback_search(query))
    else:
        logging.warning("Google API Key or CX ID missing/invalid. Using fallback.")
        if not api_key:
             logging.info("Instruction: Get a free Google Custom Search API key at https://developers.google.com/custom-search/v1/overview")
        results.extend(fallback_search(query))

    return results

if __name__ == "__main__":
    jobs = run()
    print(json.dumps(jobs, indent=2))
