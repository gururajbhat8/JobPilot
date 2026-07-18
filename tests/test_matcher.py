from app.graph.nodes.jd_parser_agent import parse_job_description
from app.graph.nodes.resume_matcher_agent  import calculate_match_score


# 1. The fake job description (Requires 5 years, FastAPI, Postgres)
sample_jd = """
We are looking for a Senior Python Developer.
Requirements:
- 5+ years of experience
- Strong knowledge of Python and FastAPI
- Experience with PostgreSQL and Docker
- AWS experience is a plus
"""

# 2. A fake resume (Has only 3 years, Django instead of FastAPI, SQL Server instead of Postgres)
sample_resume = """
John Doe - Software Engineer
Experience: 3 years building web apps.
Skills: Python, Django, SQL Server, Docker.
I have built multiple backend applications using Python and Django.
I know how to containerize apps with Docker.
"""

if __name__ == "__main__":
    print("Step 1: Parsing the Job Description (Fast 8b model)...")

    parsed_jd = parse_job_description(sample_jd)

    print("\nStep 2: Scoring the Resume (Smart 70b Reasoning model)...")

    result = calculate_match_score(parsed_jd, sample_resume)

    print("\n--- MATCH RESULT ---")
    
    print(result.model_dump_json(indent=2))