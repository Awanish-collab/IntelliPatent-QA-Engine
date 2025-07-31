# IntelliPatent Q\&A Engine 🚀

A semantic search-driven Patent Q\&A Engine that retrieves the top relevant patent documents based on user queries and summarizes them using Groq LLM API. This project leverages Pinecone Vector DB, SQLite3, Sentence-Transformers, and FastAPI, fully containerized using Docker for scalable deployments.

---

## 🌟 Features

* 🔍 **Semantic Search** on Patent Abstract & Claims using 1024-dimension Vector Embeddings.
* 📊 **Metadata Storage & Retrieval** from SQLite3 DB.
* 📝 **Summarization of Descriptions** using Groq LLM API.
* 🔢 **FastAPI REST API Endpoint** for client integration.
* 🛣️ **Dockerized Environment** with Docker Compose support.
* 🧰 **Swagger UI & Postman Collection** for easy testing & demo.

---

## 📁 Project Structure

```bash
IntelliPatent-QA-Engine/
|
├── app/
│   ├── api_server.py          # FastAPI Server Endpoint
│   ├── data_loader.py         # Data Ingestion Pipeline (Embeddings + Pinecone + SQLite)
│   ├── pinecone_helper.py     # Pinecone Connection & Upsert/Search Helpers
│   ├── groq_helper.py         # Semantic Search & Summarization Workflow
│   ├── sqlite_helper.py       # SQLite DB Schema & Data Insertion Helpers
│   └── utils.py               # Utility Functions
|
├── patent_jsons/              # Folder with Raw Patent JSON Files
├── patent_data.db             # SQLite3 Database File (Auto-generated)
├── Dockerfile                 # Docker Build File
├── docker-compose.yml         # Docker Compose Orchestration
├── requirements.txt           # Python Package Requirements
├── .env                       # API Keys & Environment Variables
└── README.md                  # Documentation (This File)
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/IntelliPatent-QA-Engine.git
cd IntelliPatent-QA-Engine
```

### 2. Configure Environment Variables

Create a `.env` file at the root level with the following content:

```bash
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=patent-data
GROQ_API_KEY=your-groq-api-key
```

### 3. Build & Run Docker Containers

```bash
docker compose up --build
```

### 4. Process JSON Data (First Time Setup)

Before searching, ingest data into Pinecone & SQLite3 by running:

```bash
docker compose run --rm intellipatent-api python app/data_loader.py
```

---

## 🤕 API Usage Guide

### 1. Swagger UI Interface

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

### 2. Postman Collection

* Import the provided **IntelliPatent\_Postman\_Collection.json** into Postman.
* Use the **Search Patent** request to test queries like:

```json
{
    "query": "Summarize patents on microprocessor instruction pipelines."
}
```

---

## 📚 Example Queries You Can Try

| Sample Query                                                          |
| --------------------------------------------------------------------- |
| "Summarize a patent related to microprocessor instruction pipelines." |
| "Find patents discussing cache memory optimization techniques."       |
| "Summarize a patent about execution units in processors."             |
| "Summarize patents describing instruction throughput improvements."   |

---

## 🔹 Requirements

* Docker Desktop (Ensure WSL2 is installed & updated on Windows)
* Minimum 4GB RAM allocated to Docker Engine
* Pinecone API Access
* Groq API Key

---

## 📅 Deployment Notes

* By default, the API is exposed on **localhost:8000**.
* For LAN network access, you can expose IP-based ports.
* For cloud deployment (AWS EC2, Azure VM), Docker image can be deployed directly.

---

## 📁 Deliverables

* Source Code (This Repo)
* Dockerfile & docker-compose.yml
* .env.example file (without actual API keys)
* Postman Collection JSON for Demo
* SQLite DB auto-generated after data ingestion

---

## 🔹 License

MIT License (or your preferred licensing)

---

## 👨‍💻 Developed by

**Awanish Kumar**

---

## 📍 Connect

* LinkedIn: \[https://www.linkedin.com/in/awanish-kumar-0a04831a708/]

```

---

```
