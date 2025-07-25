from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import logging

import uvicorn

# Import our organized modules

from models.api_models import HealthResponse, IngestResponse, QuestionRequest, QuestionResponse, StatsResponse
from config import config
from constants import MESSAGES, DB_CONSTANTS, FILE_CONSTANTS

# Import services
from services.db import DatabaseService
from services.chunk import chunk_text
from services.embedding import get_embedding, sanitize_text
from services.file_processor import FileProcessor
from services.rag import create_rag_prompt, generate_rag_answer



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
            raise HTTPException(status_code=500, detail=MESSAGES["EMBEDDING_ERROR"])
        
        # Search for similar chunks
        similar_chunks = db_service.search_similar_chunks(
            question_embedding, 
            limit=request.context_limit or DB_CONSTANTS["DEFAULT_LIMIT"]
        )
        
        print(f"Found {len(similar_chunks)} similar chunks")
        if similar_chunks:
            print(f"First chunk similarity: {similar_chunks[0]['similarity']}")
            print(f"First chunk content preview: {similar_chunks[0]['content'][:100]}")

        if not similar_chunks:
            return QuestionResponse(
                answer=MESSAGES["NO_DOCUMENTS"],
                sources=[],
                confidence=0.0
            )
        
        rag_prompt = create_rag_prompt(request.question, similar_chunks)
        answer = generate_rag_answer(rag_prompt)
        most_relevant_chunk = similar_chunks[0]
        
        return QuestionResponse(
            answer=answer,
            sources=[f"{chunk['filename']} (similarity: {chunk['similarity']:.2f})" for chunk in similar_chunks],
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
        allowed_types = config.ALLOWED_FILE_TYPES
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=MESSAGES["FILE_TYPE_NOT_SUPPORTED"].format(file_type=file.content_type, allowed_types=allowed_types)
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
                detail=MESSAGES["PROCESSING_ERROR"].format(error=processed_file.get('error', 'Unknown error'))
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
        text_chunks = chunk_text(processed_file['text'], FILE_CONSTANTS["DEFAULT_CHUNK_SIZE"])

        # DEBUG: Add these print statements
        print(f"Original text length: {len(processed_file['text'])}")
        print(f"Number of chunks created: {len(text_chunks)}")
        if text_chunks:
            print(f"First chunk preview: {text_chunks[0][:100]}")
        else:
            print("No chunks created!")

        # Process chunks and create embeddings
        processed_chunks = []
        print(f"Starting to process {len(text_chunks)} chunks...")

        for i, chunk in enumerate(text_chunks):
            print(f"Processing chunk {i+1}/{len(text_chunks)}")
            if chunk.strip():  # Skip empty chunks
                print(f"  Chunk {i+1} has content, generating embedding...")
                embedding = get_embedding(chunk)
                if embedding:
                    print(f"  Chunk {i+1} embedding generated successfully")
                    sanatized_content = sanitize_text(chunk)
                    processed_chunks.append({
                        'content': sanatized_content,
                        'embedding': embedding,
                        'index': i
                    })
                else:
                    print(f"  Chunk {i+1} embedding generation failed!")
            else:
                print(f"  Chunk {i+1} is empty, skipping")

        print(f"Total processed chunks: {len(processed_chunks)}")

        # Insert chunks into database
        chunks_inserted = db_service.insert_document_chunks(file_id, processed_chunks)
        
        return IngestResponse(
            message=MESSAGES["UPLOAD_SUCCESS"],
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
