from fastapi import FastAPI
from jobspy import scrape_jobs

app = FastAPI()


# تست سلامت سرویس
@app.get("/")
def health():
    return {"status": "ok"}


# اجرای اسکریپر (نسخه سبک)
@app.post("/run")
def run():
    jobs = scrape_jobs(
        site_name=["google"],        # فقط Google (سبک و پایدار)
        search_term="SEO",
        location="United States",
        hours_old=168                # ۷ روز اخیر
    )

    # تبدیل خروجی به JSON
    return jobs.to_dict("records")
