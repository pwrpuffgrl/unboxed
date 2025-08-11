import openai
import os
from dotenv import load_dotenv
from constants import FILE_CONSTANTS, MESSAGES

load_dotenv()

# Initialize the client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_rag_answer(prompt: str) -> str:
    """
    Send the RAG prompt to OpenAI's completion API and get back an answer.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=FILE_CONSTANTS["MAX_TOKENS"],  # Limit response length
            temperature=FILE_CONSTANTS["TEMPERATURE"]  # Balance between creativity and accuracy
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error generating RAG answer: {e}")
        return MESSAGES["RAG_ERROR"]


def create_rag_prompt(question: str, context_chunks: list) -> str:
    """
    Create a prompt for the LLM that includes the question and relevant context.
    """
    # Combine all context chunks into one context string
    context = "\n\n".join([chunk['content'] for chunk in context_chunks])
    
    prompt = f"""You are a helpful assistant that answers questions based on the provided context. Use the context below to answer the question. 

IMPORTANT: The context may contain anonymized placeholders in the format [TYPE_hash] (e.g., [NAME_abc123], [PERCENT_def456], [EMAIL_ghi789]). When you see these placeholders, assume that specific, relevant content was provided in the original text. You can reference these placeholders in your answer - they will be automatically converted to the actual values for the user.

If the context contains relevant information, provide a comprehensive answer. Only say "I don't have enough information" if the context truly doesn't contain any relevant information about the question.

Context:
{context}

Question: {question}

Please provide a detailed answer based on the context:"""
    
    return prompt