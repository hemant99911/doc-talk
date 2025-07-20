from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain

# Data model for the grader
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""
    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")

def get_document_grader(api_key: str):
    """
    Gets a chain that grades the relevance of retrieved documents.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0)
    structured_llm_grader = llm.with_structured_output(GradeDocuments)
    
    system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
    If the document contains keywords related to the user question, grade it as relevant. \n
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
        ]
    )
    
    return prompt | structured_llm_grader

def get_retrieval_grader(api_key: str):
    """
    Gets a chain that determines whether the retrieved documents are relevant to the question.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0)
    structured_llm_grader = llm.with_structured_output(GradeDocuments)

    system = """You are a grader assessing relevance of a set of retrieved documents to a user question. \n 
    If the documents contain keywords related to the user question, grade it as relevant. \n
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
    Give a binary score 'yes' or 'no' score to indicate whether the documents are relevant to the question."""
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Retrieved documents: \n\n {documents} \n\n User question: {question}"),
        ]
    )
    
    return prompt | structured_llm_grader


def get_question_rewriter(api_key: str):
    """
    Gets a chain that rephrases a question to be more specific.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0)
    
    system = """You a question re-writer that converts an input question to a better version that is optimized \n 
     for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning."""
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                "Here is the initial question: \n\n {question} \n Formulate an improved question.",
            ),
        ]
    )
    
    return prompt | llm

def get_generation_chain(api_key: str):
    """
    Gets a chain that generates an answer to a question based on the provided context.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.3)
    
    prompt = ChatPromptTemplate.from_template("""
    Answer the following question based only on the provided context.
    Think step by step before providing a detailed answer.
    <context>
    {context}
    </context>
    Question: {question}
    """)
    
    return create_stuff_documents_chain(llm, prompt)
