from langgraph.graph import (
   StateGraph,
   START,
   END
)


import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

from state import GraphState

from agents.decision_maker import decision_maker
from agents.sql_agent import generate_response_from_db
from agents.rag_agent import retrieve_relevant_doc_from_rag
from agents.final_prompt import generate_final_prompt
from agents.final_response import generate_final_response

graph = StateGraph(GraphState)

graph.add_node(
   "decision_maker",
   decision_maker
)

graph.add_node(
   "sql_agent",
   generate_response_from_db
)

graph.add_node(
   "rag_agent",
   retrieve_relevant_doc_from_rag
)

graph.add_node(
   "generate_final_prompt",
   generate_final_prompt
)

graph.add_node(
   "generate_final_response",
   generate_final_response
)

graph.add_edge(
   START,
   "decision_maker"
)

graph.add_conditional_edges(
   "decision_maker",
   lambda state: state["route"],
   {
       "SQL": "sql_agent",
       "RAG": "rag_agent"
   }
)

graph.add_edge(
   "sql_agent",
   "generate_final_prompt"
)

graph.add_edge(
   "rag_agent",
   "generate_final_prompt"
)

graph.add_edge(
   "generate_final_prompt",
   "generate_final_response"
)

graph.add_edge(
   "generate_final_response",
   END
)


conn = sqlite3.connect(
    "checkpoints.sqlite",
    check_same_thread=False
)

memory = SqliteSaver(conn)

app = graph.compile(
    checkpointer=memory
)