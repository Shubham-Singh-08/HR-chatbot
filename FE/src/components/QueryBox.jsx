import { useState } from "react";

export default function QueryBox({ onSubmit, isLoading }) {
  const [inputValue, setInputValue] = useState("");
  const [isFocused, setIsFocused] = useState(false);

  const handleSubmit = () => {
    if (inputValue.trim() && !isLoading) {
      onSubmit(inputValue);
      setInputValue("");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="relative">
      <div className={`flex items-center space-x-3 transition-all duration-200 ${
        isFocused ? 'transform scale-[1.01]' : ''
      }`}>
        <div className="flex-1 relative">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Ask me about HR policies, benefits, procedures..."
            disabled={isLoading}
            className={`w-full px-6 py-4 pr-12 border-2 rounded-2xl bg-white transition-all duration-200 resize-none overflow-hidden min-h-[56px] max-h-32 ${
              isFocused 
                ? 'border-blue-400 shadow-lg shadow-blue-100' 
                : 'border-gray-200 hover:border-gray-300'
            } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
            style={{ height: 'auto' }}
            onInput={(e) => {
              e.target.style.height = 'auto';
              e.target.style.height = Math.min(e.target.scrollHeight, 128) + 'px';
            }}
          />
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            {isLoading ? (
              <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <span className="text-gray-400 text-sm">↵</span>
            )}
          </div>
        </div>
        
        <button
          onClick={handleSubmit}
          disabled={!inputValue.trim() || isLoading}
          className={`px-6 py-4 rounded-2xl font-semibold transition-all duration-200 transform hover:scale-105 disabled:scale-100 disabled:opacity-50 disabled:cursor-not-allowed ${
            inputValue.trim() && !isLoading
              ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg hover:shadow-xl'
              : 'bg-gray-200 text-gray-500'
          }`}
        >
          {isLoading ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            '🚀'
          )}
        </button>
      </div>
      
      <p className="text-xs text-gray-500 mt-2 text-center">
        Press Enter to send • Shift + Enter for new line
      </p>
    </div>
  );
}
