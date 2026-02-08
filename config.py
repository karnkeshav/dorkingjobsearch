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
    "Agentic AI",
    "FinOps",
    "SRE"
]

# Google Dork Templates
# Space between terms acts as a logical AND. 
# Parentheses group OR logic to prevent breaking the 'site:' filter.
DORK_TEMPLATES = {
    "ats_discovery": 'site:greenhouse.io (Director OR "Senior Director") ("{keyword_1}" OR "{keyword_2}")',
    "ats_discovery_lever": 'site:lever.co (Director OR "Senior Director") ("{keyword_1}" OR "{keyword_2}")',
    "ats_discovery_ashby": 'site:ashbyhq.com (Director OR "Senior Director") ("{keyword_1}" OR "{keyword_2}")',
    "ats_discovery_workday": 'site:myworkdayjobs.com (Director OR "Senior Director") ("{keyword_1}" OR "{keyword_2}")',

    "hidden_documents": 'site:docs.google.com "we are hiring" (Director OR "Head of") "{keyword_1}"',

    "internal_career_pages": 'intitle:"career" inurl:"/jobs" -site:linkedin.com -site:indeed.com "Director" ("{keyword_1}" OR "{keyword_2}")',

    # "Director-Level" Dorks to Hardcode
    "unlisted_executive_roles": '(site:lever.co OR site:greenhouse.io OR site:ashbyhq.com) ("Director" OR "Head of") ("AI Governance" OR "FinOps") "Remote"',
    "strategic_plans": 'filetype:pdf "strategic plan" 2026 "hiring" ("AI" OR "Cloud")',
    "public_hiring_lists": 'site:airtable.com "hiring" "Director" "Engineering"'
}

# LinkedIn Boolean Search Generators
LINKEDIN_PATTERNS = {
    "hiring_manager": '("Hiring" OR "Building my team") ("VP of Engineering" OR "CIO") "{keyword}"'
}

# Search Configuration
# Increased sleep intervals to reduce the risk of GitHub IP blocking
SEARCH_CONFIG = {
    "num_results": 10,
    "sleep_interval_min": 30, 
    "sleep_interval_max": 60, 
    "lang": "en"
}
