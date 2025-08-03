# Unboxed 🧠📦

_Unbox your documents. Talk to your knowledge._

**Unboxed** is an open-source AI app that uses **Retrieval-Augmented Generation (RAG)** to turn unstructured documents into a smart, conversational assistant.

Ask questions in natural language, get accurate answers grounded in your actual data – PDFs, Markdown, Confluence pages, whatever you've got.

---

## 🔍 Key Features

- ⚙️ Embedding-based document search (OpenAI or open-source models)
- 🧠 Context-aware Q&A with GPT (RAG-style prompts)
- 📦 Vector store with PostgreSQL + `pgvector`
- 🧩 Modular Python backend (FastAPI)
- 🌐 Optional UI or API-first usage
- 🧪 Prompt evaluation (Langfuse/promptfoo ready)
- 🔒 **Privacy Protection**: Advanced spaCy-based anonymization system
- 🛡️ **Two-Way Anonymization**: Questions and answers are anonymized/deanonymized
- 📋 **File-Specific Privacy**: Choose privacy mode per document during upload
- 🔍 **Debug Mode**: Toggle to see anonymized AI responses for transparency

---

## 📂 Use cases

- Internal knowledge base search
- Developer docs Q&A
- AI-powered help desk
- Custom ChatGPT for your company

---

> Built for devs who want **control over their LLM stack** – no black boxes, no vendor lock-in.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL with pgvector extension
- OpenAI API key
- spaCy with English language model

### Installation

1. **Clone and setup:**

```bash
git clone <your-repo>
cd unboxed
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install spaCy and language model
python -m spacy download en_core_web_sm
```

2. **Database setup:**

```bash
# Create PostgreSQL database with pgvector
# Run the schema setup
python setup_database.py
```

3. **Environment variables:**

```bash
# Create .env file
DATABASE_URL=postgresql://username:password@localhost:5432/unboxed
OPENAI_API_KEY=your_openai_api_key_here
```

4. **Start the server:**

```bash
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### API Usage

**Upload a document with privacy mode:**

```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@your_document.pdf" \
  -F "anonymize=true" \
  -F "metadata={\"source\": \"manual\"}"
```

**Ask a question (automatically anonymized):**

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What did John work on?"}'
```

## �� API Reference

### Endpoints

- `POST /ingest` - Upload and process documents (with privacy mode)
- `POST /ask` - Ask questions using RAG (with anonymization)
- `GET /files` - List all uploaded files
- `DELETE /files/{id}` - Delete file and associated data
- `GET /files/{id}/download` - Download original file
- `GET /health` - Health check
- `GET /stats` - Database statistics
- `GET /docs` - Interactive API documentation

### Supported File Types

- PDF, TXT, Markdown, DOC, DOCX, CSV, JSON

## ��️ Architecture

**RAG Pipeline with Privacy:**

1. **Document Ingestion** - Upload → Extract → Chunk → Embed → Store
2. **Privacy Processing** - Anonymize sensitive data → Store mappings
3. **Question Processing** - Question → Anonymize → Embedding → Similarity Search
4. **Answer Generation** - Context + Question → LLM → Deanonymize → Answer

**Tech Stack:**

- **Backend:** FastAPI + PostgreSQL + pgvector
- **AI:** OpenAI GPT-3.5 + text-embedding-ada-002
- **Privacy:** spaCy NER + consistent anonymization
- **File Processing:** PyPDF2, text extraction
- **Vector Search:** pgvector with cosine similarity

## 🔧 Development

### Project Structure

unboxed/
├── app/
│ ├── models/ # Pydantic models
│ ├── services/ # Business logic
│ ├── config.py # Configuration
│ ├── constants.py # Constants
│ └── main.py # FastAPI app
├── database_schema.sql # Database schema
├── setup_database.py # Database setup
└── requirements.txt # Dependencies

### Environment Variables

| Variable         | Description                        | Required |
| ---------------- | ---------------------------------- | -------- |
| `DATABASE_URL`   | PostgreSQL connection string       | Yes      |
| `OPENAI_API_KEY` | OpenAI API key                     | Yes      |
| `OPENAI_MODEL`   | LLM model (default: gpt-3.5-turbo) | No       |
| `MAX_CHUNK_SIZE` | Text chunk size (default: 1000)    | No       |

## 🧪 Testing

**Test the API:**

```bash
# Health check
curl http://localhost:8000/health

# Upload test file with privacy mode
curl -X POST http://localhost:8000/ingest \
  -F "file=@test.txt" \
  -F "anonymize=true" \
  -F "metadata={\"test\": true}"

# Ask question (automatically anonymized)
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What did John work on?"}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License
