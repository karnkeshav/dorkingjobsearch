import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JobVerifier:
    def __init__(self):
        self.session = requests.Session()
        # Spoof User-Agent to avoid immediate blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def verify_link(self, url):
        """
        Checks if a URL is active (returns 200-299 status code).
        """
        try:
            # HEAD request is faster but some servers block it
            response = self.session.head(url, allow_redirects=True, timeout=10)

            if 200 <= response.status_code < 300:
                return True

            # If HEAD fails (e.g., 405 Method Not Allowed), try GET
            if response.status_code == 405 or response.status_code == 403:
                logging.debug(f"HEAD failed for {url} with {response.status_code}, trying GET...")
                response = self.session.get(url, timeout=10)
                return 200 <= response.status_code < 300

            logging.warning(f"URL {url} returned status: {response.status_code}")
            return False

        except requests.RequestException as e:
            logging.warning(f"Failed to verify {url}: {e}")
            return False

    def enrich_company_data(self, company_name):
        """
        Placeholder for company enrichment (funding, layoffs).
        Returns a dictionary with enrichment data.
        """
        # In a real scenario, call Clearbit, Crunchbase, or similar API here.
        logging.info(f"Enriching data for placeholder company: {company_name}")
        return {
            "recent_layoffs": "Check 'Layoffs.fyi'",
            "funding_stage": "Check 'Crunchbase'",
            "ghost_job_risk": "Medium" # Placeholder logic
        }

if __name__ == "__main__":
    verifier = JobVerifier()
    test_url_good = "https://www.google.com"
    test_url_bad = "https://www.google.com/this_page_does_not_exist_404"

    print(f"Verifying {test_url_good}: {verifier.verify_link(test_url_good)}")
    print(f"Verifying {test_url_bad}: {verifier.verify_link(test_url_bad)}")
