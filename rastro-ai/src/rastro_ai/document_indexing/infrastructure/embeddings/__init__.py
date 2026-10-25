"""Adaptadores de embeddings usados pela indexação semântica."""

from .openai_embedding_repository import OpenAIEmbeddingRepository
from .sentence_transformer import SentenceTransformerEmbeddingProvider

__all__ = ["OpenAIEmbeddingRepository", "SentenceTransformerEmbeddingProvider"]
