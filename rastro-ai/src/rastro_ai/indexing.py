"""Fachada legada para o módulo DDD de indexação de documentos."""

from __future__ import annotations

from pathlib import Path
from .bootstrap.container import build_indexing_container
from .document_indexing.domain.entities import DocumentChunk


def extract_text(path: str | Path) -> str:
    """Mantém a API legada enquanto delega a leitura ao adaptador de infraestrutura."""

    return build_indexing_container().text_extractor.extract(path)


# /**
#  * Mantém a fachada legada e propaga o projeto para os chunks produzidos.
#  * Histórico: v1 — adiciona `project_id` para integração com retrieval.
#  * Histórico: v2 — expõe orçamento de tokens do chunking estrutural.
#  * Histórico: v4 — usa o mesmo adaptador LangChain do caso de uso de indexação.
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
    """Mantém a API legada enquanto delega ao adaptador de chunking configurado."""

    return build_indexing_container().text_chunker.chunk(
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
def extract_and_chunk_document(
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

    return build_indexing_container().extract_and_chunk_document.execute(
        document_id,
        path,
        project_id=project_id,
        chunk_size=chunk_size,
        overlap=overlap,
        max_tokens=max_tokens,
        overlap_tokens=overlap_tokens,
    )


# /**
#  * Extrai, divide e persiste os chunks de um documento no vector store.
#  * Existe para unir preparação documental e persistência no boundary recebido pela API.
#  * Histórico: v1 — adiciona a operação de indexação ponta a ponta.
#  * Histórico: v2 — renomeia a operação para explicitar extração, chunking e persistência.
#  */
def extract_chunk_and_persist_document(
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

    from .retrieval import persist_document_chunks

    chunks = extract_and_chunk_document(
        document_id,
        path,
        project_id=project_id,
        chunk_size=chunk_size,
        overlap=overlap,
        max_tokens=max_tokens,
        overlap_tokens=overlap_tokens,
    )
    persist_document_chunks(chunks)
    return chunks
