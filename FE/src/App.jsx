import { useState, useRef, useEffect } from "react";
import { askQuestion } from "./services/api";
import QueryBox from "./components/QueryBox";
import AnswerCard from "./components/AnswerCard";
import SourcesCard from "./components/SourcesCard";
import ConnectionStatus from "./components/ConnectionStatus";

export default function App() {
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const handleAsk = async (q) => {
    if (!q.trim()) return;
    
    setIsLoading(true);
    const newQuestion = { type: 'question', content: q, timestamp: Date.now() };
    setChatHistory(prev => [...prev, newQuestion]);
    
    try {
      const res = await askQuestion(q);
      const newAnswer = { type: 'answer', content: res.answer, sources: res.sources, timestamp: Date.now() };
      setChatHistory(prev => [...prev, newAnswer]);
      setAnswer(res.answer);
      setSources(res.sources);
    } catch (error) {
      const errorAnswer = { type: 'error', content: 'Sorry, I encountered an error. Please try again.', timestamp: Date.now() };
      setChatHistory(prev => [...prev, errorAnswer]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-blue-100 sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-xl">🤖</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  TechCorp HR Assistant
                </h1>
                <p className="text-gray-600 text-sm">Your intelligent HR policy companion</p>
              </div>
            </div>
            <ConnectionStatus />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Welcome Message */}
        {chatHistory.length === 0 && (
          <div className="text-center mb-12">
            <div className="w-24 h-24 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mx-auto mb-6 flex items-center justify-center shadow-lg">
              <span className="text-white text-4xl">🤖</span>
            </div>
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Hello! How can I help you today?</h2>
            <p className="text-gray-600 text-lg mb-8">Ask me anything about HR policies, procedures, or company guidelines.</p>
            
            {/* Sample Questions */}
            <div className="grid md:grid-cols-3 gap-4 mb-8">
              {[
                "What is the vacation policy?",
                "How do I request time off?",
                "What are the working hours?"
              ].map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleAsk(question)}
                  className="p-4 bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-200 border border-gray-200 hover:border-blue-300 text-left"
                >
                  <span className="text-gray-700">{question}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Chat History */}
        {chatHistory.length > 0 && (
          <div className="mb-8">
            <div className="space-y-6">
              {chatHistory.map((message, index) => (
                <div key={index} className="animate-fade-in">
                  {message.type === 'question' && (
                    <div className="flex justify-end">
                      <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-3 rounded-2xl rounded-tr-sm max-w-2xl shadow-lg">
                        <p>{message.content}</p>
                      </div>
                    </div>
                  )}
                  {message.type === 'answer' && (
                    <div className="flex justify-start">
                      <div className="bg-white px-6 py-4 rounded-2xl rounded-tl-sm max-w-3xl shadow-lg border border-gray-100">
                        <p className="text-gray-800 whitespace-pre-wrap">{message.content}</p>
                        {message.sources && message.sources.length > 0 && (
                          <div className="mt-4 pt-4 border-t border-gray-100">
                            <p className="text-sm font-semibold text-gray-600 mb-2">📚 Sources:</p>
                            <div className="flex flex-wrap gap-2">
                              {message.sources.map((source, idx) => (
                                <span key={idx} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">
                                  {source}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                  {message.type === 'error' && (
                    <div className="flex justify-start">
                      <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-2xl rounded-tl-sm max-w-2xl">
                        <p>{message.content}</p>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
            
            {/* Loading indicator */}
            {isLoading && (
              <div className="flex justify-start mt-6">
                <div className="bg-white px-6 py-4 rounded-2xl rounded-tl-sm shadow-lg border border-gray-100">
                  <div className="flex items-center space-x-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                    <span className="text-gray-600 text-sm">Thinking...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
        )}

        {/* Query Input */}
        <div className="sticky bottom-0 bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-200 p-4">
          <QueryBox onSubmit={handleAsk} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
}
