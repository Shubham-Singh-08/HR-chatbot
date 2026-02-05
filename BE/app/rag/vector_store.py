from langchain_community.vectorstores import Chroma
from app.config import settings

class VectorStore:
    def __init__(self, embedding):
        self.embedding = embedding

    def create(self, documents):
        return Chroma.from_documents(
            documents,
            self.embedding,
            persist_directory=settings.CHROMA_PERSIST_DIR
        )

    def load(self):
        return Chroma(
            persist_directory=settings.CHROMA_PERSIST_DIR,
            embedding_function=self.embedding
        )
    
    def create_with_search_config(self, documents):
        """Create vector store with optimized search configuration"""
        vectorstore = Chroma.from_documents(
            documents,
            self.embedding,
            persist_directory=settings.CHROMA_PERSIST_DIR
        )
        
        # Configure for better retrieval of policy documents
        return vectorstore
