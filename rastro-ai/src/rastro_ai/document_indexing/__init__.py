"""Módulo DDD responsável pela extração e divisão de documentos."""

from .application.use_cases.extract_and_chunk_document import ExtractAndChunkDocumentUseCase
from .domain.entities import DocumentChunk

__all__ = ["DocumentChunk", "ExtractAndChunkDocumentUseCase"]
