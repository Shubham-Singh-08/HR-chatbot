from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import QueryRequest, QueryResponse, RetrievedDoc
from app.rag.document_loader import DocumentLoader
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore
from app.rag.retriever import PolicyRetriever
from app.rag.llm_service import OpenAiLLM
from app.rag.rag_pipeline import RAGPipeline
from app.config import settings

app = FastAPI(title="TechCorp HR RAG")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://127.0.0.1:3001"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup
loader = DocumentLoader(settings.KNOWLEDGE_BASE_PATH)
documents = loader.load()

print(f"📚 Loaded {len(documents)} document chunks:")
for doc in documents:
    filename = doc.metadata.get('filename', 'Unknown')
    doc_type = doc.metadata.get('document_type', 'unknown')
    year = doc.metadata.get('effective_year', 'N/A')
    print(f"  - {filename} (Type: {doc_type}, Year: {year}) - Content: {doc.page_content[:50]}...")

# Force delete old vector store
import shutil
try:
    shutil.rmtree(settings.CHROMA_PERSIST_DIR)
    print(f"🗑️ Deleted old vector store: {settings.CHROMA_PERSIST_DIR}")
except:
    print(f"📁 No existing vector store found")

embedding = EmbeddingService().get()
vector_store_service = VectorStore(embedding)
vector_db = vector_store_service.create(documents)

print(f"✅ Fresh vector store created with {len(documents)} documents")

retriever = PolicyRetriever(vector_db)
llm = OpenAiLLM().get()
pipeline = RAGPipeline(retriever, llm)

@app.get("/")
def health_check():
    return {"status": "OK", "message": "TechCorp HR RAG API is running"}

@app.get("/health")
def health():
    return {"status": "healthy", "documents_loaded": len(documents)}

@app.get("/debug")
def debug_retrieval():
    """Debug endpoint to test document retrieval"""
    test_query = "can I work remote"
    retrieved_docs = retriever.retrieve(test_query)
    
    debug_info = {
        "query": test_query,
        "total_documents": len(documents),
        "retrieved_count": len(retrieved_docs),
        "retrieved_docs": [
            {
                "filename": doc.metadata.get("filename"),
                "type": doc.metadata.get("document_type"),
                "year": doc.metadata.get("effective_year"),
                "content_preview": doc.page_content[:100] + "..."
            } for doc in retrieved_docs
        ]
    }
    return debug_info

@app.get("/verify-vectorization")
def verify_vectorization():
    """Comprehensive verification of knowledge base vectorization"""
    
    # Check source files in knowledge base
    kb_files = []
    import os
    kb_path = settings.KNOWLEDGE_BASE_PATH
    if os.path.exists(kb_path):
        kb_files = [f for f in os.listdir(kb_path) if f.endswith('.txt')]
    
    # Analyze loaded documents
    file_analysis = {}
    for doc in documents:
        filename = doc.metadata.get('filename', 'unknown')
        if filename not in file_analysis:
            file_analysis[filename] = {
                'chunks': 0,
                'total_chars': 0,
                'document_type': doc.metadata.get('document_type', 'unknown'),
                'effective_year': doc.metadata.get('effective_year', 'N/A'),
                'sample_content': doc.page_content[:150] + '...'
            }
        file_analysis[filename]['chunks'] += 1
        file_analysis[filename]['total_chars'] += len(doc.page_content)
    
    # Test vector store retrieval
    test_queries = [
        "work from home",
        "remote work", 
        "office policy",
        "Friday cafeteria"
    ]
    
    retrieval_tests = {}
    for query in test_queries:
        try:
            results = retriever.retrieve(query)
            retrieval_tests[query] = {
                'found_docs': len(results),
                'sources': [doc.metadata.get('filename') for doc in results]
            }
        except Exception as e:
            retrieval_tests[query] = {'error': str(e)}
    
    verification_result = {
        "status": "vectorization_check",
        "knowledge_base_files": kb_files,
        "files_processed": list(file_analysis.keys()),
        "total_chunks_created": len(documents),
        "file_details": file_analysis,
        "all_files_vectorized": set(kb_files) == set(file_analysis.keys()),
        "retrieval_tests": retrieval_tests,
        "vector_store_stats": {
            "total_documents_in_db": len(documents),
            "vectorization_complete": len(documents) > 0
        }
    }
    
    return verification_result

@app.post("/query", response_model=QueryResponse)
def query_policy(req: QueryRequest):
    try:
        answer, sources, docs = pipeline.run(req.question)

        retrieved = [
            RetrievedDoc(
                filename=doc.metadata.get('filename', 'Unknown'),
                score=1.0
            ) for doc in docs
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
