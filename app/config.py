import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
    
    # File Processing
    MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", "1000"))
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    
    # API Settings
    CONTEXT_LIMIT_DEFAULT = int(os.getenv("CONTEXT_LIMIT_DEFAULT", "5"))
    
    # Allowed file types
    ALLOWED_FILE_TYPES = [
        "application/pdf",
        "text/plain", 
        "text/markdown",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/csv",
        "application/json"
    ]

# Global config instance
config = Config()