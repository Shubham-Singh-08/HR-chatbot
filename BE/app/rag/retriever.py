class PolicyRetriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.retriever = vector_store.as_retriever(
            search_kwargs={
                "k": 5  # Get top 5 most relevant chunks
            }
        )

    def retrieve(self, query):
        print(f"🔍 Searching for: '{query}'")
        
        # Get results from similarity search
        results = self.retriever.invoke(query)
        
        if not results:
            print("❌ No documents retrieved from vector store")
            return []
        
        print(f"📄 Retrieved {len(results)} relevant chunks from latest policy")
        
        # Debug: Print retrieved documents with metadata
        for i, doc in enumerate(results):
            filename = doc.metadata.get('filename', 'Unknown')
            doc_type = doc.metadata.get('document_type', 'unknown')
            year = doc.metadata.get('effective_year', 'N/A')
            print(f"  Chunk {i}: {filename} (Type: {doc_type}, Year: {year})")
        
        return results
