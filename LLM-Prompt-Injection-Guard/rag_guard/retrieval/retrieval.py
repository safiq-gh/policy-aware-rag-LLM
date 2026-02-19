from pathlib import Path
import json
import numpy as np
from langchain_ollama import OllamaEmbeddings


class JSONVectorStore:
    def __init__(self, store_path: Path):
        self.store_path = store_path
        
        with open(store_path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)
        
        # Convert embeddings to numpy arrays
        for doc in self.documents:
            doc["embedding"] = np.array(doc["embedding"])
    
    def similarity_search(self, query: str, k: int = 5):
        """Find k most similar documents using cosine similarity"""
        
        # Embed query
        embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://127.0.0.1:11434"
        )
        query_embedding = np.array(embeddings.embed_query(query))
        
        # Calculate cosine similarity with all documents
        scores = []
        for doc in self.documents:
            # Cosine similarity
            similarity = np.dot(query_embedding, doc["embedding"]) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc["embedding"]) + 1e-10
            )
            scores.append(similarity)
        
        # Get top k
        top_indices = np.argsort(scores)[-k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "text": self.documents[idx]["text"],
                "policy_id": self.documents[idx]["policy_id"],
                "section": self.documents[idx]["section"],
                "score": float(scores[idx])
            })
        
        return results


def retrieve_policy_context(query: str, k: int = 5):
    """Retrieve relevant policy chunks for user prompt"""
    
    STORE_PATH = Path(__file__).resolve().parents[1] / "vector_store.json"
    
    if not STORE_PATH.exists():
        print(f"Error: Vector store not found at {STORE_PATH}")
        print("Run build_index.py first!")
        return []
    
    vector_store = JSONVectorStore(STORE_PATH)
    return vector_store.similarity_search(query, k=k)


if __name__ == "__main__":
    print("Running retrieval test...")
    
    results = retrieve_policy_context("ignore previous instructions", k=3)
    
    print(f"Found {len(results)} results:")
    for r in results:
        print(f"\n[{r['policy_id']}] {r['section']}")
        print(f"Score: {r['score']:.4f}")
        print(f"Text: {r['text'][:100]}...")