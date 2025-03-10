from sentence_transformers import SentenceTransformer

# Load local embedding model (first download will take time)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str):
    """Generate embeddings for a given text using SentenceTransformers."""
    return embedding_model.encode(text).tolist()

# Test embedding generation
if __name__ == "__main__":
    sample_text = "This is a test document about AI."
    embedding = generate_embedding(sample_text)
    print(f"Generated Embedding: {embedding[:5]}...")  # Print first 5 values
