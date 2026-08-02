from models.source import Source
from repository.message_repository import MessageRepository
from schemas.chat_response import ChatResponse
from services.query_rewrite_service import QueryRewriteService
from services.retrieval_service import RetrievalService
from services.prompt_builder_service import PromptBuilderService
from services.llm_service import LLMService
from sqlalchemy.orm import Session
from models.chat_model import Message

class RAGService:
    def __init__(self, db: Session):
        self.retrieval_service = RetrievalService(db)
        self.prompt_builder = PromptBuilderService()
        self.llm_service = LLMService()
        self.message_repository = MessageRepository(db)
        self.query_rewrite_service = QueryRewriteService()

    def ask(self, question: str):
        question_message_model = Message(role="user", content=question)
        self.message_repository.save(question_message_model)
        history = self.message_repository.history_as_text()
        rewritten_question = self.query_rewrite_service.rewrite(
            history=history,
            question=question
        )
        search_results = self.retrieval_service.retrieve(rewritten_question)
        prompt = self.prompt_builder.build(
            question=rewritten_question,
            search_results=search_results
        )
        answer = self.llm_service.chat(
            prompt=prompt,
            new_chat=True
        )
        answer_message_model = Message(role="assistant", content=answer)
        self.message_repository.save(answer_message_model)
        sources = []
        for result in search_results:
            sources.append(
                Source(
                    document_name=result.document_name,
                    score=result.score
                )
            )
        return ChatResponse(answer=answer, 
                            sources=sources)