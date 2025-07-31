from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY1")
index_name = os.getenv("PINECONE_INDEX_NAME")

print(f"API Key: {api_key}")

pc = Pinecone(api_key=api_key)
print(pc.list_indexes())

index = pc.Index(index_name)
print(f"Connected to index: {index_name}")


from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_7BaHzS_UZ7tvdDE3J9WoUhJcPvcacoG9mDe5AXyp1mHw4aZTmjRPa7hW7GWJRcHCSFNqny")
index = pc.Index("patent-data")

print(index.describe_index_stats())