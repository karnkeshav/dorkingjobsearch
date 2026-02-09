import json
import logging
import os
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SEEN_JOBS_FILE = 'data/seen_jobs.json'

def load_seen_jobs():
    if os.path.exists(SEEN_JOBS_FILE):
        with open(SEEN_JOBS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_seen_jobs(jobs):
    with open(SEEN_JOBS_FILE, 'w') as f:
        json.dump(jobs, f, indent=2)

def generate_job_hash(job):
    # Hash based on Title + Link (Company if available)
    # Simple deduplication key
    raw_string = f"{job.get('title')}-{job.get('link')}"
    return hashlib.md5(raw_string.encode('utf-8')).hexdigest()

def deduplicate(new_jobs):
    seen_jobs = load_seen_jobs()
    seen_hashes = {generate_job_hash(j) for j in seen_jobs}

    unique_new_jobs = []

    for job in new_jobs:
        job_hash = generate_job_hash(job)
        if job_hash not in seen_hashes:
            unique_new_jobs.append(job)
            seen_hashes.add(job_hash)
            seen_jobs.append(job) # Append to persistent list

    logging.info(f"Deduplication: {len(new_jobs)} input -> {len(unique_new_jobs)} unique new.")

    if unique_new_jobs:
        save_seen_jobs(seen_jobs)

    return unique_new_jobs

if __name__ == "__main__":
    # Test execution
    test_jobs = [
        {"title": "Director of Engineering", "link": "http://example.com/job1"},
        {"title": "Head of Platform", "link": "http://example.com/job2"},
        {"title": "Director of Engineering", "link": "http://example.com/job1"} # Duplicate
    ]
    unique = deduplicate(test_jobs)
    print("Unique Jobs:", json.dumps(unique, indent=2))
