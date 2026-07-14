from ast import keyword
from app.graph.nodes.scraper_agent import run_scraper_and_save

if __name__ == "__main__":
    print("Testing the Scraper Agent...")

    # We are just asking for 1 job so it runs quickly and saves your credits!
    saved_jobs = run_scraper_and_save(
        keywords="Python Backend Developer",
        location="Remote", 
        max_items=10
    )

    if saved_jobs:
        print("\n--- SUCCESS! ---")
        print(f"Job ID in Database: {saved_jobs[0].id}")
        print(f"Title: {saved_jobs[0].title}")
        print(f"Company: {saved_jobs[0].company}")
        print("Raw text length:", len(saved_jobs[0].raw_text))
    else:
        print("\n--- FAILED (No jobs returned) ---")