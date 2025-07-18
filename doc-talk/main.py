import os
from fastapi import FastAPI, File, UploadFile
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Get the API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

app = FastAPI()

# Global variable to store the vector store
vector_store = None

class Query(BaseModel):
    question: str

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    global vector_store
    
    # Save the uploaded file temporarily
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
        
    # Load the document based on file type
    if file.filename.endswith(".pdf"):
        loader = PyPDFLoader(file_location)
    elif file.filename.endswith(".docx"):
        loader = Docx2txtLoader(file_location)
    else:
        loader = TextLoader(file_location)
        
    documents = loader.load()
    
    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    
    # Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    
    # Create FAISS vector store
    vector_store = FAISS.from_documents(docs, embeddings)
    
    # Clean up the temporary file
    os.remove(file_location)
    
    return {"info": f"file '{file.filename}' uploaded and processed successfully."}

@app.post("/ask/")
async def ask_question(query: Query):
    global vector_store
    if vector_store is None:
        return {"error": "Please upload a document first."}
        
    # Perform similarity search
    docs = vector_store.similarity_search(query.question)
    
    # Get the answer from the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key, temperature=0.3)
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents=docs, question=query.question)
    
    return {"answer": response}
