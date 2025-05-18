This project provides an API to:

* Upload legal PDF documents
* Embed them using `nomic-embed-text` via Ollama
* Store vector data in Qdrant
* Use RAG with LLaMA 3.2 to extract structured legal summaries

Built with FastAPI + Ollama + Qdrant.

---

##  Features

*  Upload PDFs & store document chunks as embeddings
*  Query document using LLaMA 3.2 via RAG
*  Structured JSON output for legal summaries
*  List all uploaded documents

---

##  Prerequisites

Install the following:

###  Python

```bash
conda create -n vakeelai python=3.10 -y
conda activate vakeelai
```

###  Python Libraries

```bash
pip install -r requirements.txt
```

> `requirements.txt`:

```
fastapi
uvicorn
requests
PyMuPDF
qdrant-client
```

---

###  Ollama (for embeddings + LLM)

1. **Download and install Ollama:**
    [https://ollama.com/download](https://ollama.com/download)

2. **Run Ollama server**:

```bash
ollama serve
```

3. **Pull and run embedding model:**

```bash
ollama pull nomic-embed-text
```

4. **Pull and run LLaMA model for answering:**

```bash
ollama pull llama3:instruct
```

---

###  Qdrant (Vector DB)

You can either:

#### 🔹 Run with Docker (recommended)

```bash
docker run -p 6333:6333 qdrant/qdrant
```

or

#### 🔹 Run natively

* Download binary: [https://github.com/qdrant/qdrant/releases](https://github.com/qdrant/qdrant/releases)
* Run `qdrant.exe` or the equivalent file
* Confirm it's running at: [http://localhost:6333](http://localhost:6333)

---

##  Running the App

```bash
uvicorn main:app --reload
```

Then open:
 [http://localhost:8000/docs](http://localhost:8000/docs)
(Interactive Swagger UI)

---

##  API Endpoints

| Endpoint              | Method | Description                                    |
| --------------------- | ------ | ---------------------------------------------- |
| `/upload/`            | POST   | Upload a legal PDF and store its embeddings    |
| `/summarize/{doc_id}` | GET    | Query a structured summary of a given document |
| `/documents/`         | GET    | List all ingested document IDs (doc\_ids)      |

---

##  Example Usage

1. Upload a PDF → receive `doc_id`
2. Use `/summarize/{doc_id}` → returns:

```json
{
  "case_title": "...",
  "parties_involved": "...",
  "court_name": "...",
  "important_dates": "...",
  "legal_issues": "...",
  "decision_summary": "...",
  "overall_summary": "..."
}
```


Sample output from a legal document:

```json
{
  "case_title": "Small Scale Industrial Manufactures Association (Regd.) v. Union of India and Others",
  "parties_involved": "Small Scale Industrial Manufactures Association (Petitioner) vs. Union of India and Others (Respondents)",
  "court_name": "Supreme Court of India",
  "important_dates": {
    "judgment_date": "March 23, 2021",
    "rbi_notification": "March 27, 2020",
    "moratorium_end": "August 31, 2020",
    "resolution_mechanism_deadline": "December 31, 2020"
  },
  "legal_issues": [
    "Judicial review of economic and financial policy decisions by the Government and RBI during COVID-19 pandemic",
    "Waiver of interest and compound interest during moratorium",
    "Extension of moratorium period",
    "Sector-wise relief packages",
    "Validity and sufficiency of financial packages under Disaster Management Act, 2005"
  ],
  "decision_summary": "The Supreme Court held that matters of economic policy are within the domain of the government and RBI, not ordinarily amenable to judicial review. However, it directed that no compound interest or penal interest be charged during the moratorium period, and any such amount already collected must be refunded or adjusted. All other reliefs sought were dismissed.",
  "overall_summary": "This case dealt with multiple writ petitions filed by various industry groups and individuals seeking financial relief due to COVID-19. The court reaffirmed the limited scope of judicial review in economic matters, declined to interfere with RBI and government policy decisions, but allowed partial relief by prohibiting interest on interest during the loan moratorium. The judgment emphasized reliance on expert bodies like RBI for financial policy and upheld the framework of the Disaster Management Act, 2005 as constitutionally adequate."
}
```