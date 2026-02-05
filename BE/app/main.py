from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import QueryRequest, QueryResponse, RetrievedDoc
from app.rag.document_loader import DocumentLoader
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore
from app.rag.retriever import PolicyRetriever
from app.rag.llm_service import GeminiLLM
from app.rag.rag_pipeline import RAGPipeline
from app.config import settings

app = FastAPI(title="TechCorp HR RAG")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup
loader = DocumentLoader(settings.KNOWLEDGE_BASE_PATH)
documents = loader.load()

embedding = EmbeddingService().get()
vector_store_service = VectorStore(embedding)
vector_db = vector_store_service.create(documents)

retriever = PolicyRetriever(vector_db)
llm = GeminiLLM().get()
pipeline = RAGPipeline(retriever, llm)

@app.get("/")
def health_check():
    return {"status": "OK", "message": "TechCorp HR RAG API is running"}

@app.get("/health")
def health():
    return {"status": "healthy", "documents_loaded": len(documents)}

@app.post("/query", response_model=QueryResponse)
def query_policy(req: QueryRequest):
    try:
        answer, sources, docs = pipeline.run(req.question)

        retrieved = [
            RetrievedDoc(
                filename=d.metadata["filename"],
                score=1.0
            ) for d in docs
        ]

        return QueryResponse(
            answer=answer,
            sources=sources,
            retrieved_documents=retrieved
        )
    except Exception as e:
        return QueryResponse(
            answer=f"I apologize, but I encountered an error while processing your question: {str(e)}",
            sources=[],
            retrieved_documents=[]
        )
