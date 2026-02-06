import pandas as pd
from parser import ResumeParser
from searcher import JobSearcher
from verifier import JobVerifier
from signals import SignalDetector
import logging
import os
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_company_from_url(url):
    """
    Attempts to extract company name from URL.
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        # simplistic extraction
        if "greenhouse.io" in domain:
            # https://boards.greenhouse.io/companyname/...
            parts = parsed.path.split('/')
            if len(parts) > 1:
                return parts[1]
        elif "lever.co" in domain:
             # https://jobs.lever.co/companyname/...
            parts = parsed.path.split('/')
            if len(parts) > 1:
                return parts[1]

        # Fallback to domain name
        return domain.replace("www.", "").split('.')[0]
    except:
        return "Unknown"

def main():
    resume_path = "resume.docx"
    if not os.path.exists(resume_path):
        logging.error("resume.pdf not found. Please place your resume in the project root.")
        return

    # 1. Parse Resume
    logging.info("Step 1: Parsing Resume...")
    parser = ResumeParser(resume_path)
    keywords = parser.parse()
    if not keywords:
        logging.warning("No keywords found in resume. Using default keywords.")
        keywords = ["FinOps", "AI Governance"]

    # 2. Search
    logging.info("Step 2: Searching for Jobs (Dorking)...")
    searcher = JobSearcher(keywords)
    searcher.generate_dorks()

    # We limit dorks to run to avoid long waits in testing/sandbox
    # In production, remove max_dorks_to_run or increase it
    raw_results = searcher.perform_search(max_dorks_to_run=3)

    # 3. Verify & Enrich
    logging.info(f"Step 3: Verifying & Enriching {len(raw_results)} Results...")
    verifier = JobVerifier()
    verified_results = []

    for res in raw_results:
        if verifier.verify_link(res['url']):
            company_name = extract_company_from_url(res['url'])

            enrichment = verifier.enrich_company_data(company_name)

            # Map to requested columns
            row = {
                "Role": "See Source", # We don't scrape the title in this version
                "Company": company_name,
                "Source URL": res['url'],
                "Hiring Manager": "Check PhantomBuster",
                "Match Score": "High", # Placeholder logic
                "Layoff Status": enrichment["recent_layoffs"],
                "Funding Stage": enrichment["funding_stage"]
            }
            verified_results.append(row)
        else:
            logging.info(f"Skipping dead link: {res['url']}")

    # 4. Signal Detection
    logging.info("Step 4: Generating Hiring Signals...")
    detector = SignalDetector(keywords)
    signals = detector.detect_signals()

    # 5. Output
    logging.info("Step 5: Saving Results...")

    # Save Jobs
    if verified_results:
        df = pd.DataFrame(verified_results)
        df.to_csv("jobs.csv", index=False)
        logging.info(f"Saved {len(verified_results)} jobs to jobs.csv")
    else:
        logging.info("No valid jobs found to save. Creating empty template.")
        # Create an empty CSV for structure
        columns = ["Role", "Company", "Source URL", "Hiring Manager", "Match Score", "Layoff Status", "Funding Stage"]
        pd.DataFrame(columns=columns).to_csv("jobs.csv", index=False)

    # Save signals
    with open("hiring_signals.txt", "w") as f:
        f.write("Use these Boolean strings on LinkedIn or PhantomBuster to find Hiring Managers:\n\n")
        for s in signals:
            f.write(s + "\n")
    logging.info("Hiring signals saved to hiring_signals.txt")

    logging.info("Execution Complete.")

if __name__ == "__main__":
    main()
