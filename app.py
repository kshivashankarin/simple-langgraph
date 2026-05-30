from graph import app

while True:

   user_msg = input(
       "\nUser Message : "
   )

   if user_msg.lower() == "exit":
       break

   result = app.invoke(
       {
           "user_question": user_msg
       }
   )

   print(
       "\nAI Response:\n"
   )

   print(
       result["final_response"]
   )

   print(
       "\nRoute Used :",
       result["route"]
   )

   print(
       "\nGenerated SQL :",
       result.get("sql_query", "")
   )
