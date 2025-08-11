'use client';

import { useChatStore } from '../stores/chatStore';

export default function DebugStore() {
  const { messages, isLoading, error } = useChatStore();

  if (process.env.NODE_ENV === 'production') {
    return null;
  }

  return (
    <div className="fixed bottom-4 right-4 bg-black bg-opacity-80 text-white p-4 rounded-lg text-xs max-w-xs">
      <div className="font-bold mb-2">Debug Store State:</div>
      <div>Messages: {messages.length}</div>
      <div>Loading: {isLoading ? 'Yes' : 'No'}</div>
      <div>Error: {error || 'None'}</div>
      <div className="mt-2 text-gray-400">
        Last message: {messages[messages.length - 1]?.content?.substring(0, 30) || 'None'}...
      </div>
    </div>
  );
} 