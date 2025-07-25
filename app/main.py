from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import json
from dotenv import load_dotenv

# Import our services
from services.file_processor import FileProcessor
from services.db import DatabaseService
from services.chunk import chunk_text
from services.embedding import get_embedding

# Load environment variables
load_dotenv()

# Initialize services
file_processor = FileProcessor()
db_service = DatabaseService()

# Initialize FastAPI app
app = FastAPI(
    title="Unboxed API",
    description="Unbox your documents. Talk to your knowledge.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    context_limit: Optional[int] = 5

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

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Unboxed API is running"
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Unboxed API",
        "description": "Unbox your documents. Talk to your knowledge.",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "ask": "/ask",
            "ingest": "/ingest",
            "stats": "/stats"
        }
    }

# Q&A endpoint
@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question and get an answer based on ingested documents"""
    try:
        # Get embedding for the question
        question_embedding = get_embedding(request.question)
        if not question_embedding:
            raise HTTPException(status_code=500, detail="Failed to generate question embedding")
        
        # Search for similar chunks
        similar_chunks = db_service.search_similar_chunks(
            question_embedding, 
            limit=request.context_limit
        )
        
        if not similar_chunks:
            return QuestionResponse(
                answer="I don't have enough information to answer this question. Please upload some documents first.",
                sources=[],
                confidence=0.0
            )
        
        # TODO: Implement actual RAG logic here
        # For now, return a simple response with the most relevant chunk
        most_relevant_chunk = similar_chunks[0]
        
        return QuestionResponse(
            answer=f"Based on the document '{most_relevant_chunk['filename']}', here's what I found: {most_relevant_chunk['content'][:200]}...",
            sources=[f"{most_relevant_chunk['filename']} (similarity: {most_relevant_chunk['similarity']:.2f})"],
            confidence=most_relevant_chunk['similarity']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

# Document ingestion endpoint
@app.post("/ingest", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(..., description="Document file to ingest"),
    metadata: Optional[str] = Form(None, description="Optional metadata as JSON string")
):
    """Ingest a document for RAG processing"""
    try:
        # Validate file type
        allowed_types = [
            "application/pdf",
            "text/plain", 
            "text/markdown",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/csv",
            "application/json"
        ]
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file.content_type} not supported. Allowed types: {allowed_types}"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Process the file to extract text
        processed_file = file_processor.process_file(
            file_content, 
            file.content_type, 
            file.filename
        )
        
        if processed_file['status'] == 'error':
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to process file: {processed_file.get('error', 'Unknown error')}"
            )
        
        # Insert file metadata into database
        file_id = db_service.insert_file_metadata(
            filename=processed_file['filename'],
            content_type=processed_file['content_type'],
            file_size=processed_file['file_size'],
            word_count=processed_file['word_count'],
            metadata=metadata
        )
        
        # Chunk the extracted text
        text_chunks = chunk_text(processed_file['text'])
        
        # Process chunks and create embeddings
        processed_chunks = []
        for i, chunk in enumerate(text_chunks):
            if chunk.strip():  # Skip empty chunks
                embedding = get_embedding(chunk)
                if embedding:
                    processed_chunks.append({
                        'content': chunk,
                        'embedding': embedding,
                        'index': i
                    })
        
        # Insert chunks into database
        chunks_inserted = db_service.insert_document_chunks(file_id, processed_chunks)
        
        return IngestResponse(
            message="Document uploaded and processed successfully",
            filename=processed_file['filename'],
            file_size=processed_file['file_size'],
            file_type=processed_file['content_type'],
            status="processed",
            chunks_processed=chunks_inserted,
            word_count=processed_file['word_count']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting document: {str(e)}")

# Stats endpoint
@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get database statistics"""
    try:
        stats = db_service.get_file_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

# API documentation endpoint
@app.get("/docs")
async def get_docs():
    """Get API documentation"""
    return {
        "message": "API documentation available at /docs",
        "swagger_ui": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
