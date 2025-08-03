'use client';

import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { DocumentViewerProps, DocumentViewerState } from '../types';

export default function DocumentViewer({ fileId, filename, contentType, onClose }: DocumentViewerProps) {
  const [state, setState] = useState<DocumentViewerState>({
    content: null,
    blobUrl: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    const fetchContent = async () => {
      try {
        setState(prev => ({ ...prev, loading: true, error: null }));
        
        // Try to get original file blob first for better display
        try {
          const blob = await apiService.getFileBlob(fileId);
          const blobUrl = URL.createObjectURL(blob);
          setState({ content: null, blobUrl, loading: false, error: null });
        } catch (blobError) {
          console.warn('Failed to load file blob, falling back to text content:', blobError);
          // Fallback to text content if blob fails
          const response = await apiService.getFileContent(fileId);
          setState({ content: response.content, blobUrl: null, loading: false, error: null });
        }
      } catch (error) {
        console.error('Failed to load document content:', error);
        setState({
          content: null,
          blobUrl: null,
          loading: false,
          error: error instanceof Error ? error.message : 'Failed to load document content',
        });
      }
    };

    fetchContent();

    // Cleanup blob URL on unmount
    return () => {
      if (state.blobUrl) {
        URL.revokeObjectURL(state.blobUrl);
      }
    };
  }, [fileId]);

  const getFileIcon = (contentType: string) => {
    switch (contentType) {
      case 'application/pdf':
        return (
          <svg className="w-6 h-6 text-red-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      case 'text/plain':
        return (
          <svg className="w-6 h-6 text-blue-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      case 'text/markdown':
        return (
          <svg className="w-6 h-6 text-purple-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      case 'text/csv':
        return (
          <svg className="w-6 h-6 text-green-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      case 'application/json':
        return (
          <svg className="w-6 h-6 text-yellow-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      default:
        return (
          <svg className="w-6 h-6 text-gray-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
    }
  };

  const formatContent = (content: string, contentType: string) => {
    // For JSON files, try to format them nicely
    if (contentType === 'application/json') {
      try {
        const parsed = JSON.parse(content);
        return JSON.stringify(parsed, null, 2);
      } catch {
        return content;
      }
    }
    
    // For CSV files, add some basic formatting
    if (contentType === 'text/csv') {
      return content.split('\n').map(line => line.trim()).filter(line => line).join('\n');
    }
    
    return content;
  };

  if (state.loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-gray-800 rounded-xl p-6 shadow-xl border border-gray-700 max-w-7xl w-full mx-4 max-h-[98vh] flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              {getFileIcon(contentType)}
              <h2 className="text-xl font-semibold text-white ml-3">Loading...</h2>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div className="flex-1 flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
          </div>
        </div>
      </div>
    );
  }

  if (state.error) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-gray-800 rounded-xl p-6 shadow-xl border border-gray-700 max-w-7xl w-full mx-4 max-h-[98vh] flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              {getFileIcon(contentType)}
              <h2 className="text-xl font-semibold text-white ml-3">{filename}</h2>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div className="flex-1 flex items-center justify-center">
            <div className="bg-red-900/20 border border-red-500 text-red-400 px-6 py-4 rounded-lg text-center">
              <p className="text-lg font-semibold mb-2">Error Loading Document</p>
              <p className="text-sm">{state.error}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-xl p-6 shadow-xl border border-gray-700 max-w-7xl w-full mx-4 max-h-[98vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            {getFileIcon(contentType)}
            <div className="ml-3">
              <h2 className="text-xl font-semibold text-white">{filename}</h2>
              <p className="text-sm text-gray-400">{contentType}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors p-2 hover:bg-gray-700 rounded-lg"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-hidden min-h-[85vh]">
          {state.blobUrl ? (
            // Display file in its native format
            <div className="bg-white rounded-lg h-full overflow-hidden min-h-[85vh]">
              {contentType === 'application/pdf' ? (
                <iframe
                  src={state.blobUrl}
                  className="w-full h-full min-h-[80vh]"
                  title={filename}
                  style={{ minHeight: '80vh' }}
                />
              ) : contentType.startsWith('image/') ? (
                <img
                  src={state.blobUrl}
                  alt={filename}
                  className="w-full h-full object-contain"
                />
              ) : contentType.startsWith('text/') || contentType === 'application/json' ? (
                <iframe
                  src={state.blobUrl}
                  className="w-full h-full bg-white"
                  title={filename}
                />
              ) : (
                <div className="flex items-center justify-center h-full bg-gray-100">
                  <div className="text-center">
                    <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <p className="text-gray-600">Preview not available for this file type</p>
                    <a
                      href={state.blobUrl}
                      download={filename}
                      className="mt-2 inline-block bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 transition-colors"
                    >
                      Download File
                    </a>
                  </div>
                </div>
              )}
            </div>
          ) : (
            // Fallback to text display
            <div className="bg-gray-900 rounded-lg p-4 h-full overflow-auto">
              <pre className="text-sm text-gray-300 whitespace-pre-wrap font-mono">
                {state.content ? formatContent(state.content, contentType) : 'No content available'}
              </pre>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="mt-4 flex justify-between items-center text-sm text-gray-400">
          <span>File ID: {fileId}</span>
          <span>
            {state.blobUrl ? (
              <a
                href={state.blobUrl}
                download={filename}
                className="text-purple-400 hover:text-purple-300 transition-colors"
              >
                Download
              </a>
            ) : (
              `${state.content ? state.content.length : 0} characters`
            )}
          </span>
        </div>
      </div>
    </div>
  );
} 