from langchain_openai import AzureChatOpenAI
from app.config import settings

class OpenAiLLM:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            deployment_name="gpt-35-turbo",
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_version=settings.AZURE_OPENAI_API_VERSION,
            temperature=0
        )

    def get(self):
        return self.llm
