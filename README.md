# IntelliPatent Q\&A Engine 🚀

A semantic search-driven Patent Q\&A Engine that retrieves the top relevant patent documents based on user queries and summarizes them using Groq LLM API. This project leverages Pinecone Vector DB, SQLite3, Sentence-Transformers, and FastAPI, fully containerized using Docker for scalable deployments.

---

## 🌟 Features

* 🔍 **Semantic Search** on Patent Abstract & Claims using 1024-dimension Vector Embeddings.
* 📊 **Metadata Storage & Retrieval** from SQLite3 DB.
* 📝 **Summarization of Descriptions** using Groq LLM API.
* 🖥️ **FastAPI REST API Endpoint** for client integration.
* 🐳 **Dockerized Environment** with Docker Compose support.
* 🧪 **Swagger UI & Postman Collection** for easy testing & demo.

---

## 📁 Project Structure

```
IntelliPatent-QA-Engine/
│
├── app/
│   ├── api_server.py          # FastAPI Server Endpoint
│   ├── data_loader.py         # Data Ingestion Pipeline (Embeddings + Pinecone + SQLite)
│   ├── pinecone_helper.py     # Pinecone Connection & Upsert/Search Helpers
│   ├── groq_helper.py         # Semantic Search & Summarization Workflow
│   ├── sqlite_helper.py       # SQLite DB Schema & Data Insertion Helpers
│   └── utils.py               # Utility Functions
│
├── patent_jsons/              # Folder with Raw Patent JSON Files
│   ├── US-4794521-A.json
│   ├── US-5109498-A.json
│   └── ...
│
├── postman/
│   └── IntelliPatent_Postman_Collection.json  # Postman Collection for API Testing
│
├── patent_data.db             # SQLite3 Database File (Auto-generated after data ingestion)
├── .env.example               # Example file for API keys and environment variables
├── Dockerfile                 # Docker Build File
├── docker-compose.yml         # Docker Compose Orchestration
├── requirements.txt           # Python Package Requirements
└── README.md                  # This Documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/IntelliPatent-QA-Engine.git
cd IntelliPatent-QA-Engine
```

### 2️⃣ Configure Environment Variables

Create a `.env` file at the root level with the following content:

```bash
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=patent-data
GROQ_API_KEY=your-groq-api-key
```

Refer `.env.example` file as reference.

### 3️⃣ Build & Run Docker Containers

```bash
docker compose up --build
```

### 4️⃣ Process Patent JSON Data (Run Once for Ingestion)

Before searching, ingest patent data into Pinecone & SQLite3 by running:

```bash
docker compose run --rm intellipatent-api python app/data_loader.py
```

This will process JSON files, upsert vectors to Pinecone, and store metadata in SQLite DB.

---

## 🧪 API Usage Guide

### 1️⃣ Swagger UI Interface

Access the interactive API Docs at:

```
http://localhost:8000/docs
```

Test the `/search` endpoint directly with queries like:

```json
{
    "query": "Summarize a patent about data processors."
}
```

### 2️⃣ Postman Collection

* Import the provided **postman/IntelliPatent\_Postman\_Collection.json** into Postman.
* Use the **Search Patent** request to test queries like:

```json
{
    "query": "Summarize patents on microprocessor instruction pipelines."
}
```

---

## 📄 Example Queries You Can Try

| Sample Query                                                          |
| --------------------------------------------------------------------- |
| "Summarize a patent related to microprocessor instruction pipelines." |
| "Find patents discussing cache memory optimization techniques."       |
| "Summarize a patent about execution units in processors."             |
| "Summarize patents describing instruction throughput improvements."   |

---

## 📦 Deliverables

* Source Code Repository (This Repo)
* Dockerfile & docker-compose.yml
* .env.example file (without actual API keys)
* Postman Collection JSON file (in /postman folder)
* SQLite DB auto-generated after data ingestion

---

## 🔧 Requirements

* Docker Desktop (Ensure WSL2 is installed & updated on Windows)
* Minimum 4GB RAM allocated to Docker Engine
* Pinecone API Access (for Vector DB)
* Groq API Key (for summarization)

---

## 📝 Deployment Notes

* API runs on **localhost:8000** after docker-compose up.
* For LAN network or Cloud Deployment, expose ports accordingly.
* Docker Compose handles all service orchestration.

---

## 🆘 Troubleshooting

| Symptom                        | Solution                                           |
| ------------------------------ | -------------------------------------------------- |
| API stuck at embedding         | Ensure Docker has 4-6GB RAM allocated              |
| Invalid Pinecone API Key error | Check `.env` for API key correctness (no quotes)   |
| SQLite returns empty result    | Ensure data\_loader.py ran successfully            |
| Groq API Token Errors          | Check token limits on Groq Dashboard & reduce size |

---


## 🔹 License

MIT License (or your preferred licensing)

---

## 👨‍💻 Developed by

**Awanish Kumar**

## 📌 Connect

* [LinkedIn](https://www.linkedin.com/in/awanish-kumar-0a04831a708/)
* [GitHub](https://github.com/Awanish-collab)

