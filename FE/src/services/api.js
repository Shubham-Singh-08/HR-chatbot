import axios from "axios";

// Configure base URL
const API_BASE_URL = "http://localhost:8000";

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('Making API request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('API response received:', response.status);
    return response;
  },
  (error) => {
    console.error('API error:', error);
    if (error.code === 'ECONNREFUSED') {
      throw new Error('Backend server is not running. Please start the backend server.');
    }
    if (error.response?.status === 500) {
      throw new Error('Server error occurred. Please try again.');
    }
    throw error;
  }
);

export const askQuestion = async (question) => {
  try {
    const response = await api.post("/query", { question });
    return response.data;
  } catch (error) {
    console.error("Error asking question:", error);
    throw error;
  }
};

export const checkHealth = async () => {
  try {
    const response = await api.get("/health");
    return response.data;
  } catch (error) {
    console.error("Health check failed:", error);
    throw error;
  }
};
