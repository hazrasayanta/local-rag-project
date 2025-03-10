from app.chromadb import add_document, search_documents
from app.utils.embedding_generator import generate_embedding

# Step 1: Generate embedding for a test document
test_text = "Fundamental analysis helps investors understand the market."
test_embedding = generate_embedding(test_text)

# Step 2: Add the document to ChromaDB
add_document(doc_id="test_doc_1", text=test_text, embedding=test_embedding)
print("✅ Document added to ChromaDB!")

# Step 3: Generate embedding for a search query
query_text = "What is fundamental analysis?"
query_embedding = generate_embedding(query_text)

# Step 4: Search for similar documents
search_results = search_documents(query_embedding, top_k=3)
print(f"🔍 Search Results:\n{search_results}")
