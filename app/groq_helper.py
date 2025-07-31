import os
import sqlite3
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from app.pinecone_helper import init_pinecone, semantic_search
import requests

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"  # You can change model here

# Load embedding model
def load_embedding_model():
    print("🔄 Loading BAAI/bge-large-en model for query embedding...")
    model = SentenceTransformer('BAAI/bge-large-en')
    print("✅ Model Loaded Successfully!")
    return model

# Embed user query
def embed_query(query, model):
    return model.encode(query).tolist()

# Fetch full data from SQLite using vector IDs
def fetch_from_sqlite(vector_ids):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(base_dir, "patent_data.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    placeholders = ','.join('?' for _ in vector_ids)
    query = f"SELECT vector_id, patent_number, title, description FROM patent_chunks WHERE vector_id IN ({placeholders})"
    cursor.execute(query, vector_ids)
    results = cursor.fetchall()

    conn.close()
    return results

# Summarize text using Groq API
def summarize_text(text):
    # Truncate description if too large
    max_chars = 4000
    if len(text) > max_chars:
        print(f"⚠️ Description too large ({len(text)} chars). Truncating to {max_chars} chars.")
        text = text[:max_chars]

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes patent descriptions."},
            {"role": "user", "content": f"Summarize this patent description:\n\n{text}"}
        ],
        "temperature": 0.4,
        "max_tokens": 2000
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        print(f"❌ Groq API Error: {response.status_code} - {response.text}")
        return "Summary generation failed."

# Main Semantic Search + Summarization Pipeline
def search_and_summarize(query):
    model = load_embedding_model()
    index = init_pinecone()

    print(f"🔍 Generating embedding for query: '{query}'")
    query_vector = embed_query(query, model)

    print("🔎 Performing Semantic Search in Pinecone...")
    results = semantic_search(index, query_vector, top_k=3)

    print("Results from Semantic Search: ", results)

    if not results or 'matches' not in results.to_dict():
        print("❌ No results found in Pinecone.")
        return

    vector_ids = [match['id'] for match in results.to_dict()['matches']]
    print(f"🔗 Retrieved Vector IDs: {vector_ids}")

    print("📥 Fetching detailed info from SQLite DB...")
    records = fetch_from_sqlite(vector_ids)

    print("\n📄 Top Matching Patents Summary:\n")
    results_list = []
    for rec in records:
        vector_id, patent_number, title, description = rec
        print(f"Patent Number: {patent_number}")
        print(f"Title: {title}")

        summary = summarize_text(description)
        print(f"📝 Summary: {summary}\n")
        print("="*50)
        results_list.append({
            "patent_number": patent_number,
            "title": title,
            "summary": summary
        })

    return results_list


# Example Run
if __name__ == "__main__":
    user_query = input("Enter your search query: ")
    search_and_summarize(user_query)
