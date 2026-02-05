# 🤖 TechCorp HR Chatbot

An intelligent HR assistant powered by Azure OpenAI and RAG (Retrieval-Augmented Generation) technology. This application provides instant answers to HR policy questions using a modern React frontend and FastAPI backend.

![HR Chatbot Demo](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.11+-blue) ![React](https://img.shields.io/badge/React-18+-61dafb) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)

## ✨ Features

- 🎯 **Intelligent Q&A**: Ask questions about HR policies and get instant, accurate answers
- 🎨 **Modern UI**: Beautiful, responsive chat interface with gradient designs and animations
- 🔍 **Source Attribution**: See which documents were used to generate answers
- 💬 **Chat History**: Persistent conversation history during sessions
- 🔄 **Real-time Status**: Connection status indicator with health monitoring
- 📱 **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- ⚡ **Fast Performance**: Optimized for quick response times

## 🏗️ Architecture

```
HR Chatbot/
├── BE/                 # FastAPI Backend
│   ├── app/
│   │   ├── rag/       # RAG pipeline components
│   │   ├── main.py    # FastAPI application
│   │   └── config.py  # Configuration
│   ├── data/          # Knowledge base documents
│   └── requirements.txt
└── FE/                 # React Frontend
    ├── src/
    │   ├── components/
    │   └── services/
    └── package.json
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Azure OpenAI API access

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd HR-chatbot
```

### 2. Backend Setup

```bash
cd BE
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r req.txt
```

### 3. 🔑 Configure Azure OpenAI Credentials

**⚠️ IMPORTANT: Add Your Own API Credentials**

Create a `.env` file in the `BE` directory:

```bash
cd BE
touch .env  # or create manually
```

Add your Azure OpenAI credentials to `.env`:

```env
OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-01
```

**How to get your credentials:**

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. Go to "Keys and Endpoint" section
4. Copy your API key and endpoint
5. Update the deployment name in `BE/app/rag/llm_service.py` if different from `gpt-35-turbo`

### 4. Frontend Setup

```bash
cd ../FE
npm install
```

### 5. Add Your Knowledge Base

Place your HR policy documents (`.txt` files) in the `BE/data/` directory. The system will automatically load and index these documents.

### 6. Run the Application

**Start Backend (Terminal 1):**
```bash
cd BE
.\venv\Scripts\activate  # Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Start Frontend (Terminal 2):**
```bash
cd FE
npm run dev
```

### 7. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📝 Usage

1. **Ask Questions**: Type HR-related questions in the chat interface
2. **View Sources**: See which documents were used to generate answers
3. **Chat History**: Previous conversations are maintained during your session
4. **Sample Questions**: Click on suggested questions to get started

### Example Questions

- "What is the vacation policy?"
- "How do I request time off?"
- "What are the working hours?"
- "Tell me about the health benefits"

## 🛠️ Configuration

### Backend Configuration (`BE/app/config.py`)

```python
class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
    KNOWLEDGE_BASE_PATH = "data"  # Path to your documents
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

### Frontend Configuration (`FE/src/services/api.js`)

```javascript
const API_BASE_URL = "http://localhost:8000";
```

## 🧪 Testing

### Test Backend Health

```bash
curl http://localhost:8000/health
```

### Test Query Endpoint

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the vacation policy?"}'
```

## 📁 Project Structure

```
BE/
├── app/
│   ├── rag/
│   │   ├── document_loader.py    # Load and process documents
│   │   ├── embedding_service.py  # Text embeddings
│   │   ├── vector_store.py       # Vector database
│   │   ├── retriever.py          # Document retrieval
│   │   ├── llm_service.py        # Azure OpenAI integration
│   │   └── rag_pipeline.py       # Main RAG pipeline
│   ├── main.py                   # FastAPI app
│   ├── config.py                 # Configuration
│   └── schemas.py                # Pydantic models
├── data/                         # Knowledge base documents
└── req.txt                       # Python dependencies

FE/
├── src/
│   ├── components/
│   │   ├── QueryBox.jsx          # Chat input component
│   │   ├── AnswerCard.jsx        # Answer display
│   │   ├── SourcesCard.jsx       # Sources display
│   │   └── ConnectionStatus.jsx  # Backend connection status
│   ├── services/
│   │   └── api.js                # API client
│   ├── App.jsx                   # Main React component
│   └── index.css                 # Styles and animations
└── package.json                  # Node.js dependencies
```

## 🐛 Troubleshooting

### Common Issues

1. **Backend not starting**
   - Check if Python virtual environment is activated
   - Verify all dependencies are installed: `pip install -r req.txt`
   - Check if port 8000 is available

2. **Frontend can't connect to backend**
   - Ensure backend is running on port 8000
   - Check CORS configuration in `main.py`
   - Verify API URL in `api.js`

3. **OpenAI API errors**
   - Verify your API key is correct in `.env`
   - Check Azure OpenAI endpoint URL
   - Ensure deployment name matches in `llm_service.py`

4. **No documents loaded**
   - Place `.txt` files in `BE/data/` directory
   - Check file permissions
   - Restart backend after adding documents

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export LOG_LEVEL=DEBUG  # Linux/macOS
set LOG_LEVEL=DEBUG     # Windows
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔐 Security Notes

- Never commit `.env` files to version control
- Keep API keys secure and rotate regularly
- Use environment variables for all sensitive configurations
- Review documents in the knowledge base for sensitive information

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs in both frontend (browser console) and backend (terminal)
3. Ensure your Azure OpenAI credentials are correctly configured
4. Verify all dependencies are installed

---
