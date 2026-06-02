from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import app as langgraph_app

app = FastAPI(title="LangGraph QA API")


class QuestionRequest(BaseModel):
    question: str
    thread_id: str | None = None


class QuestionResponse(BaseModel):
    thread_id: str
    answer: str
    route: str
    sql_query: str | None = None


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    try:
        thread_id = request.thread_id or str(uuid4())

        result = langgraph_app.invoke(
            {
                "user_question": request.question
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )

        return {
            "thread_id": thread_id,
            "answer": result["final_response"],
            "route": result["route"],
            "sql_query": result.get("sql_query")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))