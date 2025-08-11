from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

import uvicorn

# Import our organized modules

from models.api_models import HealthResponse, IngestResponse, QuestionRequest, QuestionResponse, StatsResponse, FilesResponse
from config import config
from constants import MESSAGES, DB_CONSTANTS, FILE_CONSTANTS

# Import services
from services.db import DatabaseService
from services.chunk import chunk_text, sanitize_text
from services.embedding import get_embedding
from services.file_processor import FileProcessor
from services.rag import create_rag_prompt, generate_rag_answer
from services.spacy_anonymizer import SpacyAnonymizer



# Initialize services
file_processor = FileProcessor()
db_service = DatabaseService()
anonymizer = SpacyAnonymizer()

# Initialize FastAPI app
app = FastAPI(
    title="Unboxed API",
    description="Unbox your documents. Talk to your knowledge.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #TODO: Configure this properly for production
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
        # Get all anonymization mappings from the database
        all_mappings = db_service.get_all_anonymization_mappings()
        
        # Anonymize the question if we have mappings
        original_question = request.question
        anonymized_question = request.question
        if all_mappings:
            anonymized_question = anonymizer.anonymize_question(request.question, all_mappings)
            print(f"🔒 Original question: '{original_question}'")
            print(f"🔒 Anonymized question: '{anonymized_question}'")
        
        # Get embedding for the anonymized question
        question_embedding = get_embedding(anonymized_question)
        if not question_embedding:
            raise HTTPException(status_code=500, detail=MESSAGES["EMBEDDING_ERROR"])
        
        # Search for similar chunks
        print(f"🔍 Searching for chunks with embedding length: {len(question_embedding)}")
        similar_chunks = db_service.search_similar_chunks(
            question_embedding, 
            limit=request.context_limit or DB_CONSTANTS["DEFAULT_LIMIT"]
        )
        
        print(f"Found {len(similar_chunks)} similar chunks")
        if similar_chunks:
            print(f"First chunk similarity: {similar_chunks[0]['similarity']}")
            print(f"First chunk content preview: {similar_chunks[0]['content'][:100]}")
        else:
            print("❌ No similar chunks found - this might indicate an issue with the search")

        if not similar_chunks:
            return QuestionResponse(
                answer=MESSAGES["NO_DOCUMENTS"],
                sources=[],
                confidence=0.0
            )
        
        # Create RAG prompt with anonymized chunks (AI never sees sensitive data)
        rag_prompt = create_rag_prompt(anonymized_question, similar_chunks)
        answer = generate_rag_answer(rag_prompt)
        
        # Store the original AI answer for debug purposes
        anonymized_answer = answer
        
        # Deanonymize the answer to show original values to the user
        if all_mappings:
            original_answer = answer
            print(f"🔓 Original AI answer (before deanonymization): '{original_answer}'")
            answer = anonymizer.deanonymize_answer(answer, all_mappings)
            print(f"🔓 Final answer (after deanonymization): '{answer}'")
        
        most_relevant_chunk = similar_chunks[0]
        
        return QuestionResponse(
            answer=answer,
            sources=[f"{chunk['filename']} (similarity: {chunk['similarity']:.2f})" for chunk in similar_chunks],
            confidence=most_relevant_chunk['similarity'],
            anonymized_answer=anonymized_answer if all_mappings else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

# Document ingestion endpoint
@app.post("/ingest", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(..., description="Document file to ingest"),
    metadata: Optional[str] = Form(None, description="Optional metadata as JSON string"),
    anonymize: bool = Form(False, description="Whether to anonymize sensitive data")
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
        
        # Anonymize text if requested
        extracted_text = processed_file['text']
        anonymization_mapping = None
        anonymization_summary = None
        
        if anonymize:
            print(f"🔒 Starting anonymization process for file: {processed_file['filename']}")
            print(f"🔒 Original text length: {len(processed_file['text'])} characters")
            print(f"🔒 Original text preview: {processed_file['text'][:200]}...")
            
            anonymizer.clear_mappings()  # Clear previous mappings
            extracted_text, anonymization_mapping = anonymizer.anonymize_text(processed_file['text'])
            anonymization_summary = anonymizer.get_mapping_summary()
            
            print(f"🔒 Anonymized {len(anonymization_mapping)} sensitive data points")
            print(f"📊 Anonymization summary: {anonymization_summary}")
            
            # Print detailed anonymization mappings
            if anonymization_mapping:
                print(f"🔒 Detailed anonymization mappings:")
                for original, alias in anonymization_mapping.items():
                    print(f"   '{original}' → '{alias}'")
            
            print(f"🔒 Anonymized text length: {len(extracted_text)} characters")
            print(f"🔒 Anonymized text preview: {extracted_text[:200]}...")
        else:
            print(f"📄 No anonymization requested for file: {processed_file['filename']}")
        
        # Insert file metadata and original file content into database
        file_id = db_service.insert_file_metadata(
            filename=processed_file['filename'],
            content_type=processed_file['content_type'],
            file_size=processed_file['file_size'],
            word_count=processed_file['word_count'],
            original_file_bytes=file_content,  # Store the original file
            anonymized=anonymize,
            anonymization_mapping=anonymization_mapping if anonymization_mapping else None,
            metadata=metadata
        )
        
        # Chunk the extracted text (anonymized if requested)
        text_chunks = chunk_text(extracted_text, FILE_CONSTANTS["DEFAULT_CHUNK_SIZE"])

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
            word_count=processed_file['word_count'],
            anonymized=anonymize,
            anonymization_summary=anonymization_summary
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

# Files endpoint
@app.get("/files", response_model=FilesResponse)
async def get_files():
    """Get all uploaded files"""
    try:
        files = db_service.get_all_files()
        return FilesResponse(files=files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting files: {str(e)}")

# Document content endpoint
@app.get("/files/{file_id}/content")
async def get_file_content(file_id: int):
    """Get the content of a specific file"""
    try:
        content = db_service.get_file_content(file_id)
        if not content:
            raise HTTPException(status_code=404, detail="File not found or no content available")
        return {"content": content}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting file content: {str(e)}")

# Delete file endpoint
@app.delete("/files/{file_id}")
async def delete_file(file_id: int):
    """Delete a file and all its associated data"""
    try:
        # Delete the file and all its chunks
        deleted = db_service.delete_file(file_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="File not found")
        
        return {"message": "File deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

# Original file endpoint
@app.get("/files/{file_id}/download")
async def download_file(file_id: int):
    """Download the original file"""
    try:
        print(f"📥 Download request for file ID: {file_id}")
        
        file_info = db_service.get_file_info(file_id)
        if not file_info:
            print(f"❌ File info not found for ID: {file_id}")
            raise HTTPException(status_code=404, detail="File not found")
        
        print(f"📄 File info: {file_info['filename']} ({file_info['content_type']})")
        
        # Get the original file content
        original_file_bytes = db_service.get_original_file(file_id)
        if not original_file_bytes:
            print(f"❌ Original file bytes not found for ID: {file_id}")
            raise HTTPException(status_code=404, detail="Original file not found")
        
        print(f"✅ File bytes retrieved: {len(original_file_bytes)} bytes")
        
        from fastapi.responses import Response
        return Response(
            content=original_file_bytes,
            media_type=file_info['content_type'],
            headers={
                "Content-Disposition": f"inline; filename={file_info['filename']}",
                "Content-Length": str(len(original_file_bytes))
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error downloading file {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")

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
