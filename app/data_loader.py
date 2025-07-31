import os
import json
import uuid
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from pinecone_helper import init_pinecone, upsert_vectors
from sqlite_helper import init_sqlite, insert_chunk_data, close_sqlite

load_dotenv()

def load_embedding_model():
    print("🔄 Loading BAAI/bge-large-en model...")
    model = SentenceTransformer('BAAI/bge-large-en')
    print("✅ Model Loaded Successfully!")
    return model

def load_patent_files(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".json")]

def split_text_into_chunks(text, chunk_size=2500, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

def generate_embedding(text, model):
    try:
        return model.encode(text).tolist()
    except Exception as e:
        print(f"❌ Embedding failed: {e}")
        return None

def extract_english_field(entries, field_name):
    for entry in entries:
        if entry.get("lang") == "EN":
            return entry.get(field_name, "")
    return ""

def process_and_upsert_patents():
    model = load_embedding_model()
    index = init_pinecone()
    file_paths = load_patent_files("patent_jsons")
    print(f"📊 Total Patent Files Found: {len(file_paths)}")

    conn, cursor = init_sqlite()
    total_chunks = 0
    count = 1
    for file_idx, file_path in enumerate(file_paths):
        vectors = []
        file_name = os.path.basename(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                patent = json.load(f)
                print()
                print(f"✅ Processing File {count}: {file_name}")
                print()
                count += 1
        except Exception as e:
            print(f"❌ Failed to load {file_name}: {e}")
            continue

        patent_number = patent.get("patent_number", f"patent_{file_idx}")
        publication_id = patent.get("publication_id", "")
        family_id = patent.get("family_id", "")
        publication_date = patent.get("publication_date", "")

        title = extract_english_field(patent.get("titles", []), "text")
        abstract = extract_english_field(patent.get("abstracts", []), "paragraph_markup")
        description = extract_english_field(patent.get("descriptions", []), "paragraph_markup")

        claims_data = patent.get("claims", [{}])[0].get("claims", [])
        claims_text = " ".join([c.get("paragraph_markup", "") for c in claims_data if c.get("lang") == "EN"])

        combined_text = f"{abstract} {claims_text}".strip()

        if not combined_text:
            print(f"⚠️ Skipping {patent_number}: No Abstract/Claims found.")
            continue

        chunks = split_text_into_chunks(combined_text)
        print(f"📄 {patent_number}: {len(chunks)} chunks created.")

        for chunk_idx, chunk in enumerate(chunks):
            vector_id = f"{patent_number}_chunk_{chunk_idx}_{str(uuid.uuid4())[:8]}"
            embedding = generate_embedding(chunk, model)
            if embedding is None:
                continue

            metadata = {
                "patent_number": patent_number,
                "title": title
            }

            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": metadata
            })
            total_chunks += 1

            insert_chunk_data(
                cursor, vector_id, patent_number, publication_id, family_id,
                publication_date, title, description, abstract, claims_text, chunk
            )
            print(f"🟢 Vector & DB Entry Ready: {vector_id}")

        if vectors:
            upsert_vectors(index, vectors)
        else:
            print(f"❌ No vectors to upsert for {file_name}")

    close_sqlite(conn)
    print(f"📊 Total Chunks Processed: {total_chunks}")

if __name__ == "__main__":
    process_and_upsert_patents()