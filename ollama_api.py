from qdrant_client import QdrantClient
import requests
from ingest import embed_text_ollama

FIELDS = [
    "Case Title",
    "Parties Involved",
    "Court Name",
    "Important Dates",
    "Legal Issues",
    "Decision Summary",
    "Overall Summary"
]

def retrieve_context(doc_id, query, top_k=5):
    client = QdrantClient("localhost", port=6333)
    query_vec = embed_text_ollama(query)
    search_result = client.search(
        collection_name=doc_id,
        query_vector=query_vec,
        limit=top_k
    )
    return "\n\n".join(hit.payload["text"] for hit in search_result)

def call_llama_with_context(context):
    prompt = f"""
You are a legal assistant. Given the following legal judgment text, extract:
- Case Title
- Parties Involved
- Court Name
- Important Dates
- Legal Issues
- Decision Summary
- Overall Summary

Return only a valid JSON object with the following keys:
case_title, parties_involved, court_name, important_dates, legal_issues, decision_summary, overall_summary.

Legal Text:
{context}
"""

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })
    return response.json()['response']
