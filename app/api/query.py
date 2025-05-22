from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.llm.query_engine import retrieve_and_answer

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def ask_question(req: QueryRequest):
    try:
        answer = retrieve_and_answer(req.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
