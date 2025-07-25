from pydantic import BaseModel
from typing import List, Optional

class QuestionRequest(BaseModel):
    question: str
    context_limit: int = 5

class QuestionResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float


class HealthResponse(BaseModel):
    status: str
    message: str


class IngestResponse(BaseModel):
    message: str
    filename: str
    file_size: int
    file_type: str
    status: str
    chunks_processed: int
    word_count: int

class StatsResponse(BaseModel):
    file_count: int
    chunk_count: int
    total_words: int