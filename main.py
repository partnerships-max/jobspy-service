@app.post("/run")
def run():
    global LAST_RESULT

    try:
        jobs = scrape_jobs(
            site_name=["google"],
            search_term="SEO",
            location="United States",
            hours_old=168
        )

        LAST_RESULT = {
            "last_run_at": datetime.utcnow().isoformat(),
            "count": 0,
            "data": [],
            "error": f"columns: {list(jobs.columns)}"
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
