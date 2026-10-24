"""Fachada legada para o módulo DDD de indexação de documentos."""

from __future__ import annotations

from pathlib import Path
from .document_indexing.application.use_cases.index_document import IndexDocumentUseCase
from .document_indexing.domain.entities import DocumentChunk
from .document_indexing.infrastructure.extraction.utf8_file_text_extractor import (
    Utf8FileTextExtractor,
)

_index_document = IndexDocumentUseCase(Utf8FileTextExtractor())


def extract_text(path: str | Path) -> str:
    """Mantém a API legada enquanto delega a leitura ao adaptador de infraestrutura."""

    return Utf8FileTextExtractor().extract(path)


def chunk_text(
    text: str,
    *,
    document_id: str,
    chunk_size: int = 800,
    overlap: int = 120,
) -> tuple[DocumentChunk, ...]:
    """Mantém a API legada enquanto delega a política ao serviço de domínio."""

    from .document_indexing.domain.services import chunk_text as domain_chunk_text

    return domain_chunk_text(
        text,
        document_id=document_id,
        chunk_size=chunk_size,
        overlap=overlap,
    )


def index_document(
    document_id: str,
    path: str | Path,
    *,
    chunk_size: int = 800,
    overlap: int = 120,
) -> tuple[DocumentChunk, ...]:
    """Extrai um arquivo e gera seus chunks em uma única operação determinística."""

    return _index_document.execute(
        document_id,
        path,
        chunk_size=chunk_size,
        overlap=overlap,
    )
