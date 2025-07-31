import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY1")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def init_pinecone():
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX_NAME)
        print(f"✅ Connected to Pinecone index: {PINECONE_INDEX_NAME}")
        return index
    except Exception as e:
        print(f"❌ Error initializing Pinecone: {e}")
        return None

def upsert_vectors(index, vectors, batch_size=100):
    try:
        total_vectors = len(vectors)
        print(f"📅 Upserting {total_vectors} vectors in batches of {batch_size}...")
        for i in range(0, total_vectors, batch_size):
            batch = vectors[i:i + batch_size]
            index.upsert(vectors=batch)
            print(f"✅ Batch {i//batch_size + 1}: Upserted {len(batch)} vectors")
        print("🎉 All vectors upserted successfully!")
        return True
    except Exception as e:
        print(f"❌ Error during upsert: {e}")
        return False

def semantic_search(index, query_vector, top_k=3):
    try:
        results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
        return results
    except Exception as e:
        print(f"❌ Error during semantic search: {e}")
        return None