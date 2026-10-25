"""Contrato modular para o chunking estrutural de documentos."""

from ...document_indexing.domain.services import chunk_text, normalize_text

__all__ = ["chunk_text", "normalize_text"]
