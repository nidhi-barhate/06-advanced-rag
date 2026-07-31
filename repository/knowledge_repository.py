from models.chunk import Chunk

class KnowledgeRepository:

    def __init__(self):
        self.chunks: list[Chunk] = []

    def save(self, chunk: Chunk):
        self.chunks.append(chunk)

    def find_all(self):
        return self.chunks

    def clear(self):
        self.chunks.clear()