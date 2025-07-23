import asyncio
import time
from main import process_document, api_key
from agent.graph import build_graph
from agent.chains import get_generation_chain, get_retrieval_grader, get_question_rewriter

async def main():
    # 1. Process the test document
    print("--- PROCESSING TEST DOCUMENT ---")
    test_file_path = "doc-talk/test_document.txt"
    vector_store = process_document(test_file_path, "test_document.txt")
    print("--- DOCUMENT PROCESSING COMPLETE ---")

    # 2. Define test questions
    test_questions = [
        {
            "question": "What is the average temperature on Mars?",
            "should_be_in_doc": True
        },
        {
            "question": "Who was Gustave Eiffel?",
            "should_be_in_doc": True
        },
        {
            "question": "What is the capital of Japan?",
            "should_be_in_doc": False
        },
        {
            "question": "Tell me about the red planet.",
            "should_be_in_doc": True # This will test the rewriter
        }
    ]

    # 3. Run evaluation
    print("\n--- STARTING EVALUATION ---")
    total_response_time = 0
    correct_answers = 0

    # Initialize the graph and chains
    graph = build_graph()
    retriever = vector_store.as_retriever()
    generation_chain = get_generation_chain(api_key)
    retrieval_grader = get_retrieval_grader(api_key)
    question_rewriter = get_question_rewriter(api_key)

    for i, test in enumerate(test_questions):
        print(f"\n--- TEST {i+1}: '{test['question']}' ---")
        
        start_time = time.time()

        inputs = {
            "question": test["question"],
            "retriever": retriever,
            "generation_chain": generation_chain,
            "retrieval_grader": retrieval_grader,
            "question_rewriter": question_rewriter,
            "iterations": 0,
        }
        
        response = graph.invoke(inputs)
        answer = response.get("generation", "No answer generated.")

        end_time = time.time()
        response_time = end_time - start_time
        total_response_time += response_time

        print(f"Answer: {answer}")
        print(f"Response Time: {response_time:.2f} seconds")

        # Manual scoring for accuracy (placeholder)
        # In a real scenario, you might compare against a ground truth answer
        user_score = input("Was this answer correct? (y/n): ")
        if user_score.lower() == 'y':
            correct_answers += 1

    # 4. Print results
    print("\n--- EVALUATION COMPLETE ---")
    average_response_time = total_response_time / len(test_questions)
    accuracy = (correct_answers / len(test_questions)) * 100
    print(f"Average Response Time: {average_response_time:.2f} seconds")
    print(f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    # This is needed to run the async main function
    # In a real application, you might use a library like `typer` for a CLI
    # For this script, we can just run the asyncio event loop
    asyncio.run(main())
