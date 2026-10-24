"""Entidades do domínio de indexação de documentos."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DocumentChunk:
    """Representa um trecho indexável e sua posição no texto normalizado."""

    document_id: str
    index: int
    content: str
    start_offset: int
    end_offset: int
