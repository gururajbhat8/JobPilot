from app.services.vector_db import add_job_to_vector_db, search_similar_jobs

if __name__ == "__main__":
    print("Step 1: Adding jobs to Vector DB (This might take 10 seconds the very first time as it downloads the math model)...")

    # Adding a React job
    add_job_to_vector_db(
        job_id="job_react_1",
        job_text="Frontend Developer. Looking for React and Tailwind CSS experts."
    )

    print("\nStep 2: Searching Vector DB with a fake Python resume...")

    # fr testing we don't say "Django" or "REST APIs" here!
    my_resume = "I am a software engineer. I build backend systems using Python."

    results = search_similar_jobs(resume_text=my_resume, n_results=1)

    print("\n--- TOP MATCH ---")
    print(f"Matched Job ID: {results['ids'][0][0]}")
    print(f"Distance Score (lower is better): {results['distances'][0][0]}")