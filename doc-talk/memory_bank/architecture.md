# System Architecture

This document contains the architecture diagrams for the Doc-Talk application.

## Phase 1 Architecture (Simple RAG Chain)

This diagram represents the initial design of the RAG pipeline and the FastAPI server.

```mermaid
graph TD
    %% Define styles
    classDef user fill:#28a745,color:#fff,stroke:#28a745,stroke-width:2px;
    classDef server fill:#007bff,color:#fff,stroke:#007bff,stroke-width:2px;
    classDef pipeline fill:#6f42c1,color:#fff,stroke:#6f42c1,stroke-width:2px;
    classDef external fill:#dc3545,color:#fff,stroke:#dc3545,stroke-width:2px;

    subgraph User
        A[User Browser]:::user
    end

    subgraph FastAPI Server
        B[Endpoint: /uploadfile/]:::server
        C[Endpoint: /ask/]:::server
    end

    subgraph RAG Pipeline
        D[Load Document]:::pipeline
        E[Chunk Text]:::pipeline
        F[Create Embeddings & FAISS Store]:::pipeline
        G[Retrieve Docs & Generate Answer]:::pipeline
    end

    subgraph External Services
        H[Google AI Platform]:::external
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
    %% Define styles
    classDef startEnd fill:#28a745,color:#fff,stroke:#28a745,stroke-width:2px;
    classDef process fill:#007bff,color:#fff,stroke:#007bff,stroke-width:2px;
    classDef decision fill:#ffc107,color:#333,stroke:#ffc107,stroke-width:2px;

    A[Start]:::startEnd --> B(Retrieve Documents):::process;
    B --> C{Grade Documents}:::decision;
    C -- Relevant --> D(Generate Answer):::process;
    C -- Not Relevant --> E(Rewrite Question):::process;
    E --> B;
    D --> F[End]:::startEnd;
```

## Phase 2.2 Architecture (Synthesis Agent with Web Search)

This diagram shows the final agent design, which can synthesize answers from both local documents and a web search tool.

```mermaid
graph TD
    %% Define styles
    classDef startEnd fill:#28a745,color:#fff,stroke:#28a745,stroke-width:2px;
    classDef process fill:#007bff,color:#fff,stroke:#007bff,stroke-width:2px;
    classDef decision fill:#ffc107,color:#333,stroke:#ffc107,stroke-width:2px;
    classDef web fill:#17a2b8,color:#fff,stroke:#17a2b8,stroke-width:2px;

    A[Start]:::startEnd --> B(Retrieve Document):::process;
    B --> C{Grade Document}:::decision;
    C -- Relevant --> D{Web Search Needed?}:::decision;
    C -- Not Relevant --> E(Rewrite Question):::process;
    E --> B;
    D -- Yes --> G(Web Search):::web;
    D -- No --> F(Generate Answer):::process;
    G -- Web Results --> F;
    F --> H[End]:::startEnd;
