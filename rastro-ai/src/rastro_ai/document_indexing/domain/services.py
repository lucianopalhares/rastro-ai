"""Serviços puros para normalização e divisão do texto de documentos."""

from __future__ import annotations

import re

from .entities import DocumentChunk


def normalize_text(text: str) -> str:
    """Normaliza finais de linha e espaços sem alterar o conteúdo semântico."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    normalized = "\n".join(line.rstrip() for line in normalized.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", normalized).strip()


def _find_chunk_end(text: str, start: int, chunk_size: int) -> int:
    """Prefere terminar em espaço sem deixar um chunk curto demais."""

    limit = min(start + chunk_size, len(text))
    if limit == len(text):
        return limit

    boundary = text.rfind(" ", start + chunk_size // 2, limit)
    return boundary if boundary > start else limit


# /**
#  * Divide texto normalizado em chunks reproduzíveis associados a um projeto.
#  * Histórico: v1 — propaga `project_id` sem alterar offsets, tamanho ou sobreposição.
#  */
def chunk_text(
    text: str,
    *,
    document_id: str,
    project_id: str = "",
    chunk_size: int = 800,
    overlap: int = 120,
) -> tuple[DocumentChunk, ...]:
    """Divide texto em chunks reproduzíveis, preservando offsets e sobreposição."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between zero and chunk_size")

    normalized = normalize_text(text)
    if not normalized:
        raise ValueError("Document text is required")

    chunks: list[DocumentChunk] = []
    start = 0
    while start < len(normalized):
        raw_end = _find_chunk_end(normalized, start, chunk_size)
        content_start = start
        while content_start < raw_end and normalized[content_start].isspace():
            content_start += 1
        content_end = raw_end
        while content_end > content_start and normalized[content_end - 1].isspace():
            content_end -= 1

        if content_start < content_end:
            chunks.append(
                DocumentChunk(
                    document_id=document_id,
                    index=len(chunks),
                    content=normalized[content_start:content_end],
                    start_offset=content_start,
                    end_offset=content_end,
                    project_id=project_id,
                )
            )

        if raw_end == len(normalized):
            break

        next_start = max(content_end - overlap, content_start + 1)
        while next_start < len(normalized) and normalized[next_start].isspace():
            next_start += 1
        start = next_start

    return tuple(chunks)
