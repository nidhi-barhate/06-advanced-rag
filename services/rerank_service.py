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
            print("=" * 60)
            print("Question:", question)
            print("Document:", result.document_name)
            print("LLM Score:", result.score)    
            
        search_results.sort(
            key=lambda item: item.score,
            reverse=True
        )
        return search_results