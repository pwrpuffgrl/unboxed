from pydantic import BaseModel
from typing import List, Optional

class QuestionRequest(BaseModel):
    question: str
    context_limit: int = 5

class QuestionResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float
    anonymized_answer: Optional[str] = None  # Debug: original AI response before deanonymization


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
    anonymized: bool = False
    anonymization_summary: Optional[dict] = None

class FileInfo(BaseModel):
    id: int
    filename: str
    content_type: str
    file_size: int
    word_count: int
    anonymized: bool = False
    created_at: str

class StatsResponse(BaseModel):
    file_count: int
    chunk_count: int
    total_words: int

class FilesResponse(BaseModel):
    files: List[FileInfo]