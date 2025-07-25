# services/embedding.py
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text: str) -> list:
    """
    This function takes a text string and returns its embedding using OpenAI's API.
    """
    try:
        # Request the embedding from OpenAI
        response = openai.embeddings.create(
            model="text-embedding-ada-002",  # Use the 'text-embedding-ada-002' model for embeddings
            input=text
        )
        
        return response.data[0].embedding
    except Exception as e:
        print(f"Error while generating embedding: {e}")
        return []  # Return an empty list if there was an error


def sanitize_text(text: str) -> str:
    """
    Clean and sanitize text for database storage and processing.
    """
    # Remove null characters
    text = text.replace('\x00', '').replace('\0', '')
    
    # Normalize whitespace (replace multiple spaces/tabs with single space)
    text = ' '.join(text.split())
    
    # Remove other problematic characters if needed
    # text = text.replace('\r', ' ').replace('\n', ' ')
    
    return text.strip()


def chunk_text(text: str, max_chunk_size: int = 1000) -> list:
    """
    This function takes a large text and splits it into smaller chunks
    that are approximately `max_chunk_size` tokens in length.
    """
    # Sanitize the text first
    text = sanitize_text(text)
    
    # Split the text into sentences or paragraphs
    sentences = text.split(". ")
    
    chunks = []
    current_chunk = ""
    
    # Iterate through sentences and create chunks
    for sentence in sentences:
        # If adding the sentence doesn't exceed the max chunk size, add it to the current chunk
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk += sentence + ". "
        else:
            # Otherwise, finalize the current chunk and start a new one
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    # Add any remaining chunk that might not have been added
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
