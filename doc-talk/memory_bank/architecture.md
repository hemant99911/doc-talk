# System Architecture

This document contains the architecture diagrams for the Doc-Talk application.

## Current Architecture

This diagram represents the initial design of the RAG pipeline and the FastAPI server.

```mermaid
graph TD
    subgraph User
        A[User Browser]
    end

    subgraph FastAPI Server
        B[Endpoint: /uploadfile/]
        C[Endpoint: /ask/]
    end

    subgraph RAG Pipeline
        D[Load Document]
        E[Chunk Text]
        F[Create Embeddings & FAISS Store]
        G[Retrieve Docs & Generate Answer]
    end

    subgraph External Services
        H[Google AI Platform]
    end

    A -- Uploads file --> B
    B --> D
    D --> E
    E --> F
    F -- Stores in-memory --> B

    A -- Asks question --> C
    C --> G
    G -- Uses FAISS Store --> F
    G -- Sends request to --> H
    H -- Returns answer to --> G
    G -- Returns response to --> C
    C -- Sends answer to --> A

```
