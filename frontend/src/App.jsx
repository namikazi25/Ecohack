import React from 'react'
import EcoBotChatUI from './EcoBotChatUI'
import './App.css'  // or wherever your Tailwind/app styles reside

function App() {
  return (
    // Full viewport so your EcoBot UI can occupy the entire screen
    <div className="w-screen h-screen">
      {/* Render your EcoBot chat UI */}
      <EcoBotChatUI />
    </div>
  )
}

export default App
