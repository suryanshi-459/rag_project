# 🧠 RAG-Powered Document Q&A System

A lightweight Retrieval-Augmented Generation (RAG) system built with FastAPI, LangChain, ChromaDB, and a locally hosted LLM (`EleutherAI/gpt-neo-125M`). This project enables users to upload PDF documents, embed their content, and ask context-aware questions with accurate source citations — all without using OpenAI APIs.

---

## 🚀 Features

- ✅ Upload and store PDF documents.
- ✅ Extract and chunk text intelligently.
- ✅ Generate embeddings using `all-MiniLM-L6-v2`.
- ✅ Store/retrieve vectors using **ChromaDB**.
- ✅ Run question-answering over embedded documents.
- ✅ Offline local LLM (`gpt-neo-125M`) for inference.
- ✅ Source tracking for generated answers.
- ✅ FastAPI-based backend with interactive Swagger UI.

---

## 🧰 Tech Stack

| Component       | Tool/Library                       |
|----------------|------------------------------------|
| Embeddings      | HuggingFace `all-MiniLM-L6-v2`     |
| Vector DB       | `ChromaDB`                         |
| LLM             | `EleutherAI/gpt-neo-125M` (offline)|
| Backend         | `FastAPI`, `Uvicorn`               |
| File parsing    | `PyMuPDF`, `langchain`             |
| TTS (optional)  | `pyttsx3` or `gTTS`                |

---
