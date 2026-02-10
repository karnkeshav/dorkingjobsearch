import json
import logging
import os
import requests
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run():
    logging.warning("This module is deprecated. Use career_crawler.py instead.")
    return []

if __name__ == "__main__":
    jobs = run()
    print(json.dumps(jobs, indent=2))
