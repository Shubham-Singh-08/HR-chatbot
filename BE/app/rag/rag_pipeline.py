from langchain_core.prompts import PromptTemplate

class RAGPipeline:
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm

        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are an HR policy assistant.

Rules:
- Answer ONLY from the context.
- If policies conflict, prefer the most recent policy.
- Always cite the policy filename.
- Ignore irrelevant documents.

Context:
{context}

Question:
{question}

Answer:
"""
        )

    def run(self, question):
        docs = self.retriever.retrieve(question)

        context = "\n\n".join(
            f"[{d.metadata['filename']}]\n{d.page_content}" for d in docs
        )

        response = self.llm.invoke(
            self.prompt.format(context=context, question=question)
        )

        sources = list({d.metadata["filename"] for d in docs})

        return response.content, sources, docs
