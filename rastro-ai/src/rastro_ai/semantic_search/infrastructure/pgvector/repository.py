"""Repository pgvector exposto pelo limite modular de busca semântica."""

from ....document_indexing.infrastructure.retrieval.postgres_vector_store import (
    PostgresVectorStore,
)

__all__ = ["PostgresVectorStore"]
