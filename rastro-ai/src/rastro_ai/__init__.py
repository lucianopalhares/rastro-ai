"""Componentes mínimos de indexação do Rastro AI."""

from .indexing import DocumentChunk, extract_text, chunk_text, index_document, index_document_in_store
from .document_indexing.application.use_cases import IndexDocumentUseCase

__all__ = [
    "DocumentChunk",
    "IndexDocumentUseCase",
    "chunk_text",
    "extract_text",
    "index_document",
    "index_document_in_store",
]
