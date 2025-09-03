import React, { useState } from 'react';
import { Send, Facebook, Twitter, Instagram, Linkedin, Youtube } from 'lucide-react';

// Reusing Header Component
const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <span className="text-2xl font-bold text-blue-600">NextStep</span>
            </div>
            <nav className="hidden md:ml-6 md:flex md:space-x-8">
              <a href="#" className="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium">Home</a>
              <a href="#" className="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium">Assessment</a>
              <a href="#" className="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium">Careers</a>
              <a href="#" className="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium">Mentors</a>
              <a href="#" className="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium">Resources</a>
              <a href="#" className="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium">Profile</a>
            </nav>
          </div>
          <div className="flex items-center">
            <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
              <span className="text-sm font-medium">AJ</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

// Page Title Component
const PageTitle = () => {
  return (
    <div className="bg-gray-100 py-4">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-lg text-gray-600">FAQ / Chatbot</h1>
      </div>
    </div>
  );
};

// Chat Message Component
const ChatMessage = ({ message, isBot = false }) => {
  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-4`}>
      <div className={`flex max-w-xs lg:max-w-md ${isBot ? 'flex-row' : 'flex-row-reverse'}`}>
        {isBot && (
          <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center mr-3 flex-shrink-0">
            <span className="text-xs font-medium text-gray-700">NS</span>
          </div>
        )}
        
        <div className={`px-4 py-2 rounded-lg ${
          isBot 
            ? 'bg-gray-100 text-gray-900' 
            : 'bg-blue-600 text-white'
        }`}>
          <div className="text-sm leading-relaxed">
            {message}
          </div>
        </div>
      </div>
    </div>
  );
};

// Suggested Questions Component
const SuggestedQuestions = ({ questions, onQuestionClick }) => {
  return (
    <div className="mb-6">
      <div className="flex flex-wrap gap-2">
        {questions.map((question, index) => (
          <button
            key={index}
            onClick={() => onQuestionClick(question)}
            className="bg-white border border-gray-300 text-gray-700 px-3 py-2 rounded-full text-xs hover:bg-gray-50 transition-colors"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
};

// Chat Input Component
const ChatInput = ({ message, setMessage, onSend }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSend(message);
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2">
      <div className="flex-1 relative">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
          className="w-full px-4 py-2 border border-gray-300 rounded-full focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
        />
      </div>
      <button
        type="submit"
        disabled={!message.trim()}
        className="p-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <Send className="w-5 h-5" />
      </button>
    </form>
  );
};

// Footer Component
const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex space-x-6 text-sm mb-4 md:mb-0">
            <a href="#" className="hover:text-gray-300">Company</a>
            <a href="#" className="hover:text-gray-300">Support</a>
            <a href="#" className="hover:text-gray-300">Legal</a>
          </div>
          
          <div className="flex space-x-4">
            <Facebook className="w-5 h-5 text-gray-400 hover:text-blue-400 cursor-pointer" />
            <Twitter className="w-5 h-5 text-gray-400 hover:text-blue-300 cursor-pointer" />
            <Instagram className="w-5 h-5 text-gray-400 hover:text-pink-400 cursor-pointer" />
            <Linkedin className="w-5 h-5 text-gray-400 hover:text-blue-400 cursor-pointer" />
            <Youtube className="w-5 h-5 text-gray-400 hover:text-red-400 cursor-pointer" />
          </div>
        </div>
      </div>
    </footer>
  );
};

// Main Chat Component
const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      text: "Hello! I am Next Step Bot, your AI career advisor. How can I assist you today?",
      isBot: true,
      timestamp: new Date()
    }
  ]);
  
  const [currentMessage, setCurrentMessage] = useState('');
  
  const suggestedQuestions = [
    "What career is best for someone good at biology?",
    "What are the steps to become a software engineer?",
    "Can you suggest resources for learning graphic design?",
    "How do I prepare for UX interviews?"
  ];

  const handleSendMessage = (message) => {
    // Add user message
    const userMessage = {
      text: message,
      isBot: false,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    
    // Simulate bot response
    setTimeout(() => {
      const botResponse = {
        text: "I can help you explore career paths, understand necessary skills, and suggest resources. You can also ask me about specific industries or job requirements.",
        isBot: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botResponse]);
    }, 1000);
  };

  const handleQuestionClick = (question) => {
    handleSendMessage(question);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        {/* Chat Header */}
        <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
          <div className="flex items-center">
            <div className="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center mr-3">
              <span className="text-sm font-medium text-gray-700">NS</span>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">Next Step Bot</h3>
              <p className="text-sm text-gray-500">Online</p>
            </div>
          </div>
        </div>
        
        {/* Chat Messages */}
        <div className="p-6 min-h-96 max-h-96 overflow-y-auto">
          {messages.map((message, index) => (
            <ChatMessage
              key={index}
              message={message.text}
              isBot={message.isBot}
            />
          ))}
        </div>
        
        {/* Suggested Questions */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
          <p className="text-sm text-gray-600 mb-3">Suggested questions:</p>
          <SuggestedQuestions 
            questions={suggestedQuestions}
            onQuestionClick={handleQuestionClick}
          />
        </div>
        
        {/* Chat Input */}
        <div className="px-6 py-4 border-t border-gray-200">
          <ChatInput
            message={currentMessage}
            setMessage={setCurrentMessage}
            onSend={handleSendMessage}
          />
        </div>
      </div>
    </div>
  );
};

// Main App Component
const Chatbot = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <PageTitle />
      <ChatInterface />
      <Footer />
    </div>
  );
};

export default Chatbot;
