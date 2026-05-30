from llm import llm


def generate_final_response(state):

   response = llm.invoke(
       state["final_prompt"]
   )

   return {
       "final_response": response.content
   }
