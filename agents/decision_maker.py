
from llm import llm
from utils.db_utils import get_database_schema

DB_PATH = "db/company.db"


def decision_maker(state):

   question = state["user_question"]

   schema = get_database_schema(DB_PATH)

   print(f"This is my current schema : {schema}")

   prompt = f"""
You are a routing agent.

Database Schema:

{schema}

Task:

If the user question can be answered
using database tables above,
return only:

SQL

Otherwise return:

RAG

Question:
{question}
"""

   response = llm.invoke(prompt)

   route = response.content.strip().upper()

   if "SQL" in route:
       route = "SQL"
   else:
       route = "RAG"

   return {
       "route": route
   }
