from services.prompt_builder_service import PromptBuilderService
from services.llm_service import LLMService

class QueryRewriteService:
    def __init__(self):
        self.prompt_builder = PromptBuilderService()
        self.llm_service = LLMService()

    def rewrite(
            self,
            history: str,
            question: str
    ) -> str:
        prompt = self.prompt_builder.build_query_rewrite_prompt(
            history=history,
            question=question
        )
        rewritten = self.llm_service.chat(
            prompt
        )
        return rewritten.strip()