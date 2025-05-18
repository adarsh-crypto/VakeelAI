import fitz
import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import requests

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def extract_text_chunks(pdf_bytes, chunk_size=1000):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    full_text = "\n".join(page.get_text() for page in doc)
    return [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]

def embed_text_ollama(text):
    response = requests.post("http://localhost:11434/api/embeddings", json={
        "model": "nomic-embed-text",
        "prompt": text
    })

    try:
        data = response.json()
        if 'embedding' not in data:
            print(" Ollama returned:", data)
            raise ValueError("Ollama response missing 'embedding' key")
        return data['embedding']
    except Exception as e:
        print(" Failed to get embedding from Ollama:", e)
        raise

def ingest_pdf(pdf_bytes):
    chunks = extract_text_chunks(pdf_bytes)
    doc_id = hashlib.sha1(pdf_bytes).hexdigest()

    client.recreate_collection(
        collection_name=doc_id,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )

    points = []
    for i, chunk in enumerate(chunks):
        embedding = embed_text_ollama(chunk)
        points.append(PointStruct(id=i, vector=embedding, payload={"text": chunk}))

    client.upload_points(collection_name=doc_id, points=points)
    return doc_id

def list_ingested_documents():
    collections = client.get_collections()
    return [collection.name for collection in collections.collections]
