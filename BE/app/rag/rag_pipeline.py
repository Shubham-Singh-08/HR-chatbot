from langchain_core.prompts import PromptTemplate
from typing import List
from langchain_core.documents import Document

class RAGPipeline:
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm

        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are TechCorp's helpful HR assistant. Answer based on the CURRENT company policies provided below.

IMPORTANT GUIDELINES:
- Use ONLY the most recent and current information from the context
- The information provided is already filtered to show current policies
- Give friendly, conversational responses in 2-3 lines
- Focus on current work arrangements and policies
- If the question is completely unrelated to work, HR, or company matters, respond: "The question asked is not related to the policy"

Current Company Information:
{context}

Employee Question: {question}

Your Response (based on current policies):"""
        )

    def _filter_and_rank_documents(self, docs: List[Document], question: str) -> List[Document]:
        """Filter out noise and rank documents by relevance and recency"""
        # Separate documents by type
        policy_docs = []
        other_docs = []
        
        for doc in docs:
            doc_type = doc.metadata.get("document_type", "general")
            if doc_type == "policy":
                policy_docs.append(doc)
            else:
                other_docs.append(doc)
        
        # For policy questions, prioritize policy documents  
        policy_keywords = ["work", "remote", "office", "policy", "can i", "allow", "home", "wfh", "working"]
        is_policy_query = any(keyword in question.lower() for keyword in policy_keywords)
        
        if is_policy_query and policy_docs:
            # Sort policy docs by effective year (most recent first)
            policy_docs.sort(key=lambda x: x.metadata.get("effective_year", 0), reverse=True)
            
            # CRITICAL: Only keep the most recent policy, completely ignore older ones
            if len(policy_docs) > 1:
                most_recent_year = policy_docs[0].metadata.get("effective_year", 0)
                # Keep ONLY documents from the most recent year (2024)
                policy_docs = [doc for doc in policy_docs 
                             if doc.metadata.get("effective_year", 0) == most_recent_year]
            
            # For policy questions, use ONLY current policy documents
            filtered_docs = policy_docs  # No mixing with other documents
        else:
            # For non-policy questions, include all relevant docs
            filtered_docs = policy_docs + other_docs
        
        return filtered_docs[:3]  # Limit to top 3 most relevant documents

    def run(self, question: str):
        # Retrieve documents
        raw_docs = self.retriever.retrieve(question)
        
        # Check if we got any documents
        if not raw_docs:
            return "I don't have enough information to answer that question.", [], []
        
        # Apply intelligent filtering and ranking
        filtered_docs = self._filter_and_rank_documents(raw_docs, question)
        
        # If no documents after filtering, return not related message
        if not filtered_docs:
            return "The question asked is not related to the policy", [], []
        
        # Build context without filename metadata
        context_parts = []
        for doc in filtered_docs:
            # Just use the content without metadata headers
            context_parts.append(doc.page_content)
        
        context = "\n\n".join(context_parts)
        
        # If context is empty, return not related
        if not context.strip():
            return "The question asked is not related to the policy", [], []
        
        # Generate response
        response = self.llm.invoke(
            self.prompt.format(context=context, question=question)
        )
        
        # Return just the answer content and empty sources list
        return response.content, [], filtered_docs
