"""Entidades e serviços puros do módulo de indexação."""

from .entities import DocumentChunk
from .services import chunk_text, normalize_text

__all__ = ["DocumentChunk", "chunk_text", "normalize_text"]
