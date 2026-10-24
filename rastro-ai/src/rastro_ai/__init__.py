"""Componentes mínimos de indexação do Rastro AI."""

from .indexing import DocumentChunk, extract_text, chunk_text, index_document
from .document_indexing import IndexDocumentUseCase

__all__ = ["DocumentChunk", "IndexDocumentUseCase", "chunk_text", "extract_text", "index_document"]
