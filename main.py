from fastapi import FastAPI
from jobspy import scrape_jobs

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/run")
def run():
    jobs = scrape_jobs(
        site_name=["google", "linkedin", "indeed"],
        search_term="SEO",
        location="United States",
        hours_old=168,
        fetch_full_description=True
    )

    return jobs.to_dict("records")
