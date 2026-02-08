import config
import logging
import time
import random
from googlesearch import search

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JobSearcher:
    def __init__(self, keywords):
        self.keywords = keywords
        self.dorks = []
        self.results = []

    def generate_dorks(self):
        """
        Generates dork queries by injecting keywords into templates.
        """
        # We need at least 2 keywords for some templates, if not enough, use defaults
        k1 = self.keywords[0] if len(self.keywords) > 0 else "FinOps"
        k2 = self.keywords[1] if len(self.keywords) > 1 else "AI"

        logging.info(f"Generating dorks using keywords: {k1}, {k2}")

        # Dynamic ATS Dorks
        self.dorks.append(config.DORK_TEMPLATES["ats_discovery"].format(keyword_1=k1, keyword_2=k2))
        self.dorks.append(config.DORK_TEMPLATES["ats_discovery_lever"].format(keyword_1=k1, keyword_2=k2))
        self.dorks.append(config.DORK_TEMPLATES["ats_discovery_ashby"].format(keyword_1=k1, keyword_2=k2))
        self.dorks.append(config.DORK_TEMPLATES["ats_discovery_workday"].format(keyword_1=k1, keyword_2=k2))

        # Static/Hardcoded Dorks from Config
        self.dorks.append(config.DORK_TEMPLATES["hidden_documents"])
        self.dorks.append(config.DORK_TEMPLATES["internal_career_pages"])
        self.dorks.append(config.DORK_TEMPLATES["unlisted_executive_roles"])
        self.dorks.append(config.DORK_TEMPLATES["strategic_plans"])
        self.dorks.append(config.DORK_TEMPLATES["public_hiring_lists"])

        return self.dorks

    def perform_search(self, max_dorks_to_run=None):
        """
        Executes Google searches for generated dorks.
        Args:
            max_dorks_to_run (int): Optional limit on how many dorks to process (for testing).
        """
        all_results = []
        dorks_to_process = self.dorks[:max_dorks_to_run] if max_dorks_to_run else self.dorks

        for dork in dorks_to_process:
            logging.info(f"Searching for: {dork}")
            try:
                # search() returns a generator
                # advanced=True is not available in all versions/libraries, usually standard search returns URLs
                results_generator = search(dork, num_results=config.SEARCH_CONFIG["num_results"], lang=config.SEARCH_CONFIG["lang"])

                count = 0
                for url in results_generator:
                    logging.info(f"Found URL: {url}")
                    all_results.append({
                        "query": dork,
                        "url": url,
                        "source": "Google Dork"
                    })
                    count += 1

                if count == 0:
                    logging.info("No results found for this dork.")

                # Sleep to avoid rate limiting
                sleep_time = random.uniform(config.SEARCH_CONFIG["sleep_interval_min"], config.SEARCH_CONFIG["sleep_interval_max"])
                logging.info(f"Sleeping for {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)

            except Exception as e:
                logging.error(f"Error searching for '{dork}': {e}")
                # Backoff on error
                time.sleep(30)

        self.results = all_results
        return all_results

if __name__ == "__main__":
    # Test execution
    test_keywords = ["FinOps", "AI"]
    searcher = JobSearcher(test_keywords)
    dorks = searcher.generate_dorks()

    print("-" * 20)
    print("Generated Dorks:")
    for d in dorks:
        print(f"- {d}")
    print("-" * 20)

    # Run a limited search to verify functionality without triggering bans
    print("Running limited search test (1 dork)...")
    results = searcher.perform_search(max_dorks_to_run=1)
    print(f"Total results found: {len(results)}")
