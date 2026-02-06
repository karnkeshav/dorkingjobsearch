# DorkingJobSearch: The Job Intelligence Engine

An automated tool for discovering "hidden" executive job listings that are not easily found on standard job boards. This project is designed for Senior IT Executives (Director/Senior Director level) to find unlisted roles and detect hiring intent.

## Features

*   **Resume Parsing:** Extracts high-value keywords from your PDF resume using `pdfminer.six`.
*   **Smart Dorking:** Generates dynamic Google Dork queries to find ATS listings (Greenhouse, Lever, Ashby), hidden Google Docs, and internal career pages.
*   **Hiring Signals:** Generates Boolean search strings to find hiring managers on LinkedIn.
*   **Verification:** Validates found URLs and provides placeholders for company enrichment (layoffs, funding).
*   **Rate Limiting:** Uses random sleep intervals to mimic human behavior.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/dorkingjobsearch.git
    cd dorkingjobsearch
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Prepare your Resume:**
    *   Place your `resume.pdf` in the root directory.

## Usage

Run the main script:

```bash
python main.py
```

### Output

*   `jobs.csv`: Contains found job listings with Company, Source URL, and enrichment data.
*   `hiring_signals.txt`: Contains Boolean search strings for LinkedIn/PhantomBuster.

## Configuration

Edit `config.py` to customize:
*   `TARGET_KEYWORDS`: Default keywords if resume parsing misses them.
*   `DORK_TEMPLATES`: Add or modify search patterns.
*   `SEARCH_CONFIG`: Adjust search depth and sleep intervals.

## The "Hybrid Intelligence" Workflow (PhantomBuster)

Since aggressive LinkedIn scraping can lead to bans, use this hybrid approach:

1.  **Find Companies:** Use this Python tool (`main.py`) to generate a list of target companies via Google Dorking.
2.  **Find People:** Use **PhantomBuster** for the "social web".
    *   **Step 1:** Copy the generated Boolean strings from `hiring_signals.txt`.
    *   **Step 2:** Feed the identified companies into PhantomBuster's "LinkedIn Company Employees Export".
    *   **Step 3:** Filter for titles like "CTO", "CIO", "VP of Engineering".
    *   **Step 4:** This gives you authentic hiring manager data.

## Modules

*   `main.py`: Orchestrator.
*   `parser.py`: Resume keyword extraction.
*   `searcher.py`: Google Dork generation and execution.
*   `signals.py`: Signal detection logic.
*   `verifier.py`: Link validation and enrichment.
*   `config.py`: Configuration settings.

## Disclaimer

This tool is for educational and personal use. Respect website Terms of Service.
