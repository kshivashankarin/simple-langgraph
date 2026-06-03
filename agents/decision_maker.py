
from llm import llm
from utils.db_utils import get_database_schema

DB_PATH = "db/company.db"


def decision_maker(state):

   question = state.get("standalone_question", state["user_question"])

   schema = get_database_schema(DB_PATH)

   print(f"This is my current schema : {schema}")

   prompt = f"""
You are a query routing agent.

Your job is to decide whether a user's question can be answered using ONLY the data available in the database schema provided below.

Database Schema:
{schema}

Classification Rules:

1. Return SQL if the question can be answered by querying the tables and columns present in the schema.
   This includes:
   - Filtering records
   - Aggregations (COUNT, SUM, AVG, MIN, MAX)
   - Sorting and ranking
   - Grouping
   - Joins using relationships present in the schema
   - Any factual information stored in the database

2. Return RAG if the question requires:
   - Information not represented in the schema
   - External knowledge
   - Company policies or documentation
   - Explanations, reasoning, opinions, recommendations, or analysis beyond stored data
   - Assumptions about fields, tables, or relationships that are not explicitly present in the schema

3. Do NOT assume the existence of any table, column, relationship, or data that is not shown in the schema.

4. If even one piece of required information is missing from the schema, return RAG.

5. If the question can be answered with a SQL query over the provided schema, return SQL.

6. If you are uncertain, return RAG.

Examples:

Schema:
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER
);

Question: How many employees are there?
Output: SQL

Question: List all employee names.
Output: SQL

Question: What is the average salary by department?
Output: SQL

Question: Which employee has the highest salary?
Output: SQL

Question: What is the salary of John?
Output: SQL

Question: Who is John's manager?
Output: RAG

Question: When was Alice hired?
Output: RAG

Question: What are the responsibilities of the HR department?
Output: RAG

Question: What is the company's leave policy?
Output: RAG

Question: Why are salaries different across departments?
Output: RAG

Question: Is Alice underpaid compared to industry standards?
Output: RAG

Output Instructions:
- Return ONLY one word.
- Valid outputs are:
  SQL
  RAG
- Do not explain your decision.
- Do not generate SQL.
- Do not output any additional text.

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
