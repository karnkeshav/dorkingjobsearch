import json
import logging
import requests
from bs4 import BeautifulSoup
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    with open('config/settings.json', 'r') as f:
        return json.load(f)

CONFIG = load_config()

def crawl_site(url):
    try:
        logging.info(f"Crawling {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        jobs = []

        # 1. Look for JSON-LD JobPosting
        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'JobPosting':
                    jobs.append(parse_json_ld(data))
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get('@type') == 'JobPosting':
                            jobs.append(parse_json_ld(item))
            except json.JSONDecodeError:
                continue

        # 2. Fallback: Simple keyword search in links
        if not jobs:
            logging.info("No JSON-LD found, falling back to link scanning.")
            for link in soup.find_all('a', href=True):
                title = link.get_text(strip=True)
                href = link['href']
                if is_target_job(title):
                    jobs.append({
                        "title": title,
                        "link": href if href.startswith('http') else url.rstrip('/') + '/' + href.lstrip('/'),
                        "source": f"Career Site: {url}"
                    })

        return jobs

    except requests.exceptions.RequestException as e:
        logging.error(f"Error crawling {url}: {e}")
        return []

def parse_json_ld(data):
    return {
        "title": data.get('title'),
        "company": data.get('hiringOrganization', {}).get('name', 'Unknown'),
        "location": data.get('jobLocation', {}).get('address', {}).get('addressLocality', 'Unknown'),
        "link": data.get('url', ''),
        "source": "JSON-LD"
    }

def is_target_job(title):
    if not title:
        return False

    title_lower = title.lower()

    has_title = any(t.lower() in title_lower for t in CONFIG['keywords']['titles'])
    has_domain = any(d.lower() in title_lower for d in CONFIG['keywords']['domains'])

    # Require at least one Title keyword AND (one Domain keyword OR Location keyword if available in title)
    # The prompt says: "Job title must include at least one: Director... Platform..."
    return has_title and has_domain

def run():
    all_jobs = []
    career_sites = CONFIG.get('career_sites', [])

    for site in career_sites:
        jobs = crawl_site(site)
        logging.info(f"Found {len(jobs)} jobs on {site}")
        all_jobs.extend(jobs)

    return all_jobs

if __name__ == "__main__":
    jobs = run()
    print(json.dumps(jobs, indent=2))
