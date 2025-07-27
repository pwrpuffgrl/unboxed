'use client';

import { createContext, useContext, useState, ReactNode } from 'react';
import { FileContextType } from '../types';

const FileContext = createContext<FileContextType | undefined>(undefined);

export function FileProvider({ children }: { children: ReactNode }) {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const triggerRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <FileContext.Provider value={{ refreshTrigger, triggerRefresh }}>
      {children}
    </FileContext.Provider>
  );
}

export function useFileContext() {
  const context = useContext(FileContext);
  if (context === undefined) {
    throw new Error('useFileContext must be used within a FileProvider');
  }
  return context;
} 