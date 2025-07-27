from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.rag_pipeline import get_rag_answer

app = FastAPI(title="Bank of Maharashtra Loan Product Assistant")

class QueryRequest(BaseModel):
    """
    Pydantic model for parsing user queries to the /ask endpoint.
    """
    question: str

@app.post("/ask")
def ask_query(request: QueryRequest):
    """
    FastAPI endpoint to handle user question POST requests.
    Uses the RAG pipeline to generate and return an answer.

    Args:
        request (QueryRequest): The user query as a JSON payload.

    Returns:
        dict: The answer to the user's question.
    """
    try:
        answer = get_rag_answer(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
