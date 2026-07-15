# 🚀 JobPilot: AI-Powered Applicant Tracking System (ATS)

JobPilot is a production-grade AI Agent pipeline built to autonomously scrape, process, and match candidate resumes to real-world job postings using advanced large language models (LLMs) and vector search.

## 🧠 System Architecture

1. **Data Ingestion (Apify & PostgreSQL):** Uses an Apify Scraper Agent to bypass bot protection and fetch real LinkedIn job postings. Raw data is persisted in a Dockerized PostgreSQL database.
2. **Orchestration (LangGraph):** A state machine orchestrates the data pipeline, automatically passing jobs between specialized AI agents.
3. **Structured Extraction (Groq + Llama-3-8b):** The fast Llama-3-8b model parses unstructured paragraphs into a strict, predictable JSON schema using Pydantic.
4. **Vector Retrieval (ChromaDB):** Converts structured job requirements into mathematical vectors, enabling blazing-fast Semantic Search without hitting the LLM for every job.
5. **Reasoning Engine (Groq + Llama-3-70b):** The massive 70b reasoning model cross-references user resumes against the top 3 vector matches to generate a 0-100 match score and missing skills feedback.
6. **API Layer (FastAPI):** Exposes the entire pipeline via a REST API endpoint.

## 🛠️ Tech Stack

- **Framework:** FastAPI, Uvicorn
- **AI & Orchestration:** LangGraph, LangChain, Groq API (Llama-3 8b & 70b)
- **Database:** PostgreSQL (Dockerized), SQLAlchemy, Pydantic
- **Vector Search:** ChromaDB, Sentence-Transformers
- **Data Ingestion:** Apify Client

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.13+
- Docker Desktop
- [Groq API Key](https://console.groq.com/)
- [Apify API Token](https://console.apify.com/)

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/gururajbhat8/JobPilot.git
cd JobPilot
python -m venv jobpilot
jobpilot\Scripts\activate  # On Mac/Linux use: source jobpilot/bin/activate
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key
APIFY_API_TOKEN=your_apify_api_token
```

### 4. Start the Database
Spin up the PostgreSQL container:
```bash
docker compose up -d
```

### 5. Run the Pipeline & API
Run the LangGraph pipeline to scrape and vectorize jobs:
```bash
python test_pipeline.py
```
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
Navigate to `http://127.0.0.1:8000/docs` to test the `/match` endpoint via the interactive Swagger UI!

## 📄 License
This project is licensed under the MIT License.
