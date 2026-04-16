import json
import numpy as np
import pandas as pd
from jobspy import scrape_jobs

sites = ["google", "indeed", "linkedin"]
all_jobs = []

for site in sites:
    try:
        print(f"Scraping {site}...")
        jobs = scrape_jobs(
            site_name=[site],
            search_term="SEO",
            google_search_term="SEO jobs United States",
            location="United States",
            results_wanted=50,
            hours_old=24,
            country_indeed="USA",
            description_format="markdown",
            linkedin_fetch_description=True,
        )
        if jobs is not None and len(jobs) > 0:
            all_jobs.append(jobs)
            print(f"  {site}: {len(jobs)} jobs")
    except Exception as e:
        print(f"  {site} failed: {e}")
        continue

if not all_jobs:
    print("No results from any site")
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump([], f)
    exit(0)

jobs = pd.concat(all_jobs, ignore_index=True)
print("TOTAL ROWS:", len(jobs))

# Keep only rows where title contains "SEO"
jobs = jobs[jobs["title"].str.contains(r"\bSEO\b", case=False, na=False)]

if "job_url" in jobs.columns:
    jobs = jobs.drop_duplicates(subset=["job_url"])
else:
    jobs = jobs.drop_duplicates()

jobs = jobs.replace({np.nan: None})
records = jobs.to_dict(orient="records")

with open("results.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2, default=str, allow_nan=False)

print("DONE")
