
from langgraph.graph import StateGraph, END
from services.ai_engine.state import AgentState
from services.ai_engine.nodes import (
    select_tables_node,
    generate_sql_node,
    execute_sql_node,
    format_response_node,
    should_retry_router
)

def create_agent_graph():
    builder = StateGraph(AgentState)

    # 1. Add Nodes
    builder.add_node("select_tables", select_tables_node)
    builder.add_node("generate_sql", generate_sql_node)
    builder.add_node("execute_sql", execute_sql_node)
    builder.add_node("format_response", format_response_node)

    # 2. Define Flow
    builder.set_entry_point("select_tables")
    builder.add_edge("select_tables", "generate_sql")
    builder.add_edge("generate_sql", "execute_sql")

    # 3. Add Self-Correction Conditional Edge
    builder.add_conditional_edges(
        "execute_sql",
        should_retry_router,
        {
            "retry": "generate_sql",
            "format": "format_response"
        }
    )
    builder.add_edge("format_response", END)

    return builder.compile()

# Single compiled instance to be imported by FastAPI routes
lms_rag_agent = create_agent_graph()