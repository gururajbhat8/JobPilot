# JobPilot
A multi-agent LangGraph pipeline that scrapes live job postings via Apify, scores them against a resume using local embeddings + ChromaDB, runs a RAGAS-style faithfulness check via a critic agent, and generates tailored resume bullets for strong matches using Groq LLMs.
