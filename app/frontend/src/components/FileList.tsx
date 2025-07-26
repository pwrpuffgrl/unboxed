export default function FileList() {
  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-xl border border-gray-700">
      <div className="flex items-center mb-4">
        <div className="w-3 h-3 bg-purple-500 rounded-full mr-3"></div>
        <h3 className="text-lg font-semibold text-white">Uploaded Files</h3>
      </div>
      
      <div className="space-y-3">
        {/* Placeholder for uploaded files */}
        <div className="text-gray-400 text-center py-8">
          <svg className="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p>No files uploaded yet</p>
          <p className="text-sm">Upload documents to get started</p>
        </div>
      </div>
    </div>
  );
} 