# System Architecture

This document contains the architecture diagrams for the Doc-Talk application.

## Phase 1 Architecture (Simple RAG Chain)

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

## Phase 2 Architecture (LangGraph Agent)

This diagram illustrates the cyclical, self-correcting agent architecture using LangGraph.

```mermaid
graph TD
    A[Start] --> B(Retrieve Documents);
    B --> C{Grade Documents};
    C -- Relevant --> D(Generate Answer);
    C -- Not Relevant --> E(Rewrite Question);
    E --> B;
    D --> F[End];
```

## Phase 2.2 Architecture (Synthesis Agent with Web Search)

This diagram shows the final agent design, which can synthesize answers from both local documents and a web search tool.

```mermaid
graph TD
    A[Start] --> B(Retrieve Document);
    B --> C{Grade Document};
    C -- Relevant --> D{Web Search Needed?};
    C -- Not Relevant --> E(Rewrite Question);
    E --> B;
    D -- Yes --> G(Web Search);
    D -- No --> F(Generate Answer);
    G -- Web Results --> F;
    F --> H[End];
