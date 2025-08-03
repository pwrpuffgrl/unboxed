'use client';

import { useState } from 'react';
import { Shield, ShieldCheck, Upload, X } from 'lucide-react';

interface PrivacyPromptProps {
  file: File;
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (anonymize: boolean) => void;
}

export default function PrivacyPrompt({ file, isOpen, onClose, onConfirm }: PrivacyPromptProps) {
  const [privacyMode, setPrivacyMode] = useState(false);

  if (!isOpen) return null;

  const handleConfirm = () => {
    onConfirm(privacyMode);
    setPrivacyMode(false); // Reset for next file
  };

  const handleCancel = () => {
    onClose();
    setPrivacyMode(false); // Reset for next file
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4 border border-gray-700">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white flex items-center space-x-2">
            <Upload className="w-5 h-5 text-cyan-400" />
            <span>Upload File</span>
          </h3>
          <button
            onClick={handleCancel}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* File Info */}
        <div className="mb-6">
          <div className="bg-gray-700 rounded-lg p-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-cyan-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-medium text-sm">
                  {file.name.split('.').pop()?.toUpperCase() || 'FILE'}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-white font-medium truncate">{file.name}</p>
                <p className="text-gray-400 text-sm">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Privacy Mode Toggle */}
        <div className="mb-6">
          <div className="flex items-center space-x-3 p-4 bg-gradient-to-r from-blue-900/50 to-indigo-900/50 rounded-lg border border-blue-700">
            <div className="flex items-center space-x-2">
              {privacyMode ? (
                <ShieldCheck className="w-5 h-5 text-green-400" />
              ) : (
                <Shield className="w-5 h-5 text-gray-400" />
              )}
              <span className="font-medium text-white">
                Privacy Mode
              </span>
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                type="button"
                onClick={() => setPrivacyMode(!privacyMode)}
                className={`
                  relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-offset-2 focus:ring-offset-gray-800
                  ${privacyMode 
                    ? 'bg-green-600 hover:bg-green-700' 
                    : 'bg-gray-600 hover:bg-gray-500'
                  }
                `}
              >
                <span
                  className={`
                    inline-block h-4 w-4 transform rounded-full bg-white transition-transform
                    ${privacyMode ? 'translate-x-6' : 'translate-x-1'}
                  `}
                />
              </button>
              
              <span className={`text-sm font-medium ${privacyMode ? 'text-green-400' : 'text-gray-400'}`}>
                {privacyMode ? 'ON' : 'OFF'}
              </span>
            </div>
          </div>
          
          <p className="text-gray-400 text-sm mt-3">
            {privacyMode 
              ? '🔒 Sensitive data (names, emails, phones, etc.) will be automatically detected and anonymized before processing.'
              : '📄 File will be processed as-is. Consider enabling privacy mode for sensitive documents.'
            }
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-3">
          <button
            onClick={handleCancel}
            className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleConfirm}
            className="flex-1 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg transition-colors flex items-center justify-center space-x-2"
          >
            <Upload className="w-4 h-4" />
            <span>Upload</span>
          </button>
        </div>
      </div>
    </div>
  );
} 