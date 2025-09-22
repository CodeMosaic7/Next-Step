import { useState, useEffect, useRef } from 'react';
import { Send, Facebook, Twitter, Instagram, Linkedin, Youtube, Bot, User, Loader } from 'lucide-react';
import { auth } from "../firebase";
import axios from "axios";
import Header from "../components/Header.jsx"

// Page Title Component
const PageTitle = () => {
  return (
    <div className="bg-gray-100 py-4">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-lg text-gray-600">AI Career Assistant</h1>
      </div>
    </div>
  );
};

// Agent Selector Component
const AgentSelector = ({ selectedAgent, onAgentChange }) => {
  const agents = [
    { id: 'COORDINATOR', name: 'Career Coordinator', description: 'General career guidance' },
    { id: 'PSYCHOLOGIST', name: 'AI Psychologist', description: 'Personality insights' },
    { id: 'COUNSELLOR', name: 'Career Counsellor', description: 'Career planning' }
  ];

  return (
    <div className="mb-4">
      <p className="text-sm text-gray-600 mb-2">Choose your AI assistant:</p>
      <div className="flex flex-wrap gap-2">
        {agents.map((agent) => (
          <button
            key={agent.id}
            onClick={() => onAgentChange(agent.id)}
            className={`px-3 py-2 rounded-lg text-xs transition-colors ${
              selectedAgent === agent.id
                ? 'bg-blue-600 text-white'
                : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            <div className="font-medium">{agent.name}</div>
            <div className="text-xs opacity-75">{agent.description}</div>
          </button>
        ))}
      </div>
    </div>
  );
};

// Chat Message Component
const ChatMessage = ({ message, isBot = false, agentType = 'COORDINATOR', isLoading = false }) => {
  const getAgentIcon = (type) => {
    switch(type) {
      case 'PSYCHOLOGIST':
        return '🧠';
      case 'COUNSELLOR':
        return '🎯';
      case 'COORDINATOR':
      default:
        return '🤖';
    }
  };

  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-4`}>
      <div className={`flex max-w-xs lg:max-w-md ${isBot ? 'flex-row' : 'flex-row-reverse'}`}>
        {isBot && (
          <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-3 flex-shrink-0">
            <span className="text-sm">{getAgentIcon(agentType)}</span>
          </div>
        )}
        
        <div className={`px-4 py-2 rounded-lg ${
          isBot 
            ? 'bg-gray-100 text-gray-900' 
            : 'bg-blue-600 text-white'
        }`}>
          <div className="text-sm leading-relaxed">
            {isLoading ? (
              <div className="flex items-center space-x-2">
                <Loader className="w-4 h-4 animate-spin" />
                <span>Thinking...</span>
              </div>
            ) : (
              message
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Suggested Questions Component
const SuggestedQuestions = ({ questions, onQuestionClick, selectedAgent }) => {
  const getAgentQuestions = (agentType) => {
    switch(agentType) {
      case 'PSYCHOLOGIST':
        return [
          "What are my personality strengths?",
          "How do I handle stress better?",
          "What motivates me at work?",
          "Help me understand my work style"
        ];
      case 'COUNSELLOR':
        return [
          "What career path suits me?",
          "How do I change careers?",
          "What skills should I develop?",
          "Create a learning roadmap for me"
        ];
      case 'COORDINATOR':
      default:
        return [
          "What career is best for someone good at biology?",
          "What are the steps to become a software engineer?",
          "Can you suggest resources for learning graphic design?",
          "How do I prepare for UX interviews?"
        ];
    }
  };

  const relevantQuestions = getAgentQuestions(selectedAgent);

  return (
    <div className="mb-6">
      <div className="flex flex-wrap gap-2">
        {relevantQuestions.map((question, index) => (
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
const ChatInput = ({ message, setMessage, onSend, isLoading }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
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
          disabled={isLoading}
          className="w-full px-4 py-2 border border-gray-300 rounded-full focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none disabled:opacity-50"
        />
      </div>
      <button
        type="submit"
        disabled={!message.trim() || isLoading}
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
      text: "Hello! I'm your AI career advisor. I can help you with career guidance, personality insights, and skill development. Which assistant would you like to talk to?",
      isBot: true,
      agentType: 'COORDINATOR',
      timestamp: new Date()
    }
  ]);
  
  const [currentMessage, setCurrentMessage] = useState('');
  const [selectedAgent, setSelectedAgent] = useState('COORDINATOR');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionToken, setSessionToken] = useState(null);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  const API_BASE_URL = import.meta.env.VITE_APP_API_URL || "http://127.0.0.1:8000";

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message) => {
    // Add user message
    const userMessage = {
      text: message,
      isBot: false,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError('');

    // Add loading message
    const loadingMessage = {
      text: "",
      isBot: true,
      agentType: selectedAgent,
      isLoading: true,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, loadingMessage]);

    try {
      if (!auth.currentUser) {
        throw new Error("Please sign in to use the AI assistant");
      }

      const token = await auth.currentUser.getIdToken();
      
      const requestData = {
        agent_type: selectedAgent,
        interaction_type: "CHAT",
        user_message: message,
        context_data: {
          previous_messages: messages.slice(-5), // Send last 5 messages for context
          timestamp: new Date().toISOString()
        },
        session_token: sessionToken
      };

      const response = await axios.post(`${API_BASE_URL}/api/v1/agent/interact`, requestData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        timeout: 30000 // 30 seconds timeout for AI responses
      });

      // Remove loading message and add actual response
      setMessages(prev => prev.slice(0, -1));

      const botResponse = {
        text: response.data.agent_response,
        isBot: true,
        agentType: selectedAgent,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botResponse]);
      
      // Update session token if provided
      if (response.data.session_token) {
        setSessionToken(response.data.session_token);
      }

    } catch (err) {
      console.error("Chat error:", err);
      
      // Remove loading message
      setMessages(prev => prev.slice(0, -1));
      
      let errorMessage = "I'm having trouble connecting right now. Please try again.";
      
      if (err.response?.status === 401) {
        errorMessage = "Please sign in to continue chatting.";
      } else if (err.response?.status === 429) {
        errorMessage = "Too many requests. Please wait a moment before trying again.";
      } else if (err.code === 'ECONNABORTED') {
        errorMessage = "The request is taking too long. Please try a shorter message.";
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      }

      const errorResponse = {
        text: errorMessage,
        isBot: true,
        agentType: selectedAgent,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorResponse]);
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuestionClick = (question) => {
    handleSendMessage(question);
  };

  const handleAgentChange = (agentType) => {
    setSelectedAgent(agentType);
    
    // Add system message about agent change
    const agentNames = {
      'COORDINATOR': 'Career Coordinator',
      'PSYCHOLOGIST': 'AI Psychologist',
      'COUNSELLOR': 'Career Counsellor'
    };

    const systemMessage = {
      text: `Switched to ${agentNames[agentType]}. How can I help you today?`,
      isBot: true,
      agentType: agentType,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, systemMessage]);
  };

  const getAgentStatus = () => {
    const agentNames = {
      'COORDINATOR': 'Career Coordinator',
      'PSYCHOLOGIST': 'AI Psychologist', 
      'COUNSELLOR': 'Career Counsellor'
    };
    
    return agentNames[selectedAgent] || 'AI Assistant';
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        {/* Chat Header */}
        <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                <Bot className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">{getAgentStatus()}</h3>
                <p className="text-sm text-gray-500">
                  {isLoading ? 'Typing...' : 'Online'}
                </p>
              </div>
            </div>
            
            {/* Connection Status */}
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${
                error ? 'bg-red-400' : 'bg-green-400'
              }`}></div>
              <span className="text-xs text-gray-500">
                {error ? 'Connection Error' : 'Connected'}
              </span>
            </div>
          </div>
        </div>

        {/* Agent Selector */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <AgentSelector 
            selectedAgent={selectedAgent}
            onAgentChange={handleAgentChange}
          />
        </div>
        
        {/* Chat Messages */}
        <div className="p-6 min-h-96 max-h-96 overflow-y-auto">
          {messages.map((message, index) => (
            <ChatMessage
              key={index}
              message={message.text}
              isBot={message.isBot}
              agentType={message.agentType || selectedAgent}
              isLoading={message.isLoading}
            />
          ))}
          <div ref={messagesEndRef} />
        </div>
        
        {/* Suggested Questions */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
          <p className="text-sm text-gray-600 mb-3">Suggested questions for {getAgentStatus()}:</p>
          <SuggestedQuestions 
            selectedAgent={selectedAgent}
            onQuestionClick={handleQuestionClick}
          />
        </div>
        
        {/* Error Display */}
        {error && (
          <div className="px-6 py-2 bg-red-50 border-t border-red-200">
            <p className="text-sm text-red-600 flex items-center">
              <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {error}
            </p>
          </div>
        )}
        
        {/* Chat Input */}
        <div className="px-6 py-4 border-t border-gray-200">
          <ChatInput
            message={currentMessage}
            setMessage={setCurrentMessage}
            onSend={handleSendMessage}
            isLoading={isLoading}
          />
          
          {/* Usage Tip */}
          <p className="text-xs text-gray-500 mt-2 text-center">
            Tip: Switch between different AI assistants for specialized advice
          </p>
        </div>
      </div>

      {/* Chat History Note */}
      <div className="mt-4 text-center">
        <p className="text-xs text-gray-500">
          Your conversations are saved and can help provide better personalized advice over time.
        </p>
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