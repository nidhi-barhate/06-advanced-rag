from config.repository_config import knowledge_repository
from schemas.search_result import SearchResult
from services.embedding_service import EmbeddingService
from utils.similarity import Similarity


class RetrievalService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.repository = knowledge_repository

    def retrieve(self, question: str, top_k: int = 3):
        query_embedding = self.embedding_service.generate(question)
        results = []
        for chunk in self.repository.find_all():
            score = Similarity.cosine(
                query_embedding,
                chunk.embedding
            )
            results.append((score, chunk))
        results.sort(
            key=lambda item: item[0],
            reverse=True
        )

        search_results = []
        for score, chunk in results[:top_k]:

            search_results.append(
                SearchResult(
                    document_name=chunk.document_name,
                    text=chunk.text,
                    score=score
                )
            )
        return search_results