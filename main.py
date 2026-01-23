from fastapi import FastAPI
from jobspy import scrape_jobs
from datetime import datetime

app = FastAPI()

LAST_RESULT = {
    "last_run_at": None,
    "count": 0,
    "data": [],
    "error": None
}

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/run")
def run():
    global LAST_RESULT

    try:
        jobs = scrape_jobs(
            site_name=["google"],      # فقط Google
            search_term="SEO",
            location="United States",
            hours_old=168              # ۷ روز اخیر
        )

        # فیلتر SEO در title
        jobs = jobs[jobs["title"].str.contains("SEO", case=False, na=False)]

        records = jobs.to_dict("records")

        LAST_RESULT = {
            "last_run_at": datetime.utcnow().isoformat(),
            "count": len(records),
            "data": records,
            "error": None
        }

        return {"started": True}

    except Exception as e:
        LAST_RESULT = {
            "last_run_at": datetime.utcnow().isoformat(),
            "count": 0,
            "data": [],
            "error": str(e)
        }
        return {"started": False, "error": str(e)}

@app.get("/results")
def results():
    return LAST_RESULT
