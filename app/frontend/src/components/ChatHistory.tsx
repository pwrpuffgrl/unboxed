export default function ChatHistory() {
  return (
    <div className="flex-1 overflow-y-auto p-6">
      {/* Welcome message when no chat has started */}
      <div className="text-center text-gray-400 py-12">
        <div className="w-16 h-16 bg-gray-700 rounded-full mx-auto mb-4 flex items-center justify-center">
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold mb-2">Welcome to Unboxed RAG</h3>
        <p className="mb-4">Upload some documents and start asking questions!</p>
        <div className="text-sm space-y-1">
          <p>• Upload PDF, TXT, MD, CSV, or JSON files</p>
          <p>• Ask questions about your documents</p>
          <p>• Get AI-powered answers with source references</p>
        </div>
      </div>
    </div>
  );
} 