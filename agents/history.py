def save_history(state):
   history = state.get("conversation_history", [])

   history.append(f"User: {state['user_question']}")
   history.append(f"Assistant: {state['final_response']}")

   return {
       "conversation_history": history
   }
