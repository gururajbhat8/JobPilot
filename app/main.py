from fastapi import FastAPI, HTTPException, UploadFile, File
from dotenv import load_dotenv
import os 
import pdfplumber
from app.services.db import init_db, SessionLocal
from app.models.db_models import Job
from app.services.vector_db import search_similar_jobs
from app.graph.nodes.resume_matcher_agent import calculate_match_score
from app.models.schemas import ParsedJD
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="JobPilot API", description="AI Job Search Copilot")

init_db()

@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "Hello from JobPilot! FastAPI is running.",
        "groq_key_loaded": bool(os.getenv("GROQ_API_KEY")),
        "apify_key_loaded": bool(os.getenv("APIFY_API_TOKEN"))
    }

@app.post("/match")
def find_best_jobs(file: UploadFile = File(...)):
    print(f"\n0. Reading uploaded PDF: {file.filename}")
    
    # 1. Extract text from the PDF
    resume_text = ""
    try:
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    resume_text += text + "\n"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read PDF: {e}")
        
    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from the PDF.")

    print("\n1. Searching Vector DB for Top 3 matches...")
    results = search_similar_jobs(resume_text, n_results=3)
    
    if not results['ids'] or not results['ids'][0]:
        raise HTTPException(status_code=404, detail="No jobs found in Vector DB!")
        
    final_results = []
    
    # 2. Open DB session to get original Job details (like the URL!)
    db = SessionLocal()
    try:
        # Loop through the 3 best jobs ChromaDB found
        for i in range(len(results['ids'][0])):
            job_id = results['ids'][0][i]
            job_json_string = results['documents'][0][i]
            
            parsed_jd = ParsedJD.model_validate_json(job_json_string)
            
            # Query Postgres to get the URL, Title, and Company!
            original_job = db.query(Job).filter(Job.id == job_id).first()
            
            print(f"2. Running LLM Matcher for Job: {job_id}")
            match_result = calculate_match_score(parsed_jd, resume_text)
            
            final_results.append({
                "job_id": job_id,
                "title": original_job.title if original_job else "Unknown",
                "company": original_job.company if original_job else "Unknown",
                "url": original_job.url if original_job else "", # HERE IS THE URL!
                "match_analysis": match_result.model_dump()
            })
    finally:
        db.close()
        
    return {"status": "success", "matches": final_results}
