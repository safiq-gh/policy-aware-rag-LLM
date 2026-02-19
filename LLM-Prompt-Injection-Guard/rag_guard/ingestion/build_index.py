from pathlib import Path
import re
import sys
import json
from langchain_ollama import OllamaEmbeddings

# ---- POLICY PATH ----
POLICY_DIR = Path(r"C:\Users\User\Desktop\LLM-SLM\LLM-Prompt-Injection-Guard\policies")


def split_sections(text: str):
    pattern = r"## (.+)"
    parts = re.split(pattern, text)

    sections = []
    for i in range(1, len(parts), 2):
        sections.append({
            "section": parts[i].strip(),
            "text": parts[i + 1].strip()
        })
    return sections


def load_policy_chunks():
    chunks = []

    for file in POLICY_DIR.glob("*.md"):
        policy_id = file.stem

        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        for idx, sec in enumerate(split_sections(text)):
            chunks.append({
                "id": f"{policy_id}_{idx}",
                "policy_id": policy_id,
                "section": sec["section"],
                "text": sec["text"]
            })

    return chunks


def split_long_text(text, max_chars=700):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]


def build_vector_store(chunks):

    print("Entered build_vector_store", flush=True)
    sys.stdout.flush()

    # ---- Build embedding docs ----
    docs = []

    for c in chunks:
        for i, piece in enumerate(split_long_text(c["text"])):
            docs.append({
                "id": f"{c['id']}_{i}",
                "text": piece,
                "policy_id": c["policy_id"],
                "section": c["section"]
            })

    print(f"Created {len(docs)} embedding documents", flush=True)
    sys.stdout.flush()

    # ---- Embedding model ----
    print("Initializing embeddings...", flush=True)
    sys.stdout.flush()
    
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://127.0.0.1:11434"
    )
    print("Embeddings initialized", flush=True)
    sys.stdout.flush()

    # ---- Embed batched ----
    BATCH = 10
    all_embeddings = []

    print("Embedding documents...", flush=True)
    sys.stdout.flush()

    for i in range(0, len(docs), BATCH):
        batch = docs[i:i+BATCH]
        texts = [d["text"] for d in batch]

        print(f"Embedding batch {i//BATCH + 1} / {(len(docs)-1)//BATCH + 1}", flush=True)
        sys.stdout.flush()

        batch_embeds = embeddings.embed_documents(texts)
        all_embeddings.extend(batch_embeds)

    print(f"Embedding complete ({len(all_embeddings)} vectors)", flush=True)
    sys.stdout.flush()

    # ---- Store in JSON ----
    DB_PATH = Path(__file__).resolve().parents[1] / "vector_store.json"
    print(f"Saving to: {DB_PATH}", flush=True)
    sys.stdout.flush()

    # Combine docs with embeddings
    vector_store = []
    for idx, doc in enumerate(docs):
        vector_store.append({
            "id": doc["id"],
            "text": doc["text"],
            "embedding": all_embeddings[idx],
            "policy_id": doc["policy_id"],
            "section": doc["section"]
        })

    # Write to JSON
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(vector_store, f)

    print(f"✓ Saved {len(vector_store)} vectors to JSON", flush=True)
    sys.stdout.flush()

    print("✓ Vector store built successfully!", flush=True)
    sys.stdout.flush()


if __name__ == "__main__":
    chunks = load_policy_chunks()
    print("Total chunks:", len(chunks))
    build_vector_store(chunks)