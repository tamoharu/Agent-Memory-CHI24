import os
import faiss
import numpy


class Faiss:
    def __init__(self, dimension: int, index_path: str, index_type: str='IndexFlatL2'):
        self.dimension = dimension
        self.index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../assets/{index_path}'))
        self.index_type = index_type
        self.index = None
        if os.path.exists(self.index_path):
            self._load_index()
        else:
            self._create_index()

    def add_embeddings(self, embedding: numpy.ndarray , id: int) -> None:
        embedding_np = numpy.array([embedding], dtype=numpy.float32)
        embedding_np /= numpy.linalg.norm(embedding_np)
        id_np = numpy.array([id], dtype=numpy.int64)
        self.index.add_with_ids(embedding_np, id_np) #type: ignore
        self.save_index()

    def search_embeddings(self, query_vector: numpy.ndarray, threshold: float, exclude_ids: list) -> list:
        query_vector = numpy.array([query_vector], dtype=numpy.float32)
        query_vector /= numpy.linalg.norm(query_vector)
        distances, indices = self.index.search(query_vector, self.index.ntotal) #type: ignore
        distances, indices = distances[0], indices[0]
        indices = [int(i) for i in indices]
        distances = [float(d) for d in distances]
        results = [(d, i) for d, i in zip(distances, indices) if d >= threshold and i not in exclude_ids]
        return results

    def save_index(self) -> None:
        faiss.write_index(self.index, self.index_path)

    def delete_index(self) -> None:
        os.remove(self.index_path)

    def _create_index(self) -> None:
        index_flat_l2 = faiss.IndexFlatIP(self.dimension)
        index = faiss.IndexIDMap(index_flat_l2)
        self.index = index

    def _load_index(self) -> None:
        self.index = faiss.read_index(self.index_path)