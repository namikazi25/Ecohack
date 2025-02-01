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
  Leaf
} from 'lucide-react';

export default function EcoBotChatUI() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [input, setInput] = useState('');

  const toggleSidebar = () => setIsSidebarOpen((prev) => !prev);

  const handleSendMessage = () => {
    console.log('User message:', input);
    setInput('');
  };

  return (
    <div className="h-screen w-screen flex eco-main-bg text-white overflow-hidden">
      <div
        className={`${
          isSidebarOpen ? 'w-48' : 'w-16'
        } transition-all duration-300 eco-sidebar-bg flex flex-col`}
      >
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

      <div className="flex-1 flex flex-col">
        <div className="flex items-center h-16 px-4 eco-border-color border-b">
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-green-600 text-3xl font-bold tracking-wide">
            EcoBot
          </span>
        </div>

        <div className="flex-1 flex flex-col items-center justify-center px-4 py-8">
          <p className="text-gray-400">
            Chat messages will appear here.
          </p>
        </div>

        <div className="h-20 px-4 flex items-center eco-border-color border-t">
          <div className="flex items-center w-full eco-input-bg rounded-full px-4 py-2">
            <input
              type="text"
              className="flex-1 bg-transparent outline-none placeholder-gray-500 text-white"
              placeholder="Ask EcoBot about ecology..."
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