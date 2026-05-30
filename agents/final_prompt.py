def generate_final_prompt(state):

    question = state["user_question"]

    route = state["route"]

    if route == "SQL":

       context = state["db_response"]

    else:

       context = state["retrieved_docs"]

    final_prompt = f"""
    Answer the question only using the context.

    Question:
    {question}

    Context:
    {context}


    Generate a user-friendly answer.
    """

    print(f"Final prompt : {final_prompt}")

    return {"final_prompt": final_prompt}
