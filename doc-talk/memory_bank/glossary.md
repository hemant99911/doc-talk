# Glossary

A dictionary of key terms and concepts used in this project.

### **RAG (Retrieval-Augmented Generation)**

- An AI architecture that enhances the responses of a Large Language Model (LLM) by first retrieving relevant information from a knowledge base. The LLM then uses this retrieved context to generate a more accurate and informed answer.

### **LLM (Large Language Model)**

- A deep learning model trained on vast amounts of text data, capable of understanding and generating human-like text. In our case, we are using Google's Gemini Pro.

### **Embeddings**

- Numerical representations (vectors) of text, concepts, or other data. In this project, text is converted into embeddings so that we can mathematically compare how similar or different two pieces of text are.

### **Vector Store**

- A specialized database designed to store and efficiently search through embeddings. It allows us to quickly find the most relevant text chunks to a user's query by comparing their vector representations. We are using FAISS.

### **Text Chunking**

- The process of breaking down a large document into smaller, more manageable pieces of text. This is necessary because LLMs have a limited context window (the amount of text they can consider at one time).

### **FastAPI**

- A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
