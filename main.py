from fastapi import FastAPI, UploadFile, File, HTTPException
from ingest import ingest_pdf, list_ingested_documents
from ollama_api import retrieve_context, call_llama_with_context

app = FastAPI()

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDFs are supported.")

    pdf_bytes = await file.read()
    try:
        doc_id = ingest_pdf(pdf_bytes)
        return {"doc_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summarize/{doc_id}")
async def summarize_doc(doc_id: str):
    query = "Summarize the legal judgment with structured details."
    context = retrieve_context(doc_id, query)
    result = call_llama_with_context(context)
    return {"doc_id": doc_id, "summary": result}

@app.get("/documents/")
async def get_documents():
    return {"documents": list_ingested_documents()}
