'use client';

import { useChatStore } from '../stores/chatStore';

export default function ChatHistory() {
  const { messages, isLoading, error, clearMessages } = useChatStore();

  if (messages.length === 0) {
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

  return (
    <div className="flex-1 overflow-y-auto p-6">
      {/* Header with clear button */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-white">Chat History</h2>
        <button
          onClick={clearMessages}
          className="text-gray-400 hover:text-white text-sm flex items-center gap-1 transition-colors py-1 px-2 rounded hover:bg-gray-700"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Clear Chat
        </button>
      </div>
      
      <div className="space-y-6">
        {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-[80%] rounded-2xl px-4 py-3 ${
              message.type === 'user'
                ? 'bg-emerald-600 text-white'
                : 'bg-gray-700 text-gray-100'
            }`}
          >
            <div className="text-sm">{message.content}</div>
            {message.type === 'assistant' && message.sources && message.sources.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-600">
                <div className="text-xs text-gray-400 mb-1">Sources:</div>
                <div className="text-xs text-gray-300 space-y-1">
                  {message.sources.map((source, index) => (
                    <div key={index} className="truncate">
                      {source}
                    </div>
                  ))}
                </div>
              </div>
            )}
            {message.type === 'assistant' && message.confidence !== undefined && (
              <div className="mt-2 text-xs text-gray-400">
                Confidence: {(message.confidence * 100).toFixed(1)}%
              </div>
            )}
          </div>
        </div>
      ))}
      
      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-gray-700 text-gray-100 rounded-2xl px-4 py-3">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            </div>
          </div>
        </div>
      )}
      
      {error && (
        <div className="flex justify-start">
          <div className="bg-red-600 text-white rounded-2xl px-4 py-3">
            <div className="text-sm">Error: {error}</div>
          </div>
        </div>
      )}
      </div>
    </div>
  );
} 