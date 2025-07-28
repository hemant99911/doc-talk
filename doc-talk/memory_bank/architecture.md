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

## Phase 3 Architecture (Multi-Agent Orchestrator)

This diagram shows the high-level architecture for a multi-agent system, where a central orchestrator delegates tasks to specialized agents.

```mermaid
graph TD
    %% Define styles
    classDef user fill:#28a745,color:#fff,stroke:#28a745,stroke-width:2px;
    classDef orchestrator fill:#6f42c1,color:#fff,stroke:#6f42c1,stroke-width:2px;
    classDef agent fill:#007bff,color:#fff,stroke:#007bff,stroke-width:2px;
    classDef answer fill:#20c997,color:#fff,stroke:#20c997,stroke-width:2px;

    A[User Request]:::user --> B{Orchestrator Agent}:::orchestrator;
    B --"Impact Analysis?"--> C[Code & PRD Agent]:::agent;
    B --"Create Story?"--> D[Jira Agent]:::agent;
    B --"Prod Issue?"--> E[Log & Ticket Agent]:::agent;
    C --> F[Answer]:::answer;
    D --> F;
    E --> F;
```

## Phase 4 Architecture (Proactive, Event-Driven Agent)

This diagram shows the final agent design, which is triggered by external events and can proactively assist the development team.

```mermaid
graph TD
    %% Define styles
    classDef event fill:#dc3545,color:#fff,stroke:#dc3545,stroke-width:2px;
    classDef listener fill:#fd7e14,color:#fff,stroke:#fd7e14,stroke-width:2px;
    classDef orchestrator fill:#6f42c1,color:#fff,stroke:#6f42c1,stroke-width:2px;
    classDef agent fill:#007bff,color:#fff,stroke:#007bff,stroke-width:2px;

    subgraph External_Systems
        A[GitHub Event: New PR]:::event
        B[Jira Event: New Ticket]:::event
    end

    subgraph Doc_Talk_System
        C[Webhook Listener]:::listener
        D{Orchestrator Agent}:::orchestrator
        E[Code & PRD Agent]:::agent
        F[Jira Agent]:::agent
        G[Log & Ticket Agent]:::agent
    end

    A --> C
    B --> C
    C -- Triggers --> D
    D --> E
    D --> F
    D --> G
