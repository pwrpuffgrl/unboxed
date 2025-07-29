import Header from './components/Header';
import FileUpload from './components/FileUpload';
import FileList from './components/FileList';
import ChatHistory from './components/ChatHistory';
import ChatInput from './components/ChatInput';
import MobileSidebar from './components/MobileSidebar';
import DebugStore from './components/DebugStore';
import { FileProvider } from './contexts/FileContext';

export default function Home() {
  return (
    <FileProvider>
      <div className="h-screen bg-gray-900 flex flex-col overflow-hidden">
        <Header />

        {/* Main content area */}
        <div className="flex-1 flex overflow-hidden">
          {/* Desktop sidebar - File management */}
          <div className="hidden lg:block w-96 xl:w-[28rem] 2xl:w-[32rem] bg-gray-800 border-r border-gray-700 flex flex-col h-full">
            <div className="flex-1 p-6 pb-12 space-y-6 overflow-y-auto">
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
        
        {/* Debug component (development only) */}
        <DebugStore />
      </div>
    </FileProvider>
  );
}