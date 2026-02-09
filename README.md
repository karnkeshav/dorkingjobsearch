# Director-Level Job Radar

A fully automated, stateful job discovery system that detects real **Director / Head / Principal** roles in **Platform / Cloud / SRE / DevOps** (India/Remote) as soon as they are published and sends Telegram notifications.

This system runs entirely on **GitHub Free Tier** using GitHub Actions.

## 🚀 Features

*   **Multi-Source Discovery:**
    *   **Google X-Ray:** Uses Custom Search JSON API (with fallback logic).
    *   **Bing X-Ray:** Uses Bing Search API (with fallback logic).
    *   **Career Site Crawling:** Scrapes configurable company career pages (JSON-LD aware).
*   **Smart Filtering:**
    *   **Titles:** Director, Head, Principal
    *   **Domains:** Platform, Cloud, SRE, DevOps
    *   **Locations:** India, Remote
*   **Persistence:** Remembers seen jobs in `data/seen_jobs.json` to prevent duplicate alerts.
*   **Scheduling:** Runs every 2 hours within the **09:00–23:00 IST** window.
*   **Notifications:** Sends a consolidated digest to Telegram.

## 📂 Project Structure

```
/
├── README.md                  # Documentation
├── index.html                 # Status page
├── config/
│   └── settings.json          # Keywords, career sites, timezone
├── scripts/
│   ├── google_xray.py         # Google search logic
│   ├── bing_xray.py           # Bing search logic
│   ├── career_crawler.py      # Company site crawler
│   ├── dedupe.py              # Deduplication logic
│   ├── notifier.py            # Telegram sender
│   └── main.py                # Orchestrator
├── data/
│   └── seen_jobs.json         # Persistent state
├── logs/
│   └── latest.log             # Execution logs
├── .github/workflows/
│   └── scheduler.yml          # Automation workflow
└── requirements.txt
```

## 🛠 Setup Instructions

### 1. Fork this Repository
Click the **Fork** button at the top right of this page.

### 2. Enable Read & Write Permissions (CRITICAL)
GitHub Actions defaults to read-only. To allow the script to save state:
1.  Go to **Settings** → **Actions** → **General**.
2.  Scroll to **Workflow permissions**.
3.  Select **Read and write permissions**.
4.  Click **Save**.

### 3. Configure Telegram Bot
1.  Open Telegram and search for **@BotFather**.
2.  Send `/newbot` and follow the prompts.
3.  Copy the **HTTP API Token**. This is your `TELEGRAM_BOT_TOKEN`.
4.  Start a chat with your new bot (or add it to a group).
5.  Get your **Chat ID**:
    *   Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
    *   Look for `"chat": {"id": 123456789, ...}`. This number is your `TELEGRAM_CHAT_ID`.

### 4. Get Google Custom Search API Key (Free)
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a project and enable the **Custom Search API**.
3.  Create an **API Key**. This is `GOOGLE_API_KEY`.
4.  Go to [Programmable Search Engine](https://programmablesearchengine.google.com/).
5.  Create a search engine:
    *   **Sites to search:** `linkedin.com/jobs`
    *   **Name:** Job Radar
6.  Get the **Search Engine ID** (cx). This is `GOOGLE_CX_ID`.

*(Optional: For Bing X-Ray, get a [Bing Search API Key](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/) for `BING_API_KEY`)*

### 5. Set GitHub Secrets
Go to **Settings** → **Secrets and variables** → **Actions** → **New repository secret**. Add:

| Name | Value |
| :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | Your Telegram Bot Token |
| `TELEGRAM_CHAT_ID` | Your Telegram Chat ID |
| `GOOGLE_API_KEY` | Your Google API Key |
| `GOOGLE_CX_ID` | Your Google Search Engine ID |
| `BING_API_KEY` | (Optional) Your Bing API Key |

### 6. Enable Automation
Go to the **Actions** tab in GitHub and ensure workflows are enabled. You can manually trigger the "Director-Level Job Radar" workflow to test it immediately.

## ⚙️ Configuration
Edit `config/settings.json` to customize:
*   **Keywords:** Titles, Domains, Locations.
*   **Schedule Window:** Start/End hours.
*   **Career Sites:** List of URLs to crawl.

## ⚠️ Notes
*   **Timezone:** The script runs on IST (Asia/Kolkata).
*   **Failures:** If one source fails (e.g., Google API quota exceeded), others will continue running.
*   **Free Tier Limits:** Google Custom Search API allows 100 queries/day for free. Adjust scheduling if needed.
