import Header from './components/Header';
import FileUpload from './components/FileUpload';
import FileList from './components/FileList';
import ChatHistory from './components/ChatHistory';
import ChatInput from './components/ChatInput';
import MobileSidebar from './components/MobileSidebar';
import { FileProvider } from './contexts/FileContext';

export default function Home() {
  return (
    <FileProvider>
      <div className="min-h-screen bg-gray-900 flex flex-col">
        <Header />

        {/* Main content area */}
        <div className="flex-1 flex overflow-hidden">
          {/* Desktop sidebar - File management */}
          <div className="hidden xl:block w-80 bg-gray-800 border-r border-gray-700 flex flex-col">
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              <FileUpload />
              <FileList />
            </div>
          </div>

          {/* Right side - Chat area */}
          <div className="flex-1 flex flex-col bg-gray-900">
            <ChatHistory />
            <ChatInput />
          </div>
        </div>

        {/* Mobile components */}
        <MobileSidebar />
      </div>
    </FileProvider>
  );
}