# Components

This document provides a detailed breakdown of each major component in the Doc-Talk application.

## FastAPI Server (`main.py`)

- **Purpose:** To provide a web interface (API) for interacting with the RAG pipeline.
- **Endpoints:**
    - `@app.get("/")`: A simple health-check endpoint to confirm the server is running.
    - `@app.post("/uploadfile/")`: Handles file uploads. It is responsible for taking the raw file, processing it through the initial stages of the RAG pipeline (loading, chunking, embedding), and storing the resulting vector store in memory.
    - `@app.post("/ask/")`: Handles user questions. It takes a question, uses the in-memory vector store to retrieve relevant documents, and then calls the language model to generate an answer.

## RAG Pipeline

The core logic of the application, orchestrated by LangChain.

- **Document Loaders:**
    - **Purpose:** To read and parse text from different file formats.
    - **Implementations:** `PyPDFLoader`, `Docx2txtLoader`, `TextLoader`.
- **Text Splitter:**
    - **Purpose:** To break large documents into smaller, uniform chunks. This is crucial for the embedding model's context window and for effective retrieval.
    - **Implementation:** `RecursiveCharacterTextSplitter`.
- **Embeddings Model:**
    - **Purpose:** To convert text chunks into numerical vectors (embeddings).
    - **Implementation:** `GoogleGenerativeAIEmbeddings` using the `models/embedding-001` model.
- **Vector Store:**
    - **Purpose:** To store the text chunk embeddings in a way that allows for efficient searching of similar vectors.
    - **Implementation:** `FAISS` (Facebook AI Similarity Search), an in-memory vector database.
- **Retrieval Chain (LCEL):**
    - **Purpose:** To orchestrate the retrieval and generation process using the modern LangChain Expression Language (LCEL).
    - **Implementation:** We use `create_retrieval_chain`, which combines a `retriever` (our FAISS vector store) with a document processing chain (`create_stuff_documents_chain`). This provides a more flexible and powerful way to handle RAG pipelines compared to the deprecated `load_qa_chain`.
