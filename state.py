from typing import TypedDict, List

class GraphState(TypedDict, total=False):
   user_question: str
   standalone_question: str

   route: str

   sql_query: str
   db_response: str
   retrieved_docs: str

   final_prompt: str
   final_response: str

   conversation_history: List[str]
