# API Response Messages
MESSAGES = {
    "NO_DOCUMENTS": "I don't have enough information to answer this question. Please upload some documents first.",
    "UPLOAD_SUCCESS": "Document uploaded and processed successfully",
    "FILE_TYPE_NOT_SUPPORTED": "File type {file_type} not supported. Allowed types: {allowed_types}",
    "PROCESSING_ERROR": "Failed to process file: {error}",
    "EMBEDDING_ERROR": "Failed to generate embedding",
    "RAG_ERROR": "Sorry, I encountered an error while generating the answer."
}

# Database
DB_CONSTANTS = {
    "DEFAULT_LIMIT": 5,
    "EMBEDDING_DIMENSION": 1536,  # OpenAI ada-002 dimension
}

# File Processing
FILE_CONSTANTS = {
    "DEFAULT_CHUNK_SIZE": 1000,
    "MAX_TOKENS": 500,
    "TEMPERATURE": 0.7,
}
