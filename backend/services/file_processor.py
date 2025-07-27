# services/file_processor.py
import os
import logging
from typing import Optional, Dict, Any
import PyPDF2
import io

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileProcessor:
    """Handles processing of different file types to extract text content"""
    
    def __init__(self):
        self.supported_types = {
            'application/pdf': self._process_pdf,
            'text/plain': self._process_text,
            'text/markdown': self._process_text,
            'text/csv': self._process_csv,
            'application/json': self._process_json,
            # Add more file types as needed
        }
    
    def process_file(self, file_content: bytes, content_type: str, filename: str) -> Dict[str, Any]:
        """
        Process a file and extract its text content
        
        Args:
            file_content: Raw file bytes
            content_type: MIME type of the file
            filename: Original filename
            
        Returns:
            Dict containing extracted text and metadata
        """
        try:
            if content_type not in self.supported_types:
                raise ValueError(f"Unsupported file type: {content_type}")
            
            # Process the file based on its type
            processor = self.supported_types[content_type]
            extracted_text = processor(file_content)
            
            # Calculate basic metadata
            file_size = len(file_content)
            word_count = len(extracted_text.split()) if extracted_text else 0
            
            return {
                'text': extracted_text,
                'file_size': file_size,
                'word_count': word_count,
                'filename': filename,
                'content_type': content_type,
                'status': 'processed'
            }
            
        except Exception as e:
            logger.error(f"Error processing file {filename}: {e}")
            return {
                'text': '',
                'file_size': len(file_content),
                'word_count': 0,
                'filename': filename,
                'content_type': content_type,
                'status': 'error',
                'error': str(e)
            }
    
    def _process_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF files"""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            return ""
    
    def _process_text(self, file_content: bytes) -> str:
        """Extract text from plain text files"""
        try:
            # Try UTF-8 first, then fallback to other encodings
            try:
                return file_content.decode('utf-8')
            except UnicodeDecodeError:
                return file_content.decode('latin-1')
        except Exception as e:
            logger.error(f"Error processing text file: {e}")
            return ""
    
    def _process_csv(self, file_content: bytes) -> str:
        """Extract text from CSV files"""
        try:
            text_content = self._process_text(file_content)
            # For now, return as-is. Could be enhanced to parse CSV structure
            return text_content
        except Exception as e:
            logger.error(f"Error processing CSV: {e}")
            return ""
    
    def _process_json(self, file_content: bytes) -> str:
        """Extract text from JSON files"""
        try:
            import json
            text_content = self._process_text(file_content)
            # Parse JSON and extract meaningful text
            data = json.loads(text_content)
            
            # Convert JSON to readable text (simplified)
            if isinstance(data, dict):
                text_parts = []
                for key, value in data.items():
                    if isinstance(value, str):
                        text_parts.append(f"{key}: {value}")
                    elif isinstance(value, (list, dict)):
                        text_parts.append(f"{key}: {str(value)}")
                return " ".join(text_parts)
            else:
                return str(data)
                
        except Exception as e:
            logger.error(f"Error processing JSON: {e}")
            return self._process_text(file_content)  # Fallback to raw text 