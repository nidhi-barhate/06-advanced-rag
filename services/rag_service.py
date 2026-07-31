from services.retrieval_service import RetrievalService
from services.prompt_builder_service import PromptBuilderService
from services.llm_service import LLMService


class RAGService:

    def __init__(self):

        self.retrieval_service = RetrievalService()

        self.prompt_builder = PromptBuilderService()

        self.llm_service = LLMService()

    def ask(self, question: str):
        search_results = self.retrieval_service.retrieve(question)
        prompt = self.prompt_builder.build(
            question=question,
            search_results=search_results
        )
        answer = self.llm_service.chat(
            prompt=prompt,
            new_chat=True
        )
        return answer