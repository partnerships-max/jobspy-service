import json
import numpy as np
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["google", "indeed", "linkedin"],
    search_term="SEO",
    google_search_term="SEO jobs United States",
    location="United States",
    results_wanted=50,
    hours_old=24,
    country_indeed="USA",
    description_format="markdown",
    linkedin_fetch_description=False,
)

print("ROWS:", len(jobs))

if jobs is None or len(jobs) == 0:
    print("No results")
    exit(0)

jobs = jobs[
    jobs["title"].str.contains("SEO", case=False, na=False)
    | jobs["description"].str.contains("SEO", case=False, na=False)
]

if "job_url" in jobs.columns:
    jobs = jobs.drop_duplicates(subset=["job_url"])
else:
    jobs = jobs.drop_duplicates()

# Replace NaN with None (valid JSON null)
jobs = jobs.replace({np.nan: None})

records = jobs.to_dict(orient="records")

with open("results.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2, default=str, allow_nan=False)

print("DONE")
