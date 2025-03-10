import chromadb

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./data/chromadb")

# Ensure collection is created with correct dimension (384)
collection = chroma_client.get_or_create_collection(
    name="documents", metadata={"hnsw:space": "cosine"}, embedding_function=None
)

def add_document(doc_id: str, text: str, embedding: list):
    """Add a document with an embedding to ChromaDB."""
    collection.add(ids=[doc_id], documents=[text], embeddings=[embedding])

def search_documents(query_embedding: list, top_k: int = 5):
    """Search for similar documents using query embedding."""
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    # Extract matched documents and similarity scores
    matched_docs = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]

    return [{"document": doc, "score": 1 - dist} for doc, dist in zip(matched_docs, distances)]
