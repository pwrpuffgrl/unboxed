import openai
import os
from dotenv import load_dotenv

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
            max_tokens=500,  # Limit response length
            temperature=0.7  # Balance between creativity and accuracy
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error generating RAG answer: {e}")
        return "Sorry, I encountered an error while generating the answer."


def create_rag_prompt(question: str, context_chunks: list) -> str:
    """
    Create a prompt for the LLM that includes the question and relevant context.
    """
    # Combine all context chunks into one context string
    context = "\n\n".join([chunk['content'] for chunk in context_chunks])
    
    prompt = f"""Based on the following context, please answer the question. If the answer cannot be found in the context, say "I don't have enough information to answer this question."

Context:
{context}

Question: {question}

Answer:"""
    
    return prompt