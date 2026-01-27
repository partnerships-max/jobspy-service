from fastapi import FastAPI
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
        from jobspy import scrape_jobs   # 👈 اینجا اضافه شد

        jobs = scrape_jobs(
            site_name=["google", "indeed", "linkedin"],
            search_term="SEO",
            location="United States",
            hours_old=168,
            fetch_full_description=True
        )

        if "job_title" in jobs.columns:
            jobs = jobs[jobs["job_title"].str.contains("SEO", case=False, na=False)]

        records = []
        for _, row in jobs.iterrows():
            records.append({
                "title": row.get("job_title"),
                "company": row.get("company"),
                "company_url": row.get("company_url"),
                "company_industry": row.get("company_industry"),
                "location": row.get("location"),
                "site": row.get("site"),
                "job_url": row.get("job_url"),
                "date_posted": row.get("date_posted"),
                "is_remote": row.get("is_remote"),
                "description": row.get("description")
            })

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
    try:
        return LAST_RESULT
    except Exception as e:
        return {"error": str(e)}

