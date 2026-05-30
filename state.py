from typing import TypedDict

class GraphState(TypedDict):

    user_question: str

    route: str

    sql_query: str
    db_response: str

    retrieved_docs: str

    final_prompt: str
    final_response: str
