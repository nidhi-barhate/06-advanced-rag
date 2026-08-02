from requests import Session

from models.chat_model import Message
from models.source import Source
from schemas.search_result import SearchResult
from services.embedding_service import EmbeddingService
from services.keyword_search_service import KeywordSearchService
from services.query_rewrite_service import QueryRewriteService
from config.repository_config import knowledge_repository
from services.rerank_service import ReRankService
from repository.message_repository import MessageRepository
from sqlalchemy.orm import Session

class RetrievalService:
    def __init__(self, db: Session):
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
        search_results = self.rerank_service.rerank(
            question,
            final_results
        )
        return search_results