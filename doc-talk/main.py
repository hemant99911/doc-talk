import os
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from pydantic import BaseModel
from dotenv import load_dotenv

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
        
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.3)
    
    prompt = ChatPromptTemplate.from_template("""
    Answer the following question based only on the provided context.
    Think step by step before providing a detailed answer.
    <context>
    {context}
    </context>
    Question: {input}
    """)
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    retriever = vector_store.as_retriever()
    
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    response = retrieval_chain.invoke({"input": query.question})
    
    return {"answer": response["answer"]}
