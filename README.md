# 🤖 06 - Advanced RAG

An Enterprise-style **Conversational Retrieval-Augmented Generation (RAG)** application built using **Python**, **FastAPI**, **Ollama**, and **FAISS**.

This project extends the RAG Foundation by introducing production-grade retrieval techniques such as **FAISS vector search**, **Hybrid Search**, **Metadata Filtering**, **LLM Re-ranking**, **Source Citations**, **PDF Knowledge Base**, and **Conversation-Aware Query Rewriting**.

Instead of simply retrieving relevant documents, this project demonstrates how modern AI assistants improve answer quality by combining semantic retrieval, keyword matching, conversational context, and grounded generation.

---

# 🎯 Objectives

- Understand Enterprise RAG Architecture
- Implement FAISS Vector Search
- Learn Hybrid Search (Semantic + Keyword)
- Perform Metadata Filtering
- Build LLM-based Re-ranking
- Add Confidence Threshold Filtering
- Support PDF Knowledge Bases
- Build Conversation Memory
- Implement Query Rewriting
- Generate Grounded Responses with Source Citations
- Understand Production RAG Design Patterns

---

# 🚀 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Framework | FastAPI |
| Validation | Pydantic |
| Database | SQLite |
| ORM | SQLAlchemy |
| LLM | Ollama (Qwen 3) |
| Embedding Model | nomic-embed-text |
| Vector Search | FAISS |
| PDF Parser | pypdf |
| Math Library | NumPy |

---

# ✨ Features

- Advanced Retrieval-Augmented Generation (RAG)
- FAISS Vector Index
- Semantic Search
- Keyword Search
- Hybrid Search
- Metadata Filtering
- LLM-based Re-ranking
- Confidence Threshold
- Source Citations
- PDF Knowledge Base
- Conversation Memory
- Query Rewriting
- Hallucination Prevention
- Repository Pattern
- Service Layer Architecture
- Layered Architecture

---

# 🏛️ Architecture

```text
                        User
                          │
                          ▼
                  FastAPI REST API
                          │
                          ▼
                   Query Rewriter
               (Conversation Memory)
                          │
                          ▼
                Standalone Question
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
  Semantic Search                  Keyword Search
      (FAISS)                      (Text Matching)
          │                               │
          └───────────────┬───────────────┘
                          ▼
                    Hybrid Search
                          │
                          ▼
                  LLM Re-ranking
                          │
                          ▼
                Confidence Threshold
                          │
                          ▼
                  Prompt Builder
                          │
                          ▼
                    Ollama (Qwen)
                          │
                          ▼
                  Grounded Answer
                          │
                          ▼
                 Source Citations
```

---

# 📂 Project Structure

```text
06-advanced-rag
│
├── clients/
├── config/
├── controllers/
├── knowledge/
├── models/
├── prompts/
├── repository/
├── schemas/
├── services/
├── utils/
├── app.py
└── requirements.txt
```

---

# ▶️ Getting Started

## Start Ollama

```bash
ollama serve
```

Pull required models

```bash
ollama pull qwen3:8b

ollama pull nomic-embed-text
```

Run application

```bash
uvicorn app:app --reload
```

Open Swagger

```text
http://localhost:8000/docs
```

---

# 📡 REST APIs

## POST `/api/load`

Load all knowledge files (.txt and .pdf) into the vector database.

---

## POST `/api/chat`

Ask questions against your knowledge base.

### Request

```json
{
    "question": "What is AWS Lambda?"
}
```

### Response

```json
{
    "answer": "AWS Lambda is a serverless compute service...",
    "sources": [
        {
            "document_name": "AWS_RAG_Test_Guide.pdf",
            "score": 9.8
        }
    ]
}
```

---

# 🧠 Advanced RAG Pipeline

```text
Knowledge Files
(txt / pdf)
       │
       ▼
Document Loader
       │
       ▼
Chunk Service
       │
       ▼
Embedding Generation
       │
       ▼
FAISS Vector Index
       │
       ▼
Semantic Search
       │
       ▼
Keyword Search
       │
       ▼
Hybrid Search
       │
       ▼
LLM Re-ranking
       │
       ▼
Confidence Threshold
       │
       ▼
Prompt Builder
       │
       ▼
LLM
       │
       ▼
Grounded Response
```

---

# 🔍 Hybrid Search

Instead of relying only on embeddings, this project combines two retrieval strategies.

```text
                User Question
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 Semantic Search              Keyword Search
        │                           │
        └─────────────┬─────────────┘
                      ▼
                Hybrid Results
```

Hybrid Search significantly improves retrieval accuracy by combining semantic understanding with traditional keyword matching.

---

# 🧠 FAISS Vector Search

FAISS indexes embedding vectors for efficient nearest-neighbor search.

```text
Documents
      │
      ▼
Embeddings
      │
      ▼
FAISS Index
      │
      ▼
Top-K Similar Chunks
```

Unlike linear search, FAISS is optimized for scalable vector retrieval.

---

# 🏷️ Metadata Filtering

Each document chunk stores metadata alongside its embedding.

```text
Chunk

id

document_name

category

topic

language

text

embedding
```

Metadata can be used to restrict search results before retrieval.

---

# 🎯 LLM Re-ranking

After retrieval, candidate documents are evaluated again using an LLM.

```text
Top-K Results
      │
      ▼
LLM Judge
      │
      ▼
Relevance Score
      │
      ▼
Sorted Results
```

This improves retrieval precision by selecting the most relevant context before answer generation.

---

# 📄 PDF Knowledge Base

The application supports multiple document formats.

```text
TXT

PDF

↓

Plain Text

↓

Chunking

↓

Embeddings

↓

FAISS
```

New document formats can be added without modifying the retrieval pipeline.

---

# 💬 Conversation Memory

Conversation history is stored in SQLite and used to improve follow-up questions.

Example

```text
User:
What is AWS Lambda?

Assistant:
AWS Lambda is a serverless compute service.

User:
What is its timeout?
```

The conversation history is retrieved before searching the knowledge base.

---

# 🔄 Query Rewriting

Before retrieval, the user's latest question is rewritten into a standalone question.

```text
Original Question

What is its timeout?

↓

Rewritten Question

What is the maximum execution timeout for AWS Lambda?
```

This dramatically improves retrieval quality for conversational AI.

---

# 📚 Source Citations

Every generated answer includes the supporting knowledge source.

Example

```json
{
    "answer": "The maximum execution timeout is 15 minutes.",
    "sources": [
        {
            "document_name": "AWS_RAG_Test_Guide.pdf",
            "score": 10
        }
    ]
}
```

Source citations increase transparency and user trust.

---

# 🧩 Repository Pattern

The application separates storage logic from business logic.

```python
vector_repository.add(chunk)

vector_repository.search(query)

message_repository.find_last_messages()
```

This allows the implementation to evolve without affecting service logic.

---

# 🧠 Concepts Explored

- Retrieval-Augmented Generation (RAG)
- Enterprise RAG Architecture
- FAISS Vector Search
- Semantic Search
- Keyword Search
- Hybrid Search
- Metadata Filtering
- LLM Re-ranking
- Confidence Threshold
- Query Rewriting
- Conversation Memory
- Source Citation
- PDF Parsing
- Repository Pattern
- Service Layer
- FastAPI
- SQLAlchemy
- SQLite
- Ollama
- Production AI Architecture

---

# 💡 Key Learnings

Building this project helped me understand:

- How Enterprise RAG systems improve retrieval quality
- Why FAISS is widely used for vector similarity search
- How Hybrid Search combines semantic and keyword retrieval
- How metadata filtering improves search precision
- Why LLM Re-ranking produces more relevant context
- How confidence thresholds reduce noisy retrieval results
- How conversational memory enables follow-up questions
- Why query rewriting is essential for conversational AI
- How PDF documents become searchable through embeddings
- Why source citations improve trust and explainability
- How to build production-style AI backend services using FastAPI, FAISS, SQLite, and Ollama

This project focuses on building a production-oriented Conversational RAG system before introducing AI Agents, Multi-Agent Systems, and autonomous AI workflows in the next project.