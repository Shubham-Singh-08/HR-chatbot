from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    question: str

class RetrievedDoc(BaseModel):
    filename: str
    score: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    retrieved_documents: List[RetrievedDoc]
