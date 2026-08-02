from models.source import Source
from schemas.search_result import SearchResult
from services.embedding_service import EmbeddingService
from services.keyword_search_service import KeywordSearchService
from utils.similarity import Similarity
from config.repository_config import knowledge_repository
from services.rerank_service import ReRankService

class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_repository = knowledge_repository
        self.keyword_search_service = KeywordSearchService()
        self.rerank_service = ReRankService()

    def retrieve(self, question: str, top_k: int = 3):
        merged = {}
        keyword_results = self.keyword_search_service.search(
            question=question,
            top_k=top_k
        )
        query_embedding = self.embedding_service.generate(question)
        results = []
        results = self.vector_repository.search(
            query_embedding=query_embedding,
            top_k=top_k
        )
        semantic_results = []
        for score, chunk in results:
            semantic_results.append(
                SearchResult(
                    document_name=chunk.document_name,
                    text=chunk.text,
                    score=score
                )
            )
        for result in keyword_results:
            if result.document_name not in merged:
                merged[result.document_name] = result
            else:
                merged[result.document_name].score += result.score
        
        final_results = list(merged.values())
        final_results.sort(
            key=lambda result: result.score,
            reverse=True
        )
        print(f"Final results before reranking: {[result.document_name for result in final_results]}")
        search_results = self.rerank_service.rerank(
            question,
            final_results
        )
        print(f"Final results after reranking: {[result.document_name for result in search_results]}")
        return search_results