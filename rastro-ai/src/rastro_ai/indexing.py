"""Fachada legada para o módulo DDD de indexação de documentos."""

from __future__ import annotations

from pathlib import Path
from .documents.domain.entities import DocumentChunk
from .document_ingestion.application.use_cases.index_document import IndexDocumentUseCase
from .document_ingestion.infrastructure.extraction.utf8_file_text_extractor import (
    Utf8FileTextExtractor,
)

_index_document = IndexDocumentUseCase(Utf8FileTextExtractor())


def extract_text(path: str | Path) -> str:
    """Mantém a API legada enquanto delega a leitura ao adaptador de infraestrutura."""

    return Utf8FileTextExtractor().extract(path)


# /**
#  * Mantém a fachada legada e propaga o projeto para os chunks produzidos.
#  * Histórico: v1 — adiciona `project_id` para integração com retrieval.
#  * Histórico: v2 — expõe orçamento de tokens do chunking estrutural.
#  */
def chunk_text(
    text: str,
    *,
    document_id: str,
    project_id: str = "",
    chunk_size: int | None = None,
    overlap: int | None = None,
    max_tokens: int = 500,
    overlap_tokens: int = 60,
) -> tuple[DocumentChunk, ...]:
    """Mantém a API legada enquanto delega a política ao serviço de domínio."""

    from .chunking.domain.chunker import chunk_text as domain_chunk_text

    return domain_chunk_text(
        text,
        document_id=document_id,
        project_id=project_id,
        chunk_size=chunk_size,
        overlap=overlap,
        max_tokens=max_tokens,
        overlap_tokens=overlap_tokens,
    )


# /**
#  * Mantém a indexação de arquivo e permite associar seus chunks a um projeto.
#  * Histórico: v1 — adiciona `project_id` sem quebrar chamadas existentes.
#  */
def index_document(
    document_id: str,
    path: str | Path,
    *,
    project_id: str = "",
    chunk_size: int | None = None,
    overlap: int | None = None,
    max_tokens: int = 500,
    overlap_tokens: int = 60,
) -> tuple[DocumentChunk, ...]:
    """Extrai um arquivo e gera seus chunks em uma única operação determinística."""

    return _index_document.execute(
        document_id,
        path,
        project_id=project_id,
        chunk_size=chunk_size,
        overlap=overlap,
        max_tokens=max_tokens,
        overlap_tokens=overlap_tokens,
    )


# /**
#  * Indexa os chunks produzidos no vector store compartilhado pelo processo Python.
#  * Existe para unir extração, chunking e persistência no boundary recebido pela API.
#  * Histórico: v1 — adiciona a operação de indexação ponta a ponta.
#  */
def index_document_in_store(
    document_id: str,
    path: str | Path,
    *,
    project_id: str = "",
    chunk_size: int | None = None,
    overlap: int | None = None,
    max_tokens: int = 500,
    overlap_tokens: int = 60,
) -> tuple[DocumentChunk, ...]:
    """Extrai, divide e persiste os chunks de um documento."""

    from .retrieval import index_chunks

    chunks = index_document(
        document_id,
        path,
        project_id=project_id,
        chunk_size=chunk_size,
        overlap=overlap,
        max_tokens=max_tokens,
        overlap_tokens=overlap_tokens,
    )
    index_chunks(chunks)
    return chunks
