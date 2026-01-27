from jobspy import scrape_jobs
import json

jobs = scrape_jobs(
    site_name=["google", "indeed", "linkedin"],
    search_term="SEO",
    location="United States",
    hours_old=168,
    fetch_full_description=True
)

jobs = jobs[jobs["job_title"].str.contains("SEO", case=False, na=False)]

jobs.to_json("results.json", orient="records")

print("DONE")
