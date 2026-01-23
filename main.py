@app.post("/run")
def run():
    global LAST_RESULT

    LAST_RESULT = {
        "last_run_at": datetime.utcnow().isoformat(),
        "count": 1,
        "data": [
            {
                "title": "TEST SEO JOB",
                "company": "Test Company",
                "site": "test",
            }
        ],
        "error": None
    }

    return {"started": True}
