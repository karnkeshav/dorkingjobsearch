# config.py

"""
Configuration module for Job Intelligence Engine.
Stores keywords, dork patterns, and other constants.
"""

# Keywords to extract from resume or fallback to
TARGET_KEYWORDS = [
    "Operational Resilience",
    "Agentic AI",
    "FinOps",
    "Cloud Transformation",
    "ITSM"
]

# Google Dork Templates
# {keywords} placeholders can be replaced dynamically
DORK_TEMPLATES = {
    # Updated ATS Discovery Templates with proper grouping logic
    "ats_discovery": 'site:greenhouse.io (Director OR "Senior Director") ("{keyword_1}" OR "{keyword_2}")',
    "ats_discovery_lever": 'site:lever.co (Director OR "Senior Director") ("{keyword_1}" OR "{keyword_2}")',
    "ats_discovery_ashby": 'site:ashbyhq.com (Director OR "Senior Director") ("{keyword_1}" OR "{keyword_2}")',
    "ats_discovery_workday": 'site:myworkdayjobs.com (Director OR "Senior Director") ("{keyword_1}" OR "{keyword_2}")',

    "hidden_documents": 'site:docs.google.com "we are hiring" AND "Director of Engineering"',

    "internal_career_pages": 'intitle:"career" inurl:"/jobs" -site:linkedin.com -site:indeed.com "Director" "Cloud Strategy"',

    # "Director-Level" Dorks to Hardcode
    "unlisted_executive_roles": 'site:lever.co OR site:greenhouse.io OR site:ashbyhq.com ("Director" OR "Head of") AND ("AI Governance" OR "FinOps") AND "Remote"',
    "strategic_plans": 'filetype:pdf "strategic plan" 2026 "hiring" ("AI" OR "Cloud")',
    "public_hiring_lists": 'site:airtable.com "hiring" "Director" "Engineering"'
}

# LinkedIn Boolean Search Generators
# These are templates for generating boolean strings for LinkedIn or signals
LINKEDIN_PATTERNS = {
    "hiring_manager": '("Hiring" OR "Building my team") AND ("VP of Engineering" OR "CIO") AND "{keyword}"'
}

# Search Configuration
SEARCH_CONFIG = {
    "num_results": 10,
    "sleep_interval_min": 30,
    "sleep_interval_max": 60,
    "lang": "en"
}
