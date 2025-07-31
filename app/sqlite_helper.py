import sqlite3
import os

def init_sqlite():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(base_dir, "patent_data.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patent_chunks (
            vector_id TEXT PRIMARY KEY,
            patent_number TEXT,
            publication_id TEXT,
            family_id TEXT,
            publication_date TEXT,
            title TEXT,
            description TEXT,
            abstract TEXT,
            claims_text TEXT,
            chunk_text TEXT
        )
    ''')
    conn.commit()
    print(f"✅ SQLite DB Initialized at {db_path}")
    return conn, cursor

def insert_chunk_data(cursor, vector_id, patent_number, publication_id, family_id,
                      publication_date, title, description, abstract, claims_text, chunk_text):
    cursor.execute('''
        INSERT INTO patent_chunks (
            vector_id, patent_number, publication_id, family_id, publication_date,
            title, description, abstract, claims_text, chunk_text
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        vector_id, patent_number, publication_id, family_id, publication_date,
        title, description, abstract, claims_text, chunk_text
    ))

def close_sqlite(conn):
    conn.commit()
    conn.close()
    print("✅ SQLite DB Saved and Closed.")
