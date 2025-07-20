# Architectural Decision Record

This document logs the key decisions made during the development of the Doc-Talk application.

## ADR-001: Choice of Web Framework

- **Decision:** Use FastAPI as the web framework.
- **Reasoning:** FastAPI is a modern, high-performance web framework for Python. It's easy to use, has automatic interactive documentation generation (which is great for testing), and is built on modern Python features like type hints.

## ADR-002: Choice of Vector Store

- **Decision:** Use FAISS (Facebook AI Similarity Search) as the vector store.
- **Reasoning:** FAISS is a highly efficient library for similarity search. For this project, we are using the CPU version (`faiss-cpu`), which is simple to set up and runs entirely in memory. This is ideal for a self-contained application that processes documents on the fly without needing a separate database server.

## ADR-003: Choice of LLM and Embedding Models

- **Decision:** Use Google Generative AI models (`gemini-1.5-flash` and `embedding-001`).
- **Reasoning:** The `langchain-google-genai` package provides a straightforward integration with Google's powerful models. We initially tried `gemini-pro` but encountered a `404 Not Found` error, likely due to the user's API key being restricted to a specific API version. Switching to the `gemini-1.5-flash` model resolved this issue.

## ADR-004: Refactor to LCEL

- **Decision:** Refactor the question-answering chain from the deprecated `load_qa_chain` to the modern LangChain Expression Language (LCEL) using `create_retrieval_chain`.
- **Reasoning:** The application was consistently failing with a `404 Not Found` error when calling the Google AI API. The traceback included deprecation warnings for `load_qa_chain` and `.run()`. Refactoring to the modern LCEL standard is the correct, future-proof way to build chains and it resolved the underlying API call issue.

## ADR-005: Choice of Web Search Tool

- **Decision:** Use the Tavily Search API as the web search tool for the agent.
- **Reasoning:** Tavily is a search engine designed specifically for LLM agents. It returns clean, summarized results that are optimized for RAG, which saves us the complexity of building a separate web scraping and data cleaning layer. It has a generous free tier and is well-integrated with LangChain.
