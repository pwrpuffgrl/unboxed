# Unboxed Frontend

This is the frontend application for Unboxed, a document processing and RAG (Retrieval-Augmented Generation) system.

## Getting Started

First, install the dependencies:

```bash
npm install
```

## Environment Configuration

Create a `.env.local` file in the frontend directory with the following content:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

This tells the frontend where to find the backend API. Make sure your backend is running on the specified URL.

## Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Features

- **File Upload**: Drag and drop or browse to upload documents (PDF, TXT, MD, CSV, JSON)
- **File Management**: View uploaded files and processing statistics
- **Chat Interface**: Ask questions about your uploaded documents
- **Responsive Design**: Works on desktop and mobile devices

## Backend Integration

The frontend communicates with the backend API for:

- File upload and processing
- Document statistics
- Chat functionality (coming soon)

Make sure your backend is running and accessible at the configured API URL.
