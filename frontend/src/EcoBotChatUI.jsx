import React, { useState } from 'react';
import axios from 'axios';
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
  const [chatHistory, setChatHistory] = useState([]); // store messages as { role: 'user' | 'assistant', content: string }

  // Toggle sidebar open/close
  const toggleSidebar = () => setIsSidebarOpen((prev) => !prev);

  // Send message to backend
  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // 1) Add user message to chat
    const userMessage = { role: 'user', content: input };
    setChatHistory((prev) => [...prev, userMessage]);

    try {
      // 2) Prepare form data
      const formData = new FormData();
      formData.append('query', input);
      // formData.append('pdf_context', ''); // Optional if you have a PDF context
      // If you have a file, you can do:
      // formData.append('file', selectedFile);

      // 3) Call your FastAPI endpoint
      const response = await axios.post('http://127.0.0.1:8000/query/', formData);
      console.log('Response from backend:', response.data);

      // 4) Extract backend response and add to chat
      const botResponse = response.data?.response || 'No response received.';
      const assistantMessage = { role: 'assistant', content: botResponse };
      setChatHistory((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error calling backend:', error);
      // Optionally add an error message to chat
      const assistantMessage = { role: 'assistant', content: `Error: ${error.message}` };
      setChatHistory((prev) => [...prev, assistantMessage]);
    } finally {
      setInput('');
    }
  };

  // Simple renderer for chat messages
  const renderMessages = () => {
    return chatHistory.map((msg, i) => {
      const isUser = msg.role === 'user';
      return (
        <div
          key={i}
          className={`w-full my-2 flex ${isUser ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`
              max-w-[60%] rounded-xl px-4 py-2
              ${isUser ? 'bg-green-600 text-white' : 'bg-gray-200 text-black'}
            `}
          >
            {msg.content}
          </div>
        </div>
      );
    });
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
          <div className="flex items-center">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-green-600 text-3xl font-bold tracking-wide">
              EcoBot
            </span>
          </div>
        </div>

        {/* Content Area: Chat display */}
        <div className="flex-1 overflow-y-auto p-4">
          {renderMessages()}
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
              {/* (Optional) if you want file attachments */}
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
