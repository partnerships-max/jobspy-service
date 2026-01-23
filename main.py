from fastapi import FastAPI, BackgroundTasks
from jobspy import scrape_jobs
import json

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

def run_scraper():
    jobs = scrape_jobs(
        site_name=["google"],
        search_term="SEO",
        location="United States",
        hours_old=168,
        fetch_full_description=True
    )

    jobs = jobs[jobs["title"].str.contains("SEO", case=False, na=False)]

    with open("jobs.json", "w") as f:
        f.write(jobs.to_json(orient="records"))

@app.post("/run")
def run(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_scraper)
    return {"started": True}
