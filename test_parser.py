from app.graph.nodes.jd_parser_agent import parse_job_description


# messy job description, for testing. 
sample_jd = """
We are looking for a Senior Python Developer to join our team in London (Hybrid).
You will be working on our core backend systems.
Requirements:
- 5+ years of software engineering experience
- Strong knowledge of Python and FastAPI
- Experience with PostgreSQL and Docker
- React and AWS experience is a plus
Salary: $100k - $130k
"""

if __name__ == "__main__":
    print("Starting test.......... ")

    result = parse_job_description(sample_jd)

    print("\n --- Extraction Result ---")

    print(result.model_dump_json(indent=2))