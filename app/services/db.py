# services/db.py
import psycopg2
import psycopg2.extras
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.connection_string = os.getenv("DATABASE_URL")
        if not self.connection_string:
            raise ValueError("DATABASE_URL environment variable is required")
    
    def get_connection(self):
        """Get a database connection"""
        return psycopg2.connect(self.connection_string)
    
    def insert_file_metadata(self, filename: str, content_type: str, file_size: int, 
                           word_count: int, metadata: Optional[str] = None) -> int:
        """
        Insert file metadata and return the file ID
        
        Returns:
            int: The file ID that was inserted
        """
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO files (filename, content_type, file_size, word_count, metadata, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (filename, content_type, file_size, word_count, metadata, datetime.utcnow()))
            
            file_id = cur.fetchone()[0]
            conn.commit()
            logger.info(f"✅ Inserted file metadata for {filename} with ID {file_id}")
            return file_id
            
        except Exception as e:
            logger.error(f"❌ Failed to insert file metadata: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    def insert_document_chunks(self, file_id: int, chunks: List[Dict[str, Any]]) -> int:
        """
        Insert document chunks with their embeddings
        
        Args:
            file_id: The ID of the file these chunks belong to
            chunks: List of dicts with 'content' and 'embedding' keys
            
        Returns:
            int: Number of chunks inserted
        """
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            inserted_count = 0
            for chunk in chunks:
                cur.execute("""
                    INSERT INTO document_chunks (file_id, content, embedding, chunk_index, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    file_id,
                    chunk['content'],
                    chunk['embedding'],
                    chunk.get('index', 0),
                    datetime.utcnow()
                ))
                inserted_count += 1
            
            conn.commit()
            logger.info(f"✅ Inserted {inserted_count} chunks for file ID {file_id}")
            return inserted_count
            
        except Exception as e:
            logger.error(f"❌ Failed to insert document chunks: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    def search_similar_chunks(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar document chunks using vector similarity
        
        Args:
            query_embedding: The embedding vector of the query
            limit: Maximum number of results to return
            
        Returns:
            List of dicts with chunk information
        """
        try:
            conn = self.get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cur.execute("""
                SELECT 
                    dc.id,
                    dc.content,
                    dc.chunk_index,
                    f.filename,
                    f.content_type,
                    1 - (dc.embedding <=> %s) as similarity
                FROM document_chunks dc
                JOIN files f ON dc.file_id = f.id
                ORDER BY dc.embedding <=> %s
                LIMIT %s
            """, (query_embedding, query_embedding, limit))
            
            results = cur.fetchall()
            return [dict(row) for row in results]
            
        except Exception as e:
            logger.error(f"❌ Failed to search similar chunks: {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    def get_file_stats(self) -> Dict[str, Any]:
        """Get basic statistics about the database"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Get file count
            cur.execute("SELECT COUNT(*) FROM files")
            file_count = cur.fetchone()[0]
            
            # Get chunk count
            cur.execute("SELECT COUNT(*) FROM document_chunks")
            chunk_count = cur.fetchone()[0]
            
            # Get total word count
            cur.execute("SELECT COALESCE(SUM(word_count), 0) FROM files")
            total_words = cur.fetchone()[0]
            
            return {
                'file_count': file_count,
                'chunk_count': chunk_count,
                'total_words': total_words
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get file stats: {e}")
            return {'file_count': 0, 'chunk_count': 0, 'total_words': 0}
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

# Legacy function for backward compatibility
def insert_document(content: str, embedding: list[float]):
    """Legacy function - use DatabaseService.insert_document_chunks instead"""
    logger.warning("⚠️ Using legacy insert_document function. Consider using DatabaseService instead.")
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
            (content, embedding)
        )
        conn.commit()
        logger.info("✅ Inserted document successfully")

    except Exception as e:
        logger.error(f"❌ Failed to insert document: {e}")

    finally:
        try:
            cur.close()
            conn.close()
        except Exception as close_err:
            logger.warning(f"⚠️ Problem closing connection: {close_err}")
