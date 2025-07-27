export default function ChatInput() {
  return (
    <div className="bg-gray-800 border-t border-gray-700 p-4 flex-shrink-0">
      <div className="relative w-full">
        <input
          type="text"
          placeholder="Ask a question about your documents..."
          className="w-full bg-gray-700 text-white placeholder-gray-400 rounded-xl px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
        />
        <button className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-2 rounded-lg transition-colors duration-200 flex items-center gap-2">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
    </div>
  );
} 