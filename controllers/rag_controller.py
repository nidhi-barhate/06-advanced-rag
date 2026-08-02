from fastapi import APIRouter,Depends
from requests import Session

from services.knowledge_service import KnowledgeService
from config.repository_config import knowledge_repository
from schemas.search_request import SearchRequest
from services.retrieval_service import RetrievalService
from services.rag_service import RAGService
from config.dependencies import get_db

router = APIRouter()


@router.post("/api/knowledge/load")
def load_knowledge(db : Session = Depends(get_db)):
    knowledge_service = KnowledgeService(db)
    total_chunks = knowledge_service.load_knowledge_base("knowledge")
    return {
        "message": "Knowledge base loaded successfully.",
        "total_chunks": total_chunks
    }

@router.get("/api/knowledge/chunks")
def get_chunks():
    return knowledge_repository.find_all()

@router.post("/api/knowledge/search")
def search(request: SearchRequest, db: Session = Depends(get_db)):
    retrieval_service = RetrievalService(db)
    return retrieval_service.retrieve(request.question)

@router.post("/api/rag/ask")
def ask(request: SearchRequest, db: Session = Depends(get_db)):
    rag_service = RAGService(db)
    return rag_service.ask(
        request.question
    )