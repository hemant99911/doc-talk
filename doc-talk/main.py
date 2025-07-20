import os
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from pydantic import BaseModel
from dotenv import load_dotenv
from agent.graph import build_graph
from agent.chains import get_document_grader, get_question_rewriter, get_retrieval_grader, get_generation_chain

load_dotenv()

# Get the API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

# Global variables
vector_store = None
app_graph = None

class Query(BaseModel):
    question: str

@app.on_event("startup")
async def startup_event():
    global app_graph
    app_graph = build_graph()

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
    global vector_store, app_graph
    if vector_store is None:
        return {"error": "Please upload a document first."}
    if app_graph is None:
        return {"error": "Graph not initialized."}

    retriever = vector_store.as_retriever()
    
    # Get the chains
    generation_chain = get_generation_chain(api_key)
    retrieval_grader = get_retrieval_grader(api_key)
    question_rewriter = get_question_rewriter(api_key)

    # Run the graph
    inputs = {
        "question": query.question,
        "retriever": retriever,
        "generation_chain": generation_chain,
        "retrieval_grader": retrieval_grader,
        "question_rewriter": question_rewriter,
        "iterations": 0,
    }
    
    response = app_graph.invoke(inputs)
    
    return {"answer": response["generation"]}
