# test_ai.py
from services.ai_engine.graph import lms_rag_agent

initial_state = {
    "question": "rahul name ke ktni employees hai?",
    "selected_tables": [],
    "schema_context": "",
    "sql_query": "",
    "query_result": None,
    "error": None,
    "retry_count": 0,
    "final_answer": ""
}

print("Running Local Ollama LangGraph Pipeline...")
result = lms_rag_agent.invoke(initial_state)

print("\n--- RESULTS ---")
print("Selected Tables:", result["selected_tables"])
print("Generated SQL:", result["sql_query"])
print("Final Answer:\n", result["final_answer"])