from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["indeed", "google", "linkedin"],
    search_term="SEO",
    location="United States",
    hours_old=168,
    fetch_full_description=True
)

print("TOTAL JOBS:", len(jobs))
print(jobs["title"].head(20))
