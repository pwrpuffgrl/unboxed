# Unboxed 🧠📦

_Unbox your documents. Talk to your knowledge._

**Unboxed** is a full-stack AI application that uses **Retrieval-Augmented Generation (RAG)** to turn unstructured documents into a smart, conversational assistant. Built with a modern React frontend and Python FastAPI backend.

Ask questions in natural language, get accurate answers grounded in your actual data – PDFs, Markdown, CSV, JSON, whatever you've got.

---

## 🔍 Key Features

### 🤖 AI-Powered Q&A

- **RAG Pipeline**: Document embedding + semantic search + LLM generation
- **Context-Aware**: Answers based on your actual documents
- **Multi-format Support**: PDF, TXT, MD, CSV, JSON files

### 🎨 Modern UI/UX

- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark Theme**: Modern, professional interface with cyan accents
- **Intuitive Navigation**: Toggleable sidebar on mobile, fixed sidebar on desktop
- **Real-time Chat**: Bottom-docked chat interface with smart send button

### 🏗️ Robust Backend

- **FastAPI**: High-performance Python web framework
- **PostgreSQL + pgvector**: Scalable vector database for embeddings
- **Modular Architecture**: Clean separation of concerns
- **RESTful API**: Easy integration and testing

---

## 🚀 Quick Start

### Prerequisites

- **Backend**: Python 3.8+, PostgreSQL with pgvector extension, OpenAI API key
- **Frontend**: Node.js 18+, npm/yarn

### Installation

1. **Clone the repository:**

```bash
git clone <your-repo>
cd unboxed
```

2. **Backend Setup:**

```bash
# Navigate to backend
cd app/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python setup_database.py

# Create .env file
echo "DATABASE_URL=postgresql://username:password@localhost:5432/unboxed
OPENAI_API_KEY=your_openai_api_key_here" > .env

# Start backend server
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3. **Frontend Setup:**

```bash
# Navigate to frontend
cd app/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

4. **Access the application:**

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🏗️ Architecture

### Frontend (Next.js + TypeScript)

```
app/frontend/
├── src/
│   ├── app/           # Next.js App Router
│   ├── components/    # Reusable UI components
│   └── styles/        # Tailwind CSS
├── public/            # Static assets
└── package.json
```

**Key Components:**

- **Header**: Custom logo with responsive behavior
- **Sidebar**: File management (desktop) / Toggleable menu (mobile)
- **Chat Interface**: Welcome message + Q&A interface
- **Upload Section**: Drag-and-drop file upload

### Backend (FastAPI + PostgreSQL)

```
app/backend/
├── services/          # Business logic
├── models/           # Pydantic models
├── main.py           # FastAPI application
├── config.py         # Configuration
└── constants.py      # Constants
```

**RAG Pipeline:**

1. **Document Ingestion**: Upload → Extract → Chunk → Embed → Store
2. **Question Processing**: Question → Embedding → Similarity Search
3. **Answer Generation**: Context + Question → LLM → Answer

---

## 🎨 UI/UX Features

### Responsive Design

- **Desktop (≥1280px)**: Fixed sidebar with upload section
- **Mobile (<1280px)**: Toggleable sidebar with hamburger menu
- **Breakpoint Strategy**: Clean transition between layouts

### Design System

- **Colors**: Dark grays with cyan/purple/emerald accents
- **Typography**: Clean white text with proper contrast
- **Spacing**: Consistent 24px padding and component gaps
- **Animations**: Smooth transitions for mobile sidebar

### Interactive Elements

- **Upload Interface**: Drag-and-drop with file type validation
- **Chat Input**: Full-width with responsive send button
- **File Management**: Upload section + file list in sidebar
- **Mobile Menu**: Slide-out panel with overlay

---

## 🔧 Development

### Environment Variables

| Variable         | Description                        | Required |
| ---------------- | ---------------------------------- | -------- |
| `DATABASE_URL`   | PostgreSQL connection string       | Yes      |
| `OPENAI_API_KEY` | OpenAI API key                     | Yes      |
| `OPENAI_MODEL`   | LLM model (default: gpt-3.5-turbo) | No       |
| `MAX_CHUNK_SIZE` | Text chunk size (default: 1000)    | No       |

### API Endpoints

- `POST /ingest` - Upload and process documents
- `POST /ask` - Ask questions using RAG
- `GET /health` - Health check
- `GET /stats` - Database statistics
- `GET /docs` - Interactive API documentation

### Testing

**Backend API:**

```bash
# Health check
curl http://localhost:8000/health

# Upload document
curl -X POST http://localhost:8000/ingest \
  -F "file=@document.pdf" \
  -F "metadata={\"source\": \"test\"}"

# Ask question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this about?"}'
```

**Frontend:**

```bash
cd app/frontend
npm run dev
# Open http://localhost:3000 in browser
```

---

## 🚀 Deployment

### Backend Deployment

- **Docker**: Containerized FastAPI application
- **Cloud**: Deploy to AWS, GCP, or Azure
- **Database**: PostgreSQL with pgvector extension

### Frontend Deployment

- **Vercel**: Optimized for Next.js
- **Netlify**: Static site hosting
- **Docker**: Containerized React application

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


---

## 🙏 Acknowledgments

- **OpenAI** for GPT and embedding models
- **FastAPI** for the high-performance backend framework
- **Next.js** for the React framework
- **Tailwind CSS** for the utility-first styling
- **pgvector** for PostgreSQL vector operations
