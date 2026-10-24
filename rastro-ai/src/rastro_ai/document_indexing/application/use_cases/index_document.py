"""Caso de uso de indexação sem dependência de infraestrutura concreta."""

from __future__ import annotations

from pathlib import Path

from ...domain.entities import DocumentChunk
from ...domain.services import chunk_text
from ..ports import TextExtractor


class IndexDocumentUseCase:
    """Orquestra a extração e a divisão de um documento em chunks."""

    # /** Histórico: v1 — preserva a injeção da porta de extração. */
    def __init__(self, text_extractor: TextExtractor) -> None:
        self._text_extractor = text_extractor

    # /**
    #  * Extrai e divide o documento, carregando o projeto no metadado de cada chunk.
    #  * Histórico: v1 — inclui `project_id` para preparar o isolamento do retrieval.
    #  */
    def execute(
        self,
        document_id: str,
        path: str | Path,
        *,
        project_id: str = "",
        chunk_size: int = 800,
        overlap: int = 120,
    ) -> tuple[DocumentChunk, ...]:
        """Executa a indexação mantendo o domínio isolado de arquivos e frameworks."""

        text = self._text_extractor.extract(path)
        return chunk_text(
            text,
            document_id=document_id,
            project_id=project_id,
            chunk_size=chunk_size,
            overlap=overlap,
        )
