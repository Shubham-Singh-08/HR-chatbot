import { useState, useEffect } from 'react';
import { checkHealth } from '../services/api';

export default function ConnectionStatus() {
  const [isConnected, setIsConnected] = useState(null);
  const [serverInfo, setServerInfo] = useState(null);

  const checkConnection = async () => {
    try {
      const health = await checkHealth();
      setIsConnected(true);
      setServerInfo(health);
    } catch (error) {
      setIsConnected(false);
      setServerInfo(null);
    }
  };

  useEffect(() => {
    checkConnection();
    // Check connection every 30 seconds
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  if (isConnected === null) {
    return (
      <div className="flex items-center space-x-2 text-gray-500">
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
        <span className="text-sm">Checking connection...</span>
      </div>
    );
  }

  return (
    <div className="flex items-center space-x-2">
      <div className={`w-2 h-2 rounded-full ${
        isConnected ? 'bg-green-500' : 'bg-red-500'
      } ${isConnected ? 'animate-pulse' : ''}`}></div>
      <span className={`text-sm ${
        isConnected ? 'text-green-600' : 'text-red-600'
      }`}>
        {isConnected ? (
          <>Connected {serverInfo?.documents_loaded ? `• ${serverInfo.documents_loaded} documents loaded` : ''}</>
        ) : (
          'Backend disconnected'
        )}
      </span>
      {!isConnected && (
        <button
          onClick={checkConnection}
          className="text-xs text-blue-500 hover:text-blue-700 underline"
        >
          Retry
        </button>
      )}
    </div>
  );
}