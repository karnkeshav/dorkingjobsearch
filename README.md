# Director-Level Job Radar

A fully automated, stateful job discovery system that detects real **Director / Head / Principal** roles in **Platform / Cloud / SRE / DevOps** (India/Remote) as soon as they are published and sends Telegram notifications.

This system runs entirely on **GitHub Free Tier** using GitHub Actions, **requiring zero billing** (no Google/Bing API keys).

## 🚀 Features

*   **Primary Discovery (Career Sites):** Direct crawling of company career pages using JSON-LD parsing and link scanning.
*   **Secondary Discovery (Google Alerts):** Ingests jobs via Google Alerts RSS feeds (user-configured).
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
│   └── settings.json          # Keywords, career sites, alerts, timezone
├── scripts/
│   ├── career_crawler.py      # Main discovery engine (JSON-LD aware)
│   ├── google_alerts_ingest.py# Google Alerts RSS parser
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

*(Note: `google_xray.py` and `bing_xray.py` are deprecated.)*

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

### 4. Set GitHub Secrets
Go to **Settings** → **Secrets and variables** → **Actions** → **New repository secret**. Add:

| Name | Value |
| :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | Your Telegram Bot Token |
| `TELEGRAM_CHAT_ID` | Your Telegram Chat ID |

### 5. Configure Job Sources (`config/settings.json`)

#### A. Add Career Sites
Add the URLs of career pages you want to monitor to the `career_sites` array.
```json
"career_sites": [
  "https://careers.google.com",
  "https://jobs.netflix.com",
  "https://www.your-target-company.com/careers"
]
```

#### B. Setup Google Alerts (Optional)
1.  Go to [Google Alerts](https://www.google.com/alerts).
2.  Create an alert for your query (e.g., `site:linkedin.com/jobs "Director" "Platform" India`).
3.  Click **Show options**.
4.  Under **Deliver to**, select **RSS Feed**.
5.  Click **Create Alert**.
6.  Right-click the RSS icon next to your new alert and **Copy Link Address**.
7.  Add this URL to `config/settings.json`:
```json
"google_alerts": {
  "enabled": true,
  "feed_urls": [
    "https://www.google.com/alerts/feeds/..."
  ]
}
```

### 6. Enable Automation
Go to the **Actions** tab in GitHub and ensure workflows are enabled. You can manually trigger the "Director-Level Job Radar" workflow to test it immediately.

## ⚠️ Notes
*   **Timezone:** The script runs on IST (Asia/Kolkata).
*   **Limitations:** Some career sites heavily reliant on JavaScript (SPA) might not be fully scraped. The crawler attempts to parse JSON-LD metadata which works on many modern sites, but headless browsing is disabled to run on free tier.
*   **Zero Billing:** This system uses no paid APIs. It relies on standard web requests and public RSS feeds.
