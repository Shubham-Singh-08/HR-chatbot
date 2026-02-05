import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    CHROMA_PERSIST_DIR = "chroma_db"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    KNOWLEDGE_BASE_PATH = "knowledge_base"  # Updated to use knowledge_base folder

settings = Settings()
