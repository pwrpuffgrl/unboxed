'use client';

import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { useFileContext } from '../contexts/FileContext';
import FileGrid from './FileGrid';
import { FileListState } from '../types';

export default function FileList() {
  const { refreshTrigger } = useFileContext();
  const [viewMode, setViewMode] = useState<'stats' | 'grid'>('stats');
  const [state, setState] = useState<FileListState>({
    stats: null,
    loading: true,
    error: null,
  });

  const fetchStats = async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const stats = await apiService.getStats();
      setState({ stats, loading: false, error: null });
    } catch (error) {
      setState({
        stats: null,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to load stats',
      });
    }
  };

  useEffect(() => {
    fetchStats();
  }, [refreshTrigger]);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatNumber = (num: number): string => {
    return new Intl.NumberFormat().format(num);
  };

  if (state.loading) {
    return (
      <div className="bg-gray-800 rounded-xl p-4 shadow-xl border border-gray-700">
        <div className="flex items-center mb-4">
          <div className="w-3 h-3 bg-purple-500 rounded-full mr-3"></div>
          <h3 className="text-lg font-semibold text-white">Uploaded Files</h3>
        </div>
        
        <div className="space-y-4">
          <div className="animate-pulse">
            <div className="h-4 bg-gray-700 rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-gray-700 rounded w-1/2 mb-2"></div>
            <div className="h-4 bg-gray-700 rounded w-2/3"></div>
          </div>
        </div>
      </div>
    );
  }

  if (state.error) {
    return (
      <div className="bg-gray-800 rounded-xl p-4 shadow-xl border border-gray-700">
        <div className="flex items-center mb-4">
          <div className="w-3 h-3 bg-purple-500 rounded-full mr-3"></div>
          <h3 className="text-lg font-semibold text-white">Uploaded Files</h3>
        </div>
        
        <div className="bg-red-900/20 border border-red-500 text-red-400 px-4 py-3 rounded-lg">
          <p className="text-sm">{state.error}</p>
          <button 
            onClick={fetchStats}
            className="mt-2 text-xs bg-red-600 hover:bg-red-700 px-2 py-1 rounded"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const stats = state.stats;
  const hasFiles = stats && stats.file_count > 0;

  return (
    <div className="bg-gray-800 rounded-xl p-4 shadow-xl border border-gray-700 flex flex-col">
      <div className="flex items-center mb-4">
        <div className="flex items-center">
          <div className="w-3 h-3 bg-purple-500 rounded-full mr-3"></div>
          <h3 className="text-lg font-semibold text-white">Uploaded Files</h3>
        </div>
        <button 
          onClick={fetchStats}
          className="ml-auto text-gray-400 hover:text-white transition-colors"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
      
      <div className="flex items-center mb-2 flex-shrink-0">
        <div className="flex bg-gray-700 rounded-lg p-1">
          <button
            onClick={() => setViewMode('stats')}
            className={`px-3 py-1 text-xs rounded-md transition-colors ${
              viewMode === 'stats'
                ? 'bg-cyan-600 text-white'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            Stats
          </button>
          <button
            onClick={() => setViewMode('grid')}
            className={`px-3 py-1 text-xs rounded-md transition-colors ${
              viewMode === 'grid'
                ? 'bg-cyan-600 text-white'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            Grid
          </button>
        </div>
      </div>
      
      <div className="flex-1 overflow-hidden">
        {viewMode === 'grid' ? (
          <FileGrid />
        ) : (
        <>
          {hasFiles ? (
            <div className="space-y-4">
              {/* File Statistics */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-700 rounded-lg p-3">
                  <div className="text-2xl font-bold text-white">{formatNumber(stats!.file_count)}</div>
                  <div className="text-xs text-gray-400">Files</div>
                </div>
                <div className="bg-gray-700 rounded-lg p-3">
                  <div className="text-2xl font-bold text-white">{formatNumber(stats!.chunk_count)}</div>
                  <div className="text-xs text-gray-400">Chunks</div>
                </div>
              </div>
              
              <div className="bg-gray-700 rounded-lg p-3">
                <div className="text-2xl font-bold text-white">{formatNumber(stats!.total_words)}</div>
                <div className="text-xs text-gray-400">Total Words</div>
              </div>

              {/* File List Placeholder - In a real app, you'd fetch actual file list */}
              <div className="border-t border-gray-700 pt-4">
                <h4 className="text-sm font-medium text-gray-300 mb-3">Recent Files</h4>
                <div className="space-y-2">
                  <div className="flex items-center justify-between p-2 bg-gray-700 rounded">
                    <div className="flex items-center">
                      <svg className="w-4 h-4 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <span className="text-sm text-gray-300">Document files</span>
                    </div>
                    <span className="text-xs text-gray-500">{stats!.file_count} files</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-gray-400 text-center py-8">
              <svg className="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p>No files uploaded yet</p>
              <p className="text-sm">Upload documents to get started</p>
            </div>
          )}
        </>
        )}
      </div>
    </div>
  );
} 