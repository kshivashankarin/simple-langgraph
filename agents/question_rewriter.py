from llm import llm

def rewrite_question(state):
   question = state["user_question"]
   history = state.get("conversation_history", [])

   history_text = "\n".join(history[-6:])

   prompt = f"""
You rewrite follow-up questions into standalone questions.

Conversation history:
{history_text}

Latest question:
{question}

Return only the standalone question.
"""

   standalone_question = llm.invoke(prompt).content.strip()

   return {
       "standalone_question": standalone_question
   }




