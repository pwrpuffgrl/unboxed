# services/chunking.py

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
    
    # Split the text into sentences or paragraphs (you can adjust the logic)
    sentences = text.split(". ")  # Split by period and space (you can customize this)
    
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
