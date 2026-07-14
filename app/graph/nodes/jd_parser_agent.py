from app.services.groq_client import get_llm, REASONING_MODEL
from app.models.schemas import ParsedJD



def parse_job_description(raw_text: str) -> ParsedJD:
    """
    Takes raw job description text and uses the LLM to extract structured data.
    """
    llm = get_llm(model_name=REASONING_MODEL)
    
    structured_llm = llm.with_structured_output(ParsedJD)
    
    prompt = f"""
    You are an expert technical recruiter. I will give you a raw job posting.
    Your task is to extract the exact skills, experience, and details required.
    Do not hallucinate or guess. If a field is not mentioned, use the actual JSON null data type (do NOT use the string "null").
    
    Raw Job Posting:
    {raw_text}
    """
    
    print("Agent is reading the job description...")
    result = structured_llm.invoke(prompt)
    
    return result
