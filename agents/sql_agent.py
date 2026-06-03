import sqlite3

from llm import llm
from utils.db_utils import get_database_schema

DB_PATH = "db/company.db"


def generate_response_from_db(state):

   question = state.get("standalone_question", state["user_question"])

   schema = get_database_schema(DB_PATH)

   prompt = f"""
You are an expert SQLite developer.

Generate ONLY SQLite query.

Schema:

{schema}

Question:
{question}

Rules:
- Return only SQL
- No markdown
- No explanation
"""

   sql_query = llm.invoke(prompt).content.strip()

   conn = sqlite3.connect(DB_PATH)

   cursor = conn.cursor()

   try:

       cursor.execute(sql_query)

       print(sql_query)

       rows = cursor.fetchall()

       print(rows)

       db_response = str(rows)

   except Exception as e:

       db_response = str(e)

   conn.close()

   print(f"DB response : {db_response}")

   return {
       "sql_query": sql_query,
       "db_response": db_response
   }
