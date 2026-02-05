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
        policy_files = []
        
        # First, collect all policy files and sort by year
        for file in os.listdir(self.base_path):
            if file.endswith(".txt") and "policy" in file.lower():
                year_match = re.search(r'(\d{4})', file)
                if year_match:
                    year = int(year_match.group(1))
                    policy_files.append((file, year))
        
        # Sort by year (newest first) and only keep the latest policy
        policy_files.sort(key=lambda x: x[1], reverse=True)
        
        if not policy_files:
            print("❌ No policy files found in knowledge base!")
            return documents
        
        # Only load the latest policy file
        latest_policy_file, latest_year = policy_files[0]
        print(f"📋 Loading only the latest policy: {latest_policy_file} ({latest_year})")
        
        # Skip older policies
        if len(policy_files) > 1:
            skipped_files = [f"{file} ({year})" for file, year in policy_files[1:]]
            print(f"⏭️ Skipping older policies: {', '.join(skipped_files)}")
        
        # Load only the latest policy file
        path = os.path.join(self.base_path, latest_policy_file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract comprehensive metadata
        metadata = self._extract_metadata(latest_policy_file, content)
        metadata["is_latest_policy"] = True
        
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
                "chunk_source": f"{latest_policy_file}_chunk_{i}",
                "is_latest_policy": True
            })
            documents.append(chunk)
        
        print(f"✅ Loaded {len(documents)} chunks from latest policy: {latest_policy_file}")
        return documents
