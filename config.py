# config.py

"""
Configuration module for Job Intelligence Engine.
Stores keywords, dork patterns, and other constants.
"""

# Keywords to extract from resume or fallback to
TARGET_KEYWORDS = [
 "Software"
]

# Google Dork Templates
# Space between terms acts as a logical AND. 
# Use parentheses for OR logic to ensure it doesn't break the 'site:' filter.
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
# Removed the OR between the persona (VP/CIO) and the intent (Hiring)
LINKEDIN_PATTERNS = {
    "hiring_manager": '("Hiring" OR "Building my team") ("VP of Engineering" OR "CIO") "{keyword}"'
}

# Search Configuration
SEARCH_CONFIG = {
    "num_results": 10,
    "sleep_interval_min": 30, # Slightly increased for GitHub Action safety
    "sleep_interval_max": 60, 
    "lang": "en"
}
