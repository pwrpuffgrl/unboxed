from fastapi import FastAPI, HTTPException  
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
            "ask": "/ask"
        }
    }

# Q&A endpoint
@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question and get an answer based on ingested documents"""
    try:
        # TODO: Implement RAG logic here
        # This is a placeholder response
        return QuestionResponse(
            answer="This is a placeholder answer. RAG functionality needs to be implemented.",
            sources=["placeholder_source"],
            confidence=0.8
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

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
