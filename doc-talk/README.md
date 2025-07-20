# Doc-Talk: An Intelligent RAG Agent

Doc-Talk is a sophisticated chatbot application that uses a Retrieval-Augmented Generation (RAG) agent to answer questions based on uploaded documents and, if necessary, information from the web.

This project is built with Python, FastAPI, LangChain, and LangGraph, and features a self-correcting agent that can reason about the relevance of retrieved information and rewrite queries to find better answers.

## Features

-   **Document Q&A:** Upload `.pdf`, `.docx`, or `.txt` files and ask questions about their content.
-   **Web Search:** The agent can autonomously decide to search the web using the Tavily API if the uploaded document doesn't contain the answer.
-   **Self-Correcting Agent:** Built with LangGraph, the agent can grade the relevance of retrieved documents and rewrite the user's question to improve search results, preventing loops and providing more accurate answers.
-   **Simple Web Interface:** A clean, easy-to-use UI for uploading files and interacting with the chatbot.

## Project Architecture

The application is built around a LangGraph agent that follows a cyclical reasoning process. You can find detailed architecture diagrams and decision logs in the `memory_bank` directory.

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
