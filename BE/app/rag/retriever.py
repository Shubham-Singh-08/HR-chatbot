class PolicyRetriever:
    def __init__(self, vector_store):
        # Use more lenient retrieval settings
        self.vector_store = vector_store
        self.retriever = vector_store.as_retriever(
            search_kwargs={
                "k": 10  # Get more documents for better coverage
            }
        )

    def retrieve(self, query):
        print(f"🔍 DEBUGGING RETRIEVAL for query: '{query}'")
        
        # Get initial results from similarity search
        raw_results = self.retriever.invoke(query)
        print(f"📄 Retrieved {len(raw_results)} raw documents")
        
        # Define work-related keywords
        work_keywords = ["work", "remote", "office", "home", "wfh", "working", "policy", "can i", "allow"]
        
        # If still no results, return empty
        if not raw_results:
            print("❌ No documents retrieved from vector store")
            return []
        
        # Debug: Print all retrieved documents with metadata
        for i, doc in enumerate(raw_results):
            filename = doc.metadata.get('filename', 'Unknown')
            doc_type = doc.metadata.get('document_type', 'unknown')
            year = doc.metadata.get('effective_year', 'N/A')
            print(f"  Doc {i}: {filename} (Type: {doc_type}, Year: {year})")
        
        # Apply filtering for policy conflicts
        policy_docs = []
        non_policy_docs = []
        
        for doc in raw_results:
            doc_type = doc.metadata.get("document_type", "general")
            if doc_type == "policy":
                policy_docs.append(doc)
            else:
                non_policy_docs.append(doc)
        
        print(f"📋 Found {len(policy_docs)} policy docs, {len(non_policy_docs)} non-policy docs")
        
        # Check for policy-related queries
        is_policy_query = any(keyword in query.lower() for keyword in work_keywords)
        print(f"🏢 Is policy query: {is_policy_query}")
        
        if is_policy_query and policy_docs:
            # Sort by year (most recent first)
            policy_docs.sort(key=lambda x: x.metadata.get("effective_year", 0), reverse=True)
            
            print(f"📅 Policy docs after sorting:")
            for doc in policy_docs:
                year = doc.metadata.get('effective_year', 'N/A')
                filename = doc.metadata.get('filename', 'Unknown')
                print(f"    - {filename} (Year: {year})")
            
            # STRICT PRIORITIZATION: Only return 2024 policy for work queries
            current_policies = [doc for doc in policy_docs 
                             if doc.metadata.get("effective_year", 0) >= 2024]
            
            print(f"🎯 Filtered to 2024+ policies: {len(current_policies)} documents")
            for doc in current_policies:
                filename = doc.metadata.get('filename', 'Unknown')
                year = doc.metadata.get('effective_year', 'N/A')
                print(f"    - SELECTED: {filename} (Year: {year})")
            
            if current_policies:
                # Only return 2024+ policies, completely ignore older ones
                final_result = current_policies[:3]
                print(f"✅ Returning {len(final_result)} current policy documents")
                return final_result
            else:
                # Fallback if no 2024 policies found (shouldn't happen)
                print(f"⚠️ No 2024+ policies found, returning most recent")
                return policy_docs[:1]
        
        # For non-policy queries, return mixed results but still prioritize recent
        if policy_docs:
            policy_docs.sort(key=lambda x: x.metadata.get("effective_year", 0), reverse=True)
        
        final_mix = (policy_docs[:2] + non_policy_docs[:2])[:3]
        print(f"🔄 Returning {len(final_mix)} mixed documents for non-policy query")
        return final_mix
