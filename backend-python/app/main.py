from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.chromadb import add_document, search_documents
from app.utils.pdf_parser import extract_text_from_pdf
from app.utils.embedding_generator import generate_embedding
from app.llm_mistral import generate_response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

# ✅ Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_FOLDER = Path("data/documents")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Define a request model for document addition
class DocumentRequest(BaseModel):
    doc_id: str
    text: str
    embedding: list

# Define request model
class SearchRequest(BaseModel):
    query: str

# Define request model
class LLMRequest(BaseModel):
    prompt: str
    max_tokens: int = 128

# Define request model
class RAGRequest(BaseModel):
    query: str
    top_k: int = 3
    max_tokens: int = 128

def stream_mistral_response(prompt, max_tokens):
    """Generator function to stream responses."""
    for chunk in generate_response(prompt, max_tokens, stream=True):  # Ensure `stream=True`
        yield chunk               

@app.post("/add-document/")
def add_doc(doc: DocumentRequest):
    add_document(doc.doc_id, doc.text, doc.embedding)
    return {"message": "Document added successfully"}

# Define a request model for search queries
class SearchRequest(BaseModel):
    query_embedding: list

@app.post("/search/")
def search_docs(query: SearchRequest):
    results = search_documents(query.query_embedding)
    return results

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF, extract text, generate embeddings, and store in ChromaDB."""
    file_path = UPLOAD_FOLDER / file.filename

    with file_path.open("wb") as buffer:
        buffer.write(await file.read())

    text = extract_text_from_pdf(str(file_path))
    embedding = generate_embedding(text)

    add_document(file.filename, text, embedding)

    return {"filename": file.filename, "extracted_text": text[:500], "embedding_sample": embedding[:5]}

@app.post("/search-docs/")
def search_docs(request: SearchRequest, top_k: int = 5):
    """Generate embedding for query and retrieve relevant documents."""
    
    # Generate embedding
    query_embedding = generate_embedding(request.query)
    print(f"Generated Embedding: {query_embedding[:5]}")  # Debugging output

    # Perform vector search
    results = search_documents(query_embedding, top_k)

    return {"query": request.query, "results": results}

@app.post("/generate/")
def generate_text(request: LLMRequest):
    """Generate text using Mistral-7B via llama.cpp."""
    response = generate_response(request.prompt, request.max_tokens)
    return {"prompt": request.prompt, "response": response}

# @app.post("/rag-query/")
# def rag_query(request: RAGRequest):
#     """Retrieve relevant documents and generate a response using Mistral-7B."""
    
#     # Step 1: Generate query embedding
#     query_embedding = generate_embedding(request.query)
    
#     # Step 2: Retrieve top_k relevant documents from ChromaDB
#     results = search_documents(query_embedding, request.top_k)
    
#     # Step 3: Combine retrieved documents into a context
#     context = "\n".join([doc["document"] for doc in results])
    
#     # Step 4: Generate response using Mistral-7B
#     prompt = f"Using the following context:\n{context}\n\nAnswer the query: {request.query}"
#     response = generate_response(prompt, request.max_tokens)

#     return {"query": request.query, "response": response, "retrieved_docs": results}

@app.post("/rag-query/")
def rag_query(request: RAGRequest):
    """Retrieve relevant documents and stream Mistral-7B's response."""
    query_embedding = generate_embedding(request.query)
    results = search_documents(query_embedding, request.top_k)
    context = "\n".join([doc["document"] for doc in results])

    prompt = f"Using the following context:\n{context}\n\nAnswer the query: {request.query}"
    
    return StreamingResponse(stream_mistral_response(prompt, request.max_tokens), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
