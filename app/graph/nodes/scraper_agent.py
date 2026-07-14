import uuid
from app.services.apify_client import scrape_jobs
from app.models.db_models import Job
from app.services.db import SessionLocal

def run_scraper_and_save(keywords: str, location: str, max_items: int = 2):
    """
    Scrapes jobs from Apify and saves the raw data to Postgres.
    """
    # 1. Call the Apify service we built
    raw_datasets = scrape_jobs(keywords, location, max_items)

    saved_jobs = []

    # 2. Open a temporary database session
    db = SessionLocal()
    try:
        for item in raw_datasets:

            new_job = Job(
                id = str(uuid.uuid4()),
                source = "linkedin_apify",
                title=item.get("title", "Unknown Title"),
                company=item.get("companyName", "Unknown Company"),
                # This is the massive wall of text the LLM will parse later!
                raw_text=item.get("descriptionText", "")
            )

            db.add(new_job) 
            saved_jobs.append(new_job) 

        db.commit()
        print(f"Successfully saved {len(saved_jobs)} raw jobs to the database!")
        
        return saved_jobs

    except Exception as e: 
        db.rollback() 
        print(f"Database error: {e}")
        return []

    finally:
        db.close() 
        