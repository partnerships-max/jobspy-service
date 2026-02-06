import json
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["google", "indeed", "linkedin"],
    search_term="SEO",
    google_search_term="SEO jobs United States",  # Google uses only this for filtering
    location="United States",
    results_wanted=50,
    hours_old=24,
    country_indeed="USA",
    description_format="markdown",
    linkedin_fetch_description=False,  # correct param
    # proxies=["user:pass@host:port", "user:pass@host:port"],  # optional
)

print("ROWS:", len(jobs))

if jobs is None or len(jobs) == 0:
    print("No results")
    exit(0)

# Filter title + description for SEO
jobs = jobs[
    jobs["title"].str.contains("SEO", case=False, na=False)
    | jobs["description"].str.contains("SEO", case=False, na=False)
]

# Deduplicate by URL
if "job_url" in jobs.columns:
    jobs = jobs.drop_duplicates(subset=["job_url"])
else:
    jobs = jobs.drop_duplicates()

records = jobs.to_dict(orient="records")

with open("results.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2, default=str)

print("DONE")
