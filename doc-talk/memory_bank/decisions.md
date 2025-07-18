# Architectural Decision Record

This document logs the key decisions made during the development of the Doc-Talk application.

## ADR-001: Choice of Web Framework

- **Decision:** Use FastAPI as the web framework.
- **Reasoning:** FastAPI is a modern, high-performance web framework for Python. It's easy to use, has automatic interactive documentation generation (which is great for testing), and is built on modern Python features like type hints.

## ADR-002: Choice of Vector Store

- **Decision:** Use FAISS (Facebook AI Similarity Search) as the vector store.
- **Reasoning:** FAISS is a highly efficient library for similarity search. For this project, we are using the CPU version (`faiss-cpu`), which is simple to set up and runs entirely in memory. This is ideal for a self-contained application that processes documents on the fly without needing a separate database server.

## ADR-003: Choice of LLM and Embedding Models

- **Decision:** Use Google Generative AI models (Gemini Pro and Embedding-001).
- **Reasoning:** The `langchain-google-genai` package provides a straightforward integration with Google's powerful models. This choice is based on the availability of a free tier and the high quality of the models.
