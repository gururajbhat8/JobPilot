from app.services.groq_client import get_llm, REASONING_MODEL
from app.models.schemas import MatchResult, ParsedJD


def calculate_match_score(parsed_jd: ParsedJD, resume_text: str) -> MatchResult:
    """
    Compares a parsed job description against a user's resume to calculate a match score.
    """

    llm = get_llm(model_name=REASONING_MODEL)

    structured_llm = llm.with_structured_output(MatchResult)

    prompt = f"""
    You are an expert ATS (Applicant Tracking System) algorithm.
    I will provide you with the extracted requirements of a Job, and a Candidate's Resume.
    
    Your task is to:
    1. Calculate a match_score from 0 to 100 based on how well the skills and experience align.
    2. Identify any required_skills from the job that are missing in the resume.
    3. Provide a brief 2-sentence reasoning for your score.
    
    JOB REQUIREMENTS:
    {parsed_jd.model_dump_json(indent=2)}
    
    CANDIDATE RESUME:
    {resume_text}
    """
    
    print("Agent is analyzing the resume against the job...")
    result = structured_llm.invoke(prompt)
    
    return result