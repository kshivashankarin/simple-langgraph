from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import app as langgraph_app

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    tread_id: int
    
class QuestionResponse(BaseModel):
    answer: str
    route: str




@app.post(
        "/chat", 
        response_model=QuestionResponse
        )
def chat(request: QuestionRequest):
    result = langgraph_app.invoke(
        {
            "user_question" : request.question
        }
    )

    # return request
    return {
        "answer" : result['final_response'], 
        "route" : result['route']
        }

