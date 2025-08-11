# services/db.py
import psycopg2
import os
import logging
import json
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
                           word_count: int, original_file_bytes: Optional[bytes] = None, 
                           anonymized: bool = False, anonymization_mapping: Optional[Dict] = None,
                           metadata: Optional[str] = None) -> int:
        """
        Insert file metadata and original file content, return the file ID
        
        Args:
            filename: Name of the file
            content_type: MIME type of the file
            file_size: Size of the file in bytes
            word_count: Number of words in the extracted text
            original_file_bytes: Original file content as bytes (optional)
            anonymized: Whether the file was anonymized
            anonymization_mapping: Mapping of original values to aliases
            metadata: Additional metadata as JSON string (optional)
            
        Returns:
            int: The file ID that was inserted
        """
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Convert anonymization_mapping to JSON string if it exists
            anonymization_mapping_json = json.dumps(anonymization_mapping) if anonymization_mapping else None
            
            cur.execute("""
                INSERT INTO files (filename, content_type, file_size, word_count, original_file, 
                                 anonymized, anonymization_mapping, metadata, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (filename, content_type, file_size, word_count, original_file_bytes, 
                  anonymized, anonymization_mapping_json, metadata, datetime.utcnow()))
            
            file_id = cur.fetchone()[0]
            conn.commit()
            logger.info(f"✅ Inserted file metadata and content for {filename} with ID {file_id}")
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
        conn = None
        cur = None
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
        """Search for similar chunks using vector similarity"""
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Convert the embedding list to a proper format for pgvector
            embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
            logger.info(f"🔍 Searching with embedding length: {len(query_embedding)}")
            logger.info(f"🔍 Embedding string preview: {embedding_str[:100]}...")
            
            cur.execute("""
                SELECT dc.content, dc.chunk_index, f.filename, f.anonymized,
                       (dc.embedding <=> %s::vector) as similarity
                FROM document_chunks dc
                JOIN files f ON dc.file_id = f.id
                WHERE dc.embedding IS NOT NULL
                ORDER BY similarity ASC
                LIMIT %s
            """, (embedding_str, limit))
            
            logger.info(f"🔍 Query executed, checking results...")
            
            results = []
            for row in cur.fetchall():
                results.append({
                    'content': row[0],
                    'chunk_index': row[1],
                    'filename': row[2],
                    'anonymized': row[3],
                    'similarity': float(row[4])
                })
            
            return results
            
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
        conn = None
        cur = None
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

    def get_all_files(self) -> List[Dict[str, Any]]:
        """Get all files with their metadata"""
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT id, filename, content_type, file_size, word_count, 
                       anonymized, created_at
                FROM files
                ORDER BY created_at DESC
            """)
            
            files = []
            for row in cur.fetchall():
                files.append({
                    'id': row[0],
                    'filename': row[1],
                    'content_type': row[2],
                    'file_size': row[3],
                    'word_count': row[4],
                    'anonymized': row[5],
                    'created_at': row[6].isoformat() if row[6] else None
                })
            
            return files
            
        except Exception as e:
            logger.error(f"❌ Failed to get all files: {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def get_file_content(self, file_id: int) -> Optional[str]:
        """Get the full content of a file by combining all its chunks"""
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # Get all chunks for the file, ordered by chunk_index
            cur.execute("""
                SELECT content 
                FROM document_chunks 
                WHERE file_id = %s 
                ORDER BY chunk_index
            """, (file_id,))
            
            chunks = cur.fetchall()
            if not chunks:
                return None
            
            # Combine all chunks into full content
            full_content = '\n'.join([chunk[0] for chunk in chunks])
            return full_content
            
        except Exception as e:
            logger.error(f"❌ Failed to get file content: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def get_file_info(self, file_id: int) -> Optional[Dict[str, Any]]:
        """Get file metadata by ID"""
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT id, filename, content_type, file_size, word_count, 
                       anonymized, anonymization_mapping, created_at
                FROM files
                WHERE id = %s
            """, (file_id,))
            
            row = cur.fetchone()
            if not row:
                return None
            
            return {
                'id': row[0],
                'filename': row[1],
                'content_type': row[2],
                'file_size': row[3],
                'word_count': row[4],
                'anonymized': row[5],
                'anonymization_mapping': row[6],
                'created_at': row[7].isoformat() if row[7] else None
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get file info: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def get_original_file(self, file_id: int) -> Optional[bytes]:
        """Get the original file content as bytes"""
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT original_file
                FROM files
                WHERE id = %s
            """, (file_id,))
            
            row = cur.fetchone()
            if not row or not row[0]:
                return None
            
            return row[0]
            
        except Exception as e:
            logger.error(f"❌ Failed to get original file: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def delete_file(self, file_id: int) -> bool:
        """Delete a file and all its associated chunks"""
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            # First, check if the file exists
            cur.execute("SELECT id FROM files WHERE id = %s", (file_id,))
            if not cur.fetchone():
                return False
            
            # Delete all chunks associated with this file
            cur.execute("DELETE FROM document_chunks WHERE file_id = %s", (file_id,))
            chunks_deleted = cur.rowcount
            
            # Delete the file itself
            cur.execute("DELETE FROM files WHERE id = %s", (file_id,))
            file_deleted = cur.rowcount
            
            conn.commit()
            
            logger.info(f"✅ Deleted file ID {file_id} and {chunks_deleted} associated chunks")
            return file_deleted > 0
            
        except Exception as e:
            logger.error(f"❌ Failed to delete file: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def get_all_anonymization_mappings(self) -> Dict[str, str]:
        """Get all anonymization mappings from all files"""
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT anonymization_mapping
                FROM files
                WHERE anonymized = true AND anonymization_mapping IS NOT NULL
            """)
            
            all_mappings = {}
            for row in cur.fetchall():
                if row[0]:  # anonymization_mapping is not None
                    mappings = row[0]
                    if isinstance(mappings, str):
                        import json
                        mappings = json.loads(mappings)
                    all_mappings.update(mappings)
            
            logger.info(f"📊 Retrieved {len(all_mappings)} anonymization mappings from database")
            return all_mappings
            
        except Exception as e:
            logger.error(f"❌ Failed to get anonymization mappings: {e}")
            return {}
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
