import faiss
import numpy as np

from models.chunk import Chunk


class VectorRepository:
    def __init__(self):
        self.index = None
        self.chunk_map: dict[int, Chunk] = {}
        self.dimension = None

    def add(self, chunk: Chunk) -> None:
        """
        Add a chunk and its embedding to the FAISS index.
        """

        # Initialize FAISS index on first insert
        if self.index is None:
            self.dimension = len(chunk.embedding)
            self.index = faiss.IndexFlatIP(self.dimension)

        vector = np.array(
            [chunk.embedding],
            dtype=np.float32
        )

        # Normalize for cosine similarity
        faiss.normalize_L2(vector)

        self.index.add(vector)

        # FAISS assigns vector IDs sequentially
        vector_id = self.index.ntotal - 1
        print(self.index.ntotal)
        print(f"Adding chunk: {chunk.document_name}")
        print(f"Embedding length: {len(chunk.embedding)}")

        self.chunk_map[vector_id] = chunk

    def search(
            self,
            query_embedding: list[float],
            top_k: int = 3
    ) -> list[tuple[float, Chunk]]:
        """
        Search the most similar chunks.
        """
        print("Searching...")

        print("FAISS size:", self.size())

        print("Top K:", top_k)

        if self.index is None:
            return []

        query = np.array(
            [query_embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(query)

        scores, indices = self.index.search(
            query,
            top_k
        )
        print(scores)
        print(indices)

        results = []

        for score, vector_id in zip(scores[0], indices[0]):

            if vector_id == -1:
                continue

            chunk = self.chunk_map.get(vector_id)

            if chunk is not None:
                results.append(
                    (
                        float(score),
                        chunk
                    )
                )

        return results

    def clear(self) -> None:
        """
        Clear the FAISS index and all stored chunks.
        """

        self.index = None
        self.chunk_map.clear()
        self.dimension = None

    def size(self) -> int:
        """
        Return the number of indexed vectors.
        """

        if self.index is None:
            return 0

        return self.index.ntotal