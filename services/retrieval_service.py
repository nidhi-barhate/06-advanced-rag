from schemas.search_result import SearchResult
from services.embedding_service import EmbeddingService
from utils.similarity import Similarity
from config.repository_config import knowledge_repository

class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_repository = knowledge_repository

    def retrieve(self, question: str, top_k: int = 3):
        query_embedding = self.embedding_service.generate(question)
        results = []
        results = self.vector_repository.search(
            query_embedding=query_embedding,
            top_k=top_k
        )
        search_results = []
        for score, chunk in results:
            search_results.append(
                SearchResult(
                    document_name=chunk.document_name,
                    text=chunk.text,
                    score=score
                )
            )
        return search_results