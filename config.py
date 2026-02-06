# config.py

"""
Configuration module for Job Intelligence Engine.
Stores keywords, dork patterns, and other constants.
"""

# Keywords to extract from resume or fallback to
TARGET_KEYWORDS = [
    "Strategic Roadmap",
    "P&L Management",
    "AI Governance",
    "Cloud FinOps",
    "Operational Resilience",
    "$30M+ Savings",
    "Agentic AI",
    "AI"
]

# Google Dork Templates
# {keyword_1} and {keyword_2} placeholders are replaced dynamically from resume keywords
DORK_TEMPLATES = {
    "ats_discovery": 'site:greenhouse.io (Director OR "Senior Director") OR "{keyword_1}" OR "{keyword_2}"',
    "ats_discovery_lever": 'site:lever.co (Director OR "Senior Director") OR "{keyword_1}" OR "{keyword_2}"',
    "ats_discovery_ashby": 'site:ashbyhq.com (Director OR "Senior Director") OR "{keyword_1}" OR "{keyword_2}"',
    "ats_discovery_workday": 'site:myworkdayjobs.com (Director OR "Senior Director") OR "{keyword_1}" OR "{keyword_2}"',

    "hidden_documents": 'site:docs.google.com "we are hiring" OR "Director of Engineering"',

    "internal_career_pages": 'intitle:"career" inurl:"/jobs" -site:linkedin.com -site:indeed.com "Director" "Cloud Strategy"',

    # "Director-Level" Dorks to Hardcode
    "unlisted_executive_roles": 'site:lever.co OR site:greenhouse.io OR site:ashbyhq.com ("Director" OR "Head of") OR ("AI Governance" OR "FinOps") OR "Remote"',
    "strategic_plans": 'filetype:pdf "strategic plan" 2026 "hiring" ("AI" OR "Cloud")',
    "public_hiring_lists": 'site:airtable.com "hiring" "Director" "Engineering"'
}

# LinkedIn Boolean Search Generators
# These are templates for generating boolean strings for LinkedIn or signals
LINKEDIN_PATTERNS = {
    "hiring_manager": '("Hiring" OR "Building my team") OR ("VP of Engineering" OR "CIO") OR "{keyword}"'
}

# Search Configuration
# To avoid being blocked by Google in GitHub Actions, increase sleep intervals
SEARCH_CONFIG = {
    "num_results": 10,
    "sleep_interval_min": 20, # Increased to avoid rate limiting
    "sleep_interval_max": 40, # Increased to avoid rate limiting
    "lang": "en"
}
