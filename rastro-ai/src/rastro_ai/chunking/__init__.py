"""Políticas de normalização e divisão de documentos."""

from .domain.chunker import chunk_text, normalize_text

__all__ = ["chunk_text", "normalize_text"]
