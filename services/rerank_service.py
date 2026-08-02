from services.prompt_builder_service import PromptBuilderService
from services.llm_service import LLMService
from schemas.search_result import SearchResult

class ReRankService:
    def __init__(self):
        self.prompt_builder = PromptBuilderService()
        self.llm_service = LLMService()

    def rerank(
            self,
            question: str,
            search_results: list[SearchResult]
    ) -> list[SearchResult]:
        for result in search_results:
            prompt = self.prompt_builder.build_rerank_prompt(
                question=question,
                document=result.text
            )
            response = self.llm_service.chat(prompt)
            try:
                result.score = float(response.strip())
            except ValueError:
                result.score = 0 
        search_results.sort(
            key=lambda item: item.score,
            reverse=True
        )
        MIN_SCORE = 5
        results = [
            result
            for result in search_results
            if result.score >= MIN_SCORE
        ]
        return results