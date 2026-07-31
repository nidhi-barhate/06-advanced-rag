from pydantic import BaseModel

class Chunk(BaseModel):
    id: int
    document_name: str
    chunk_index: int
    topic: str
    category: str
    language: str
    text: str
    embedding: list[float]