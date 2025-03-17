from typing import List

from FlagEmbedding import BGEM3FlagModel
from langchain_qdrant import SparseEmbeddings, SparseVector


class BGEM3SparseEmbeddings(SparseEmbeddings):

    def __init__(self, **kwargs):
        self.model = BGEM3FlagModel("BAAI/bge-m3", **kwargs)

    def embed_documents(self, texts: List[str]) -> List[SparseVector]:
        embeddings = self.model.encode(
            texts, return_dense=False, return_sparse=True, return_colbert_vecs=False
        )

        sparse_embeddings = embeddings["lexical_weights"]

        return [
            SparseVector(indices=list(emb.keys()), values=list(emb.values()))
            for emb in sparse_embeddings
        ]

    def embed_query(self, text: str) -> SparseVector:
        return self.embed_documents([text])[0]
