# services/db.py
import psycopg2
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_document(content: str, embedding: list[float]):
    try:
        # Connect to the database
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor()

        # Insert the document and its embedding
        cur.execute(
            "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
            (content, embedding)
        )
        conn.commit()
        logger.info("✅ Inserted document successfully")

    except Exception as e:
        logger.error(f"❌ Failed to insert document: {e}")

    finally:
        # Always close connections
        try:
            cur.close()
            conn.close()
        except Exception as close_err:
            logger.warning(f"⚠️ Problem closing connection: {close_err}")
