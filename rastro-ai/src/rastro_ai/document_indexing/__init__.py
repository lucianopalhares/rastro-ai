"""Módulo DDD responsável pela extração e divisão de documentos."""

from .application.use_cases.index_document import IndexDocumentUseCase
from .domain.entities import DocumentChunk

__all__ = ["DocumentChunk", "IndexDocumentUseCase"]
