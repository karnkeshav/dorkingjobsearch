import json
import logging
import os
import requests
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    with open('config/settings.json', 'r') as f:
        return json.load(f)

CONFIG = load_config()

def build_query():
    titles = " OR ".join([f'"{t}"' for t in CONFIG['keywords']['titles']])
    domains = " OR ".join([f'"{d}"' for d in CONFIG['keywords']['domains']])
    locations = " OR ".join([f'"{l}"' for l in CONFIG['keywords']['locations']])

    query = f'site:linkedin.com/jobs ({titles}) ({domains}) ({locations})'
    return query

def search_bing_api(api_key, query):
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": 20, "offset": 0}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('webPages', {}).get('value', [])
    except requests.exceptions.HTTPError as e:
        logging.error(f"Bing API Error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected Bing API Error: {e}")
        return None

def fallback_bing_search(query):
    logging.warning("Falling back to Bing scraping (Not fully implemented, logging instruction).")
    logging.info(f"Manual Bing link: https://www.bing.com/search?q={requests.utils.quote(query)}")
    return []

def run():
    api_key = os.environ.get('BING_API_KEY')
    if not api_key:
        api_key = CONFIG.get('search_config', {}).get('bing_subscription_key')

    query = build_query()
    logging.info(f"Bing X-Ray Query: {query}")

    results = []

    if api_key and api_key != "YOUR_BING_KEY":
        logging.info("Using Bing Search API")
        api_results = search_bing_api(api_key, query)
        if api_results is not None:
            for item in api_results:
                results.append({
                    "title": item.get('name'),
                    "link": item.get('url'),
                    "snippet": item.get('snippet'),
                    "source": "Bing X-Ray"
                })
        else:
             logging.warning("Bing API failed, attempting fallback.")
             results.extend(fallback_bing_search(query))
    else:
        logging.warning("Bing API Key missing/invalid. Using fallback.")
        logging.info("Instruction: Get a free Bing Search API key at https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/")
        results.extend(fallback_bing_search(query))

    return results

if __name__ == "__main__":
    jobs = run()
    print(json.dumps(jobs, indent=2))
