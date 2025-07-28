# Doc-Talk: An AI Agent for Software Impact Analysis

Doc-Talk is a sophisticated chatbot application designed to help software developers and product managers understand the impact of new features on existing systems.

As a developer, I often use tools like Google Notebook LM, but I needed something more specialized. The core challenge is this: when a new Product Requirements Document (PRD) comes in, how do we quickly and accurately identify which parts of our existing codebase and system architecture will be affected?

Doc-Talk is an experiment to solve this problem. You can upload your existing architecture documents, source code, and new PRDs, and then ask critical questions like:
- "Based on this new PRD, which microservices will need to be modified?"
- "What are the potential database schema changes required for this feature?"
- "Which API endpoints will be impacted by these new requirements?"

This project is built with Python, FastAPI, LangChain, and LangGraph, and features a self-correcting agent that can reason about the relevance of retrieved information to provide accurate impact analysis.

## Features

-   **Document Q&A:** Upload `.pdf`, `.docx`, or `.txt` files and ask questions about their content.
-   **Web Search:** The agent can autonomously decide to search the web using the Tavily API if the uploaded document doesn't contain the answer.
-   **Self-Correcting Agent:** Built with LangGraph, the agent can grade the relevance of retrieved documents and rewrite the user's question to improve search results, preventing loops and providing more accurate answers.
-   **Simple Web Interface:** A clean, easy-to-use UI for uploading files and interacting with the chatbot.

## Project Architecture

The application is built around a LangGraph agent that follows a cyclical reasoning process. You can find detailed architecture diagrams and decision logs in the `memory_bank` directory.

### Architectural Considerations

**In-Memory vs. Persistent Vector Database**

This project currently uses `FAISS`, an in-memory vector store. This has several advantages for rapid development and single-user applications:
- **Speed:** Being in-memory, it's extremely fast.
- **Simplicity:** It requires no separate database server or setup.

The primary limitation is that the size of your documents is constrained by your machine's available RAM. For this application's purpose (analyzing a single project's scope), this is often sufficient.

We would need to migrate to a persistent vector database (like Chroma, Weaviate, or Pinecone) under the following circumstances:
- **Persistence:** If we wanted the knowledge base to persist between server restarts without needing to re-upload documents.
- **Scalability:** If the total size of the architecture documents and codebase exceeds available RAM.
- **Multi-User Support:** If we needed to support multiple users querying the same knowledge base concurrently.

## Getting Started

### Prerequisites

-   Python 3.9+
-   An active Google AI API Key
-   An active Tavily Search API Key

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hemant99911/doc-talk.git
    cd doc-talk
    ```

2.  **Create a `.env` file:**
    Create a file named `.env` in the `doc-talk` directory and add your API keys:
    ```
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    TAVILY_API_KEY="YOUR_TAVILY_API_KEY"
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To run the web server, use the following command from within the `doc-talk` directory:

```bash
uvicorn main:app --reload --port 8001
```

Then, open your web browser and navigate to `http://127.0.0.1:8001` to use the application.
