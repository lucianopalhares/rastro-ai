"""Componentes mínimos de indexação do Rastro AI."""

from .indexing import (
    DocumentChunk,
    chunk_text,
    extract_and_chunk_document,
    extract_text,
    extract_chunk_and_persist_document,
)
from .document_indexing.application.use_cases import ExtractAndChunkDocumentUseCase

__all__ = [
    "DocumentChunk",
    "ExtractAndChunkDocumentUseCase",
    "chunk_text",
    "extract_and_chunk_document",
    "extract_text",
    "extract_chunk_and_persist_document",
]
