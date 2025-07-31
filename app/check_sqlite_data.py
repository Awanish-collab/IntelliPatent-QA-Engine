import sqlite3

# Connect to the SQLite DB (should be at project root level)
conn = sqlite3.connect('patent_data.db')
cursor = conn.cursor()

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patent_chunks';")
table_exists = cursor.fetchone()

if table_exists:
    print("✅ Table 'patent_chunks' exists.")
    
    # Count how many rows (chunks) are inserted
    cursor.execute("SELECT COUNT(*) FROM patent_chunks;")
    row_count = cursor.fetchone()[0]
    print(f"📊 Total Chunks Stored: {row_count}")

    # Fetch 1-2 sample records
    cursor.execute("SELECT vector_id, patent_number, title FROM patent_chunks LIMIT 2;")
    rows = cursor.fetchall()
    for row in rows:
        print(f"🔹 Vector ID: {row[0]}, Patent: {row[1]}, Title: {row[2]}")

else:
    print("❌ Table 'patent_chunks' does NOT exist. Data insertion might have failed!")

conn.close()
