from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os 
from app.services.db import init_db
from app.services.vector_db import search_similar_jobs
from app.graph.nodes.resume_matcher_agent import calculate_match_score
from app.models.schemas import ParsedJD
from pydantic import BaseModel
from app.graph.nodes.resume_matcher_agent import calculate_match_score



load_dotenv()

app = FastAPI(title="JobPilot API", description="AI Job Job Search Copilot")

init_db()

@app.get("/")
def read_root():
    return {"status": "success",
    "message": "Hello from JobPilot! FastAPI is running.",
    "groq_key_loaded": bool(os.getenv("GROQ_API_KEY")),
    "apify_key_loaded": bool(os.getenv("APIFY_API_TOKEN"))
    }

class ResumeRequest(BaseModel):
    resume_text: str 


@app.post("/match")
def find_best_jobs(request: ResumeRequest):
    print("\n1. Searching Vector DB for Top 3 matches...")
    # ChromaDB returns a dictionary with 'ids' and 'documents'
    results = search_similar_jobs(request.resume_text, n_results=3)
    
    if not results['ids'] or not results['ids'][0]:
        raise HTTPException(status_code=404, detail="No jobs found in Vector DB!")
        
    final_results = []
    
    # 3. Loop through the 3 best jobs ChromaDB found
    for i in range(len(results['ids'][0])):
        job_id = results['ids'][0][i]
        job_json_string = results['documents'][0][i]
        
        # Turn the string from ChromaDB back into our strict Pydantic object
        parsed_jd = ParsedJD.model_validate_json(job_json_string)
        
        print(f"2. Running LLM Matcher for Job: {job_id}")
        match_result = calculate_match_score(parsed_jd, request.resume_text)
        
        # Save the result to send back to the user
        final_results.append({
            "job_id": job_id,
            "match_analysis": match_result.model_dump()
        })
        
    return {"status": "success", "matches": final_results}