import os
import re
from datetime import datetime
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentLoader:
    def __init__(self, base_path: str, chunk_size: int = 1200, chunk_overlap: int = 200):
        self.base_path = base_path
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
            separators=[
                "\n\n",  # Paragraph breaks
                "\n",    # Line breaks
                ". ",    # Sentence breaks
                "? ",    # Question marks
                "! ",    # Exclamation marks
                "; ",    # Semicolons
                ", ",    # Commas
                " ",     # Spaces
                "",      # Characters
            ]
        )

    def _extract_metadata(self, filename: str, content: str) -> dict:
        """Extract metadata from document including policy versioning and document type"""
        metadata = {
            "filename": filename,
            "source": os.path.join(self.base_path, filename)
        }
        
        # Extract year from filename for policy documents
        if "policy" in filename.lower():
            year_match = re.search(r'(\d{4})', filename)
            if year_match:
                metadata["effective_year"] = int(year_match.group(1))
                metadata["document_type"] = "policy"
                metadata["is_current_policy"] = metadata["effective_year"] >= 2024
            
            # Extract policy priority from content
            if "revoked" in content.lower() or "override" in content.lower():
                metadata["policy_action"] = "revocation"
            elif "effective" in content.lower():
                metadata["policy_action"] = "implementation"
                
        elif "menu" in filename.lower() or "cafeteria" in filename.lower():
            metadata["document_type"] = "facility_info"
            metadata["effective_year"] = datetime.now().year
            metadata["is_current_policy"] = False
        else:
            metadata["document_type"] = "general"
            metadata["effective_year"] = 0
            metadata["is_current_policy"] = False
            
        return metadata

    def load(self) -> List[Document]:
        documents = []
        for file in os.listdir(self.base_path):
            if file.endswith(".txt"):
                path = os.path.join(self.base_path, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Extract comprehensive metadata
                metadata = self._extract_metadata(file, content)
                
                # Create document with original metadata
                doc = Document(
                    page_content=content,
                    metadata=metadata
                )
                
                # Split document into chunks
                chunks = self.text_splitter.split_documents([doc])
                
                # Add chunk-specific metadata
                for i, chunk in enumerate(chunks):
                    chunk.metadata.update({
                        "chunk_id": i,
                        "total_chunks": len(chunks),
                        "char_count": len(chunk.page_content),
                        "chunk_source": f"{file}_chunk_{i}"
                    })
                    documents.append(chunk)
                    
        return documents
