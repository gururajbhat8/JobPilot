from app.services.db import SessionLocal 
from app.models.db_models import Job 
from app.graph.workflow import app_graph

if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("Fetching jobs from Postgres...")

        jobs = db.query(Job).limit(3).all() 

        for job in jobs:
            print(f"\n--- Starting Pipeline for Job: {job.title} ---")

            initial_state = {
                "job_id": job.id,
                "raw_text": job.raw_text,
                "parsed_jd": None
            }

            final_state = app_graph.invoke(initial_state)

            extracted_skills = final_state['parsed_jd'].required_skills

            print(f"Finished! Skills Extracted: {extracted_skills}") 

    finally:
        db.close()
