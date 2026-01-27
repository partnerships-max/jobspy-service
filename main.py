from jobspy import scrape_jobs
import json

jobs = scrape_jobs(
    site_name=["google", "indeed", "linkedin"],
    search_term="SEO",
    location="United States",
    hours_old=168,
    fetch_full_description=True
)

print("COLUMNS:", list(jobs.columns))  # 👈 این خط اضافه شد

# انتخاب امن ستون عنوان
title_col = "job_title" if "job_title" in jobs.columns else "title"

jobs = jobs[jobs[title_col].str.contains("SEO", case=False, na=False)]

jobs.to_json("results.json", orient="records")
print("DONE")
