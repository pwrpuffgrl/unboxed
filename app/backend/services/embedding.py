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



