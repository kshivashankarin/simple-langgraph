def generate_final_prompt(state):
   question = state["user_question"]
   standalone_question = state.get("standalone_question", question)

   route = state["route"]

   if route == "SQL":
       context = state["db_response"]
   else:
       context = state["retrieved_docs"]

   final_prompt = f"""
Answer the question using only the context.

Original question:
{question}

Resolved standalone question:
{standalone_question}

Context:
{context}

Generate a user-friendly answer.
"""

   print(f"Final prompt : {final_prompt}")

   return {"final_prompt": final_prompt}
