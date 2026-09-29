from typing import TypedDict , Optional , List , Dict , Any

class AgentState(TypedDict):
    question:str
    selected_tables:List[str]
    schema_context:str
    sql_query:str
    query_result:Optional[List[Dict[str,Any]]]
    error:Optional[str]
    retry_count:int
    final_answer:str