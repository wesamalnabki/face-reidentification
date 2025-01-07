import os
from typing import List

import chromadb
import numpy as np
from chromadb import EmbeddingFunction, Embeddings
from chromadb.utils.data_loaders import ImageLoader

from backend.src.face_process_model import FaceProcess

__all__ = [
    'FaceEmbeddingFunction',
    'VectorDBManager'
]


class FaceEmbeddingFunction(EmbeddingFunction):

    def __init__(self):
        self.face_processor = FaceProcess()

    def __call__(self, image_np: List[np.array]) -> Embeddings:
        return [self.face_processor.get_face_embedding(i) for i in image_np]


class VectorDBManager:
    def __init__(self):
        # Initialize Chroma client
        data_loader = ImageLoader()
        ef = FaceEmbeddingFunction()
        chroma_client = chromadb.PersistentClient(path=os.getenv("CHROMA_DB_PATH"))

        self._collection = chroma_client.get_or_create_collection(name=os.getenv("CHROMA_COLLECTION_NAME"),
                                                                  embedding_function=ef,
                                                                  data_loader=data_loader,
                                                                  metadata={"hnsw:space": "cosine"})
        print("Vector DB rows count:", self._collection.count())

    def query_db(self, image_pil):
        image_np = np.array(image_pil)
        return self._collection.query(
            query_images=[image_np],
            n_results=int(os.getenv("TOP_MATCH_COUNT"))
        )

    def upsert_db(self, face_id, image_pil):
        image_np = np.array(image_pil)
        self._collection.upsert(
            ids=[face_id],
            images=[image_np]
        )
