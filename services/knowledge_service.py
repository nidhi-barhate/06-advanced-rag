from pathlib import Path

from config.repository_config import knowledge_repository
from models.chunk import Chunk
from services.chunk_service import ChunkService
from services.embedding_service import EmbeddingService


class KnowledgeService:

    def __init__(self):
        self.chunk_service = ChunkService()
        self.embedding_service = EmbeddingService()
        self.repository = knowledge_repository
        self.chunk_id = 1

    def load_knowledge_base(self, folder_path: str) -> int:
        self.repository.clear()
        self.chunk_id = 1

        folder = Path(folder_path)

        for file in folder.glob("*.txt"):
            self.load_document(file)

        return len(self.repository.find_all())

    def load_document(self, file_path: Path) -> None:

        text = file_path.read_text(encoding="utf-8")

        chunks = self.chunk_service.split(text)

        for index, chunk_text in enumerate(chunks, start=1):

            embedding = self.embedding_service.generate(chunk_text)

            chunk = Chunk(
                id=self.chunk_id,
                document_name=file_path.name,
                chunk_index=index,
                text=chunk_text,
                embedding=embedding
            )

            self.repository.save(chunk)

            self.chunk_id += 1