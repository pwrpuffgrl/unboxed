'use client';

import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { useFileContext } from '../contexts/FileContext';
import { FileGridState } from '../types';

export default function FileGrid() {
  const { refreshTrigger } = useFileContext();
  const [state, setState] = useState<FileGridState>({
    files: [],
    loading: true,
    error: null,
  });

  const fetchFiles = async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const response = await apiService.getFiles();
      setState({ files: response.files, loading: false, error: null });
    } catch (error) {
      setState({
        files: [],
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to load files',
      });
    }
  };

  useEffect(() => {
    fetchFiles();
  }, [refreshTrigger]);

  const getFileIcon = (contentType: string) => {
    switch (contentType) {
      case 'application/pdf':
        return (
          <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      case 'text/plain':
        return (
          <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      case 'text/markdown':
        return (
          <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      case 'text/csv':
        return (
          <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      case 'application/json':
        return (
          <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
      default:
        return (
          <svg className="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        );
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (state.loading) {
    return (
      <div className="bg-gray-800 rounded-xl p-4 shadow-xl border border-gray-700 h-full flex flex-col">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-white">All Files</h3>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-2 gap-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="h-32 bg-gray-700 rounded-lg"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (state.error) {
    return (
      <div className="bg-gray-800 rounded-xl p-4 shadow-xl border border-gray-700 h-full flex flex-col">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-white">All Files</h3>
        </div>
        
        <div className="bg-red-900/20 border border-red-500 text-red-400 px-4 py-3 rounded-lg">
          <p className="text-sm">{state.error}</p>
          <button 
            onClick={fetchFiles}
            className="mt-2 text-xs bg-red-600 hover:bg-red-700 px-2 py-1 rounded"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 rounded-xl p-4 shadow-xl border border-gray-700 h-full flex flex-col">
      <div className="flex items-center justify-between mb-6 flex-shrink-0">
        <h3 className="text-lg font-semibold text-white">All Files ({state.files.length})</h3>
      </div>
      
      {state.files.length === 0 ? (
        <div className="text-gray-400 text-center py-8">
          <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p>No files uploaded yet</p>
          <p className="text-sm">Upload documents to see them here</p>
        </div>
      ) : (
        <div className="overflow-y-auto h-80 pb-4">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-2 gap-3">
            {state.files.map((file) => (
            <div key={file.id} className="bg-gray-700 rounded-lg p-4 hover:bg-gray-600 transition-colors cursor-pointer">
              <div className="flex items-center space-x-3 mb-3">
                {getFileIcon(file.content_type)}
                <div className="text-[10px] text-gray-400">
                  {formatFileSize(file.file_size)}
                </div>
              </div>
              
              <h4 className="text-sm font-medium text-white mb-3 line-clamp-3" title={file.filename}>
                {file.filename}
              </h4>
              
              <div className="space-y-2">
                <div className="flex justify-between text-xs text-gray-400">
                  <span>Words:</span>
                  <span>{file.word_count.toLocaleString()}</span>
                </div>
                <div className="text-xs text-gray-400">
                  <div>Uploaded: {formatDate(file.created_at)}</div>
                </div>
              </div>
            </div>
          ))}
          </div>
          <div className="h-8"></div>
        </div>
      )}
    </div>
  );
} 