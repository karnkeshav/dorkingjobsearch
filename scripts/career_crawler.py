import json
import logging
import requests
from bs4 import BeautifulSoup
import re
import random
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    with open('config/settings.json', 'r') as f:
        return json.load(f)

CONFIG = load_config()

# User-Agent rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]

def get_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

def crawl_site(url):
    try:
        logging.info(f"Crawling {url}")

        # Simple rate limiting logic (random sleep)
        time.sleep(random.uniform(1, 3))

        response = requests.get(url, headers=get_headers(), timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        jobs = []

        # 1. Look for JSON-LD JobPosting
        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            try:
                content = script.string
                if not content:
                    continue

                data = json.loads(content)

                # Normalize to list
                items = []
                if isinstance(data, dict):
                    if data.get('@graph'):
                        items = data['@graph']
                    else:
                        items = [data]
                elif isinstance(data, list):
                    items = data

                for item in items:
                    if isinstance(item, dict) and item.get('@type') == 'JobPosting':
                        parsed = parse_json_ld(item)
                        if parsed and is_target_job(parsed['title'], parsed.get('location', '')):
                            jobs.append(parsed)

            except json.JSONDecodeError:
                continue
            except Exception as e:
                logging.warning(f"Error parsing JSON-LD snippet on {url}: {e}")
                continue

        # 2. Fallback: Simple keyword search in links
        if not jobs:
            logging.info(f"No valid JSON-LD jobs found on {url}, falling back to link scanning.")
            for link in soup.find_all('a', href=True):
                title = link.get_text(strip=True)
                href = link['href']

                # Simple check to avoid navigation links
                if len(title) > 100 or len(title) < 5:
                    continue

                if is_target_job(title):
                    full_link = href if href.startswith('http') else url.rstrip('/') + '/' + href.lstrip('/')
                    jobs.append({
                        "title": title,
                        "company": "Unknown", # Often can be inferred from URL or site
                        "location": "See Link",
                        "link": full_link,
                        "source": f"Career Site: {url}"
                    })

        return jobs

    except requests.exceptions.RequestException as e:
        logging.error(f"Error crawling {url}: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error crawling {url}: {e}")
        return []

def parse_json_ld(data):
    try:
        title = data.get('title')
        if not title:
            return None

        company = data.get('hiringOrganization', {}).get('name', 'Unknown')

        # Handle location which can be complex object
        loc_data = data.get('jobLocation', {})
        location = "Unknown"
        if isinstance(loc_data, dict):
            address = loc_data.get('address')
            if isinstance(address, dict):
                location = address.get('addressLocality', 'Unknown')
            elif isinstance(address, str):
                location = address

        return {
            "title": title,
            "company": company,
            "location": location,
            "link": data.get('url', ''),
            "source": "JSON-LD"
        }
    except Exception as e:
        logging.warning(f"Error parsing JSON-LD item: {e}")
        return None

def is_target_job(title, location=""):
    if not title:
        return False

    title_lower = title.lower()
    loc_lower = location.lower()

    has_title = any(t.lower() in title_lower for t in CONFIG['keywords']['titles'])
    has_domain = any(d.lower() in title_lower for d in CONFIG['keywords']['domains'])
    
    # NEW LOGIC: Pass if location is found OR if it's a fallback "See Link"
    target_locations = CONFIG['keywords']['locations']
    has_location = any(l.lower() in title_lower or l.lower() in loc_lower for l in target_locations)
    
    is_fallback = "see link" in loc_lower
    
    return has_title and has_domain and (has_location or is_fallback)
    

    title_lower = title.lower()
    loc_lower = location.lower()

    # Check Title Keywords
    has_title = any(t.lower() in title_lower for t in CONFIG['keywords']['titles'])

    # Check Domain Keywords
    has_domain = any(d.lower() in title_lower for d in CONFIG['keywords']['domains'])

    # Check Location (if provided, otherwise assume flexible)
    # The prompt says: "Location must include: India or Remote"
    # But usually location is checked against the job object, here we check title/location string
    # If location is unknown/empty in fallback, we might be lenient or strict.
    # Let's check if "India" or "Remote" is in title OR location string if available

    target_locations = CONFIG['keywords']['locations']
    has_location = any(l.lower() in title_lower or l.lower() in loc_lower for l in target_locations)

    # If location is totally missing (e.g. link scan), we might skip strict location check
    # OR require it in title. Let's be slightly lenient for discovery but prioritize matches.
    # Prompt says "Location must include: India or Remote".
    # If we don't have location info, we might get noise.
    # Let's assume if location is empty, we only pass if title has location keywords?
    # Or just pass and let human filter.

    # Let's enforce: (Title Keyword) AND (Domain Keyword) AND (Location Keyword anywhere)
    return has_title and has_domain and has_location

def run():
    all_jobs = []
    career_sites = CONFIG.get('career_sites', [])

    for site in career_sites:
        try:
            jobs = crawl_site(site)
            logging.info(f"Found {len(jobs)} jobs on {site}")
            all_jobs.extend(jobs)
        except Exception as e:
            # Per-site failure isolation
            logging.error(f"Critical error processing site {site}: {e}")
            continue

    return all_jobs

if __name__ == "__main__":
    jobs = run()
    print(json.dumps(jobs, indent=2))
