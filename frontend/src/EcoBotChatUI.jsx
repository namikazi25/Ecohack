import React, { useState } from 'react';
import {
  Menu,
  X,
  MessageSquare,
  PlusCircle,
  Folder,
  User,
  Upload,
  Send,
  // We'll add a Leaf icon for an eco look
  Leaf
} from 'lucide-react';

export default function EcoBotChatUI() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [input, setInput] = useState('');

  // Toggle sidebar open/close
  const toggleSidebar = () => setIsSidebarOpen((prev) => !prev);

  // Placeholder function to handle sending a message
  const handleSendMessage = () => {
    // Integrate with your backend
    console.log('User message:', input);
    setInput('');
  };

  return (
    <div className="h-screen w-screen flex bg-[#16251D] text-white overflow-hidden">
      {/* Sidebar */}
      <div
        className={`
          ${isSidebarOpen ? 'w-48' : 'w-16'}
          transition-all duration-300
          bg-[#1F2C23] flex flex-col
        `}
      >
        {/* Sidebar top bar */}
        <div className="flex items-center justify-between px-2 py-4">
          {isSidebarOpen && (
            <div className="flex items-center gap-2 text-xl font-bold">
              <Leaf className="text-green-400" />
              <span>Eco</span>
            </div>
          )}
          <button
            onClick={toggleSidebar}
            className="text-gray-200 hover:text-green-400"
          >
            {isSidebarOpen ? <X /> : <Menu />}
          </button>
        </div>

        {/* Sidebar items */}
        <div className="flex flex-col gap-4 px-2">
          <button className="flex items-center gap-2 hover:text-green-400">
            <PlusCircle />
            {isSidebarOpen && <span>New Chat</span>}
          </button>
          <button className="flex items-center gap-2 hover:text-green-400">
            <MessageSquare />
            {isSidebarOpen && <span>Conversations</span>}
          </button>
          <button className="flex items-center gap-2 hover:text-green-400">
            <Folder />
            {isSidebarOpen && <span>Files</span>}
          </button>

          <div className="mt-auto" />
          <button className="flex items-center gap-2 hover:text-green-400 my-4">
            <User />
            {isSidebarOpen && <span>Profile</span>}
          </button>
        </div>
      </div>

      {/* Main Panel */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar (no model/online status) */}
        <div className="flex items-center h-16 px-4 border-b border-[#2B372E]">
          {/* EcoBot Title */}
          <div className="flex items-center">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-green-600 text-3xl font-bold tracking-wide">
              EcoBot
            </span>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 flex flex-col items-center justify-center px-4 py-8">
          <p className="text-gray-400">
            Chat messages will appear here.
          </p>
        </div>

        {/* Input Box */}
        <div className="h-20 px-4 flex items-center border-t border-[#2B372E]">
          <div className="flex items-center w-full bg-[#2B372E] rounded-full px-4 py-2">
            <input
              type="text"
              className="flex-1 bg-transparent outline-none placeholder-gray-500 text-white"
              placeholder="Ask EcoBot about ecology, biology, or species..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleSendMessage();
                }
              }}
            />
            <div className="flex items-center space-x-3 ml-2 text-gray-400">
              <Upload className="cursor-pointer hover:text-green-400" />
              <button onClick={handleSendMessage}>
                <Send className="text-gray-400 hover:text-green-400" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
