'use client';

import { useState, useRef, useCallback } from 'react';
import { apiService } from '../services/api';
import { useFileContext } from '../contexts/FileContext';
import { UploadState } from '../types';
import PrivacyPrompt from './PrivacyPrompt';

export default function FileUpload() {
  const { triggerRefresh } = useFileContext();
  const [uploadState, setUploadState] = useState<UploadState>({
    isUploading: false,
    progress: 0,
    error: null,
    success: null,
  });
  const [isDragOver, setIsDragOver] = useState(false);
  const [privacyPromptFile, setPrivacyPromptFile] = useState<File | null>(null);
  const [isPrivacyPromptOpen, setIsPrivacyPromptOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = useCallback((file: File): string | null => {
    const allowedFileTypes = [
      'application/pdf',
      'text/plain',
      'text/markdown',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/csv',
      'application/json'
    ];
    
    if (!allowedFileTypes.includes(file.type)) {
      return `File type ${file.type} is not supported. Please upload PDF, TXT, MD, CSV, or JSON files.`;
    }
    
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      return `File size ${(file.size / 1024 / 1024).toFixed(2)}MB exceeds the maximum limit of 10MB.`;
    }
    
    return null;
  }, []);

  const handleFileSelect = useCallback((file: File) => {
    const validationError = validateFile(file);
    if (validationError) {
      setUploadState(prev => ({ ...prev, error: validationError }));
      return;
    }

    // Show privacy prompt for file-specific privacy mode
    setPrivacyPromptFile(file);
    setIsPrivacyPromptOpen(true);
  }, [validateFile]);

  const handlePrivacyPromptConfirm = async (anonymize: boolean) => {
    if (!privacyPromptFile) return;

    setIsPrivacyPromptOpen(false);
    setPrivacyPromptFile(null);

    setUploadState({
      isUploading: true,
      progress: 0,
      error: null,
      success: null,
    });

    try {
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setUploadState(prev => ({
          ...prev,
          progress: Math.min(prev.progress + 10, 90),
        }));
      }, 200);

      const response = await apiService.uploadFile(privacyPromptFile, undefined, anonymize);
      
      clearInterval(progressInterval);
      
      const successMessage = anonymize && response.anonymization_summary
        ? `Successfully uploaded ${response.filename}! Processed ${response.chunks_processed} chunks. 🔒 Privacy mode: ${Object.entries(response.anonymization_summary).map(([type, count]) => `${count} ${type.toLowerCase()}`).join(', ')} anonymized.`
        : `Successfully uploaded ${response.filename}! Processed ${response.chunks_processed} chunks.`;

      setUploadState({
        isUploading: false,
        progress: 100,
        error: null,
        success: successMessage,
      });

      // Trigger refresh of file list
      triggerRefresh();

      // Clear success message after 5 seconds
      setTimeout(() => {
        setUploadState(prev => ({ ...prev, success: null }));
      }, 5000);

    } catch (error) {
      setUploadState({
        isUploading: false,
        progress: 0,
        error: error instanceof Error ? error.message : 'Upload failed',
        success: null,
      });
    }
  };

  const handlePrivacyPromptClose = () => {
    setIsPrivacyPromptOpen(false);
    setPrivacyPromptFile(null);
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  }, [handleFileSelect]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="space-y-4">
      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors duration-200 ${
          isDragOver
            ? 'border-cyan-500 bg-cyan-500/10'
            : uploadState.isUploading
            ? 'border-yellow-500 bg-yellow-500/10'
            : 'border-gray-600 hover:border-cyan-500'
        }`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <div className="text-gray-400 mb-3">
          <svg className="w-8 h-8 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>
        
        {uploadState.isUploading ? (
          <div className="space-y-4">
            <p className="text-yellow-400">Uploading file...</p>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div 
                className="bg-cyan-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadState.progress}%` }}
              ></div>
            </div>
            <p className="text-gray-400 text-sm">{uploadState.progress}%</p>
          </div>
        ) : (
          <>
            <p className="text-gray-300 mb-2">Drag and drop files here, or</p>
            <button 
              onClick={handleBrowseClick}
              disabled={uploadState.isUploading}
              className="bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg transition-colors duration-200"
            >
              Browse Files
            </button>
            <p className="text-gray-500 text-sm mt-2">Supports PDF, TXT, MD, CSV, JSON (Max 10MB)</p>
            <p className="text-gray-400 text-xs mt-1">🔒 Privacy mode can be enabled per file during upload</p>
          </>
        )}
      </div>

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.txt,.md,.csv,.json,.doc,.docx"
        onChange={handleFileInputChange}
        className="hidden"
      />

      {/* Privacy Prompt Modal */}
      {privacyPromptFile && (
        <PrivacyPrompt
          file={privacyPromptFile}
          isOpen={isPrivacyPromptOpen}
          onClose={handlePrivacyPromptClose}
          onConfirm={handlePrivacyPromptConfirm}
        />
      )}

      {/* Error message */}
      {uploadState.error && (
        <div className="bg-red-900/20 border border-red-500 text-red-400 px-4 py-3 rounded-lg">
          <p className="text-sm">{uploadState.error}</p>
        </div>
      )}

      {/* Success message */}
      {uploadState.success && (
        <div className="bg-green-900/20 border border-green-500 text-green-400 px-4 py-3 rounded-lg">
          <p className="text-sm">{uploadState.success}</p>
        </div>
      )}
    </div>
  );
} 