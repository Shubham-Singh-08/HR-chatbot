from langchain_core.prompts import PromptTemplate
from typing import List
from langchain_core.documents import Document
import re

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
- Give friendly, conversational responses in 2-3 lines
- Focus on current work arrangements and policies
- The information is from the latest HR policy document
- If the question is completely unrelated to work, HR, or company matters, respond: "The question asked is not related to the policy"

Current Company Policy Information:
{context}

Employee Question: {question}

Your Response (based on current HR policy):"""
        )

    def run(self, question: str):
        # Retrieve documents
        docs = self.retriever.retrieve(question)
        
        # Check if we got any documents
        if not docs:
            return "I don't have enough information to answer that question.", [], []
        
        # Build context from retrieved documents
        context_parts = []
        source_files = set()
        
        for doc in docs:
            context_parts.append(doc.page_content)
            filename = doc.metadata.get('filename', 'Unknown')
            source_files.add(filename)
        
        context = "\n\n".join(context_parts)
        
        # If context is empty, return not related
        if not context.strip():
            return "The question asked is not related to the policy", [], []
        
        # Generate response
        response = self.llm.invoke(
            self.prompt.format(context=context, question=question)
        )
        
        # Create sources list with document names and years
        sources = []
        for filename in source_files:
            # Extract year from filename for display
            year_match = re.search(r'(\d{4})', filename)
            if year_match:
                year = year_match.group(1)
                sources.append(f"{filename} ({year})")
            else:
                sources.append(filename)
        
        return response.content, sources, docs
