import os
from langchain_core.documents import Document

class DocumentLoader:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def load(self):
        documents = []
        for file in os.listdir(self.base_path):
            if file.endswith(".txt"):
                path = os.path.join(self.base_path, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                year = int(file.split("_")[-1].replace(".txt", "")) if "policy" in file else 0

                documents.append(
                    Document(
                        page_content=content,
                        metadata={
                            "filename": file,
                            "effective_year": year
                        }
                    )
                )
        return documents
