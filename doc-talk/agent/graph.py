from typing import List, TypedDict
from langgraph.graph import StateGraph, END
from .chains import get_document_grader, get_question_rewriter, get_retrieval_grader
from langchain_core.documents import Document

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
        retriever: the retriever object
        generation_chain: the generation chain
        retrieval_grader: the retrieval grader chain
        question_rewriter: the question rewriter chain
    """
    question: str
    generation: str
    documents: List[Document]
    retriever: object
    generation_chain: object
    retrieval_grader: object
    question_rewriter: object

def retrieve(state):
    """
    Retrieve documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]
    retriever = state["retriever"]
    documents = retriever.invoke(question)
    return {"documents": documents}

def generate(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    generation_chain = state["generation_chain"]
    
    # The output of create_stuff_documents_chain is a dictionary with an "answer" key.
    # However, the final output from the LLM is a string.
    # The `invoke` method on the chain seems to be returning the final string directly.
    generation = generation_chain.invoke({"context": documents, "question": question})
    return {"generation": generation}

def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with only filtered relevant documents
    """
    print("---CHECK DOCUMENT RELEVANCE---")
    question = state["question"]
    documents = state["documents"]
    retrieval_grader = state["retrieval_grader"]
    
    score = retrieval_grader.invoke({"question": question, "documents": documents})
    grade = score.binary_score

    if grade == "yes":
        print("---GRADE: DOCUMENTS RELEVANT---")
        return {"documents": documents}
    else:
        print("---GRADE: DOCUMENTS NOT RELEVANT---")
        return {"documents": []}

def decide_to_generate(state):
    """
    Determines whether to generate an answer, or re-generate the question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """
    print("---ASSESS GRADED DOCUMENTS---")
    question = state["question"]
    filtered_documents = state["documents"]

    if not filtered_documents:
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        print("---DECISION: ALL DOCUMENTS ARE NOT RELEVANT, TRANSFORM QUERY---")
        return "transform_query"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: GENERATE---")
        return "generate"

def transform_query(state):
    """
    Transform the query to produce a better question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates question key with a re-phrased question
    """
    print("---TRANSFORM QUERY---")
    question = state["question"]
    question_rewriter = state["question_rewriter"]
    
    better_question = question_rewriter.invoke({"question": question})
    return {"question": better_question.content}

def build_graph():
    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("generate", generate)
    workflow.add_node("transform_query", transform_query)

    # Build graph
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate",
        },
    )
    workflow.add_edge("transform_query", "retrieve")
    workflow.add_edge("generate", END)

    return workflow.compile()
