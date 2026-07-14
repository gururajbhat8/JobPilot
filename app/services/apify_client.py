import os 
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

client = ApifyClient(os.getenv("APIFY_API_TOKEN"))


def scrape_jobs(keywords: str, location: str, max_items: int = 2):
    """
    Triggers an Apify actor to scrape jobs and returns the raw dataset.
    """

    ACTOR_ID = "curious_coder/linkedin-jobs-scraper" 

    url_keywords = keywords.replace(" ", "%20")
    url_location = location.replace(" ", "%20")
    
    # Build the actual LinkedIn search link bcz this actor designed like this.
    search_link = f"https://www.linkedin.com/jobs/search/?keywords={url_keywords}&location={url_location}"
    
    run_input = {
        "urls": [search_link], 
        "count": max_items,            # Using 'count' instead of 'maxItems'!
        "scrapeCompany": False         # We can set this to False to make it run faster
    }

    print(f"Triggering Apify Scraper for '{keywords}' in '{location}' ...")


    try: 
        run = client.actor(ACTOR_ID).call(run_input=run_input)

    # Once finished, pull all the scraped jobs from the Apify database
        dataset = client.dataset(run.default_dataset_id).list_items().items
    
        return dataset

    except Exception as e:
        print(f"Apify API Error (Check your internet or API key): {e}")

        return []