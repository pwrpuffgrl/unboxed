#!/usr/bin/env python3
"""
Database setup script for Unboxed RAG application
This script helps you set up the PostgreSQL database with pgvector extension
"""


"""
connect to DB psql postgresql://postgres:${POSTGRES_PASSWORD}@localhost:5432/unboxed
"""

import os
import psycopg2
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_database_connection():
    """Check if we can connect to the database"""
    try:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ DATABASE_URL environment variable is not set")
            print("Please set it in your .env file:")
            print("DATABASE_URL=postgresql://username:password@localhost:5432/unboxed")
            return False
        
        print("🔗 Testing database connection...")
        conn = psycopg2.connect(database_url)
        conn.close()
        print("✅ Database connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def setup_database_schema():
    """Set up the database schema"""
    try:
        database_url = os.getenv("DATABASE_URL")
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        print("📋 Setting up database schema...")
        
        # Read and execute the schema file
        with open('database_schema.sql', 'r') as f:
            schema_sql = f.read()
        
        # Split by semicolon and execute each statement
        statements = schema_sql.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                cur.execute(statement)
        
        conn.commit()
        print("✅ Database schema created successfully!")
        
        # Test the tables
        cur.execute("SELECT COUNT(*) FROM files")
        file_count = cur.fetchone()[0]
        print(f"📁 Files table: {file_count} records")
        
        cur.execute("SELECT COUNT(*) FROM document_chunks")
        chunk_count = cur.fetchone()[0]
        print(f"📄 Document chunks table: {chunk_count} records")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Failed to set up database schema: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Unboxed Database Setup")
    print("=" * 40)
    
    # Check connection
    if not check_database_connection():
        print("\n💡 To fix this, you need to:")
        print("1. Install PostgreSQL")
        print("2. Install pgvector extension")
        print("3. Create a database")
        print("4. Set DATABASE_URL in your .env file")
        print("\nExample DATABASE_URL:")
        print("DATABASE_URL=postgresql://username:password@localhost:5432/unboxed")
        sys.exit(1)
    
    # Set up schema
    if not setup_database_schema():
        sys.exit(1)
    
    print("\n🎉 Database setup complete!")
    print("You can now start your FastAPI server and upload documents!")

if __name__ == "__main__":
    main() 