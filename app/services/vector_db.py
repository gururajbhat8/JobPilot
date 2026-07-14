import chromadb 
from chromadb.utils import embedding_functions

chroma_client = chromadb.PersistentClient(path = "./chroma_db")

#choosing default embedding model
sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name="job_postings",
    embedding_function= sentence_transformer_ef
)

def add_job_to_vector_db(job_id: str, job_text: str):
    """
    Converts a job description into a mathematical vector and saves it to ChromaDB.
    """
    collection.add(
        documents=[job_text],
        ids = [job_id]
    )


def search_similar_jobs(resume_text: str, n_results: int = 3):
    """
    Uses fast geometry to find the most semantically similar jobs to your resume.
    """

    results = collection.query(
        query_texts=[resume_text],
        n_results=n_results
    )

    return results