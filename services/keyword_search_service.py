from config.repository_config import knowledge_repository
from schemas.search_result import SearchResult

class KeywordSearchService:
    def __init__(self):
        self.vector_repository = knowledge_repository
    def search(
            self,
            question: str,
            top_k: int = 3
    ) -> list[SearchResult]:
        keywords = question.lower().split()
        results = []
        for chunk in self.vector_repository.find_all():
            score = 0
            text = chunk.text.lower()
            for keyword in keywords:
                if keyword in text:
                    score += 1
            if score > 0:
                results.append(
                    SearchResult(
                        document_name=chunk.document_name,
                        text=chunk.text,
                        score=float(score)
                    )
                )
        results.sort(
            key=lambda result: result.score,
            reverse=True
        )
        return results[:top_k]