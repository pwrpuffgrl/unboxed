'use client';

import { useState } from 'react';
import { Shield, ShieldCheck } from 'lucide-react';

interface PrivacyToggleProps {
  isEnabled: boolean;
  onToggle: (enabled: boolean) => void;
  className?: string;
}

export default function PrivacyToggle({ isEnabled, onToggle, className = '' }: PrivacyToggleProps) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div className={`flex items-center space-x-3 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200 ${className}`}>
      <div className="flex items-center space-x-2">
        {isEnabled ? (
          <ShieldCheck className="w-5 h-5 text-green-600" />
        ) : (
          <Shield className="w-5 h-5 text-gray-500" />
        )}
        <span className="font-medium text-gray-900">
          Privacy Mode
        </span>
      </div>
      
      <div className="flex items-center space-x-2">
        <button
          type="button"
          onClick={() => onToggle(!isEnabled)}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          className={`
            relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
            ${isEnabled 
              ? 'bg-green-600 hover:bg-green-700' 
              : 'bg-gray-200 hover:bg-gray-300'
            }
          `}
        >
          <span
            className={`
              inline-block h-4 w-4 transform rounded-full bg-white transition-transform
              ${isEnabled ? 'translate-x-6' : 'translate-x-1'}
            `}
          />
        </button>
        
        <span className={`text-sm font-medium ${isEnabled ? 'text-green-700' : 'text-gray-600'}`}>
          {isEnabled ? 'ON' : 'OFF'}
        </span>
      </div>
      
      <div className="relative">
        {isHovered && (
          <div className="absolute z-10 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 p-3 text-sm text-gray-600 pointer-events-none">
            <div className="flex items-start space-x-2">
              <Shield className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
              <div>
                <p className="font-medium text-gray-900 mb-1">
                  {isEnabled ? 'Privacy Mode Active' : 'Privacy Mode Inactive'}
                </p>
                <p className="text-gray-600">
                  {isEnabled 
                    ? 'Sensitive data (names, emails, phones, etc.) will be automatically detected and anonymized before processing.'
                    : 'Files will be processed as-is. Consider enabling privacy mode for sensitive documents.'
                  }
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 