from pathlib import Path

from config.repository_config import knowledge_repository
from models.chunk import Chunk
from services.chunk_service import ChunkService
from services.embedding_service import EmbeddingService
from services.document_loader_service import DocumentLoaderService

class KnowledgeService:
    def __init__(self):
        self.chunk_service = ChunkService()
        self.embedding_service = EmbeddingService()
        self.vector_repository = knowledge_repository
        self.document_loader = DocumentLoaderService()
        self.chunk_id = 1

    def load_knowledge_base(self, folder_path: str) -> int:
        self.vector_repository.clear()
        self.chunk_id = 1
        folder = Path(folder_path)
        for file in folder.iterdir():
            if file.suffix.lower() not in [
                ".txt",
                ".pdf"
            ]:
                continue
            self.load_document(file)
        return self.vector_repository.size()

    def load_document(self, file_path: Path) -> None:
        text = self.document_loader.load(
            file_path
        )
        chunks = self.chunk_service.split(text)
        topic = self.get_topic(file_path.name)
        category = self.get_category(file_path.name)
        language = "English"
        for index, chunk_text in enumerate(chunks, start=1):
            embedding = self.embedding_service.generate(chunk_text)
            chunk = Chunk(
                id=self.chunk_id,
                document_name=file_path.name,
                chunk_index=index,
                topic=topic,
                category=category,
                language=language,
                text=chunk_text,
                embedding=embedding
            )
            self.vector_repository.add(chunk)
            self.chunk_id += 1

    def get_topic(self, file_name: str) -> str:
        name = file_name.lower()
        if "aws" in name:
            return "AWS"

        if "spring" in name:
            return "Spring"

        if "java" in name:
            return "Java"

        if "docker" in name:
            return "Docker"

        return "General"        

    def get_category(self, file_name: str) -> str:
        name = file_name.lower()
        if "aws" in name:
            return "Cloud"

        if "spring" in name:
            return "Backend"

        if "java" in name:
            return "Programming"

        if "docker" in name:
            return "DevOps"

        return "General"