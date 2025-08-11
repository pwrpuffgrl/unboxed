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
- **Privacy Mode**: Choose to anonymize sensitive data during upload
- **File Management**: View uploaded files, processing statistics, and privacy status
- **Chat Interface**: Ask questions about your uploaded documents
- **Debug Mode**: Toggle to see anonymized AI responses for transparency
- **Document Viewer**: View original files in their native format
- **File Deletion**: Remove files and associated data from the system
- **Responsive Design**: Works on desktop and mobile devices

## Backend Integration

The frontend communicates with the backend API for:

- File upload and processing (with privacy mode)
- Document statistics and privacy status
- Chat functionality with anonymization
- File management and deletion
- Document viewing and download

Make sure your backend is running and accessible at the configured API URL.
