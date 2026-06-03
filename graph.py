from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

from state import GraphState

from agents.question_rewriter import rewrite_question
from agents.decision_maker import decision_maker
from agents.sql_agent import generate_response_from_db
from agents.rag_agent import retrieve_relevant_doc_from_rag
from agents.final_prompt import generate_final_prompt
from agents.final_response import generate_final_response
from agents.history import save_history

conn = sqlite3.connect(
   "checkpoints.sqlite",
   check_same_thread=False
)

checkpointer = SqliteSaver(conn)

graph = StateGraph(GraphState)

# user : what is the salary of John
# ai : salary of john is 734837483
# user : what is his department?


graph.add_node("rewrite_question", rewrite_question) 
graph.add_node("decision_maker", decision_maker)
graph.add_node("sql_agent", generate_response_from_db)
graph.add_node("rag_agent", retrieve_relevant_doc_from_rag)
graph.add_node("generate_final_prompt", generate_final_prompt)
graph.add_node("generate_final_response", generate_final_response)
graph.add_node("save_history", save_history)

graph.add_edge(START, "rewrite_question")
graph.add_edge("rewrite_question", "decision_maker")

graph.add_conditional_edges(
   "decision_maker",
   lambda state: state["route"],
   {
       "SQL": "sql_agent",
       "RAG": "rag_agent"
   }
)

graph.add_edge("sql_agent", "generate_final_prompt")
graph.add_edge("rag_agent", "generate_final_prompt")
graph.add_edge("generate_final_prompt", "generate_final_response")
graph.add_edge("generate_final_response", "save_history")
graph.add_edge("save_history", END)

app = graph.compile(checkpointer=checkpointer)
