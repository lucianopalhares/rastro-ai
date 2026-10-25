"""Caso de uso de indexação sem dependência de infraestrutura concreta."""

from __future__ import annotations

from pathlib import Path

from ...domain.entities import DocumentChunk
from ..ports import TextChunker, TextExtractor


class IndexDocumentUseCase:
    """Orquestra a extração e a divisão de um documento em chunks."""

    # /**
    #  * Injeta as portas de extração e chunking usadas pela indexação.
    #  * Existe para impedir que o caso de uso conheça implementações de infraestrutura.
    #  * Histórico: v1 — preserva a injeção da porta de extração.
    #  * Histórico: v2 — adiciona a porta `TextChunker` para isolar a estratégia LangChain.
    #  */
    def __init__(self, text_extractor: TextExtractor, text_chunker: TextChunker) -> None:
        self._text_extractor = text_extractor
        self._text_chunker = text_chunker

    # /**
    #  * Extrai e divide o documento, carregando o projeto no metadado de cada chunk.
    #  * Histórico: v1 — inclui `project_id` para preparar o isolamento do retrieval.
    #  * Histórico: v2 — usa chunking estrutural por tokens por padrão.
    #  * Histórico: v2 — delega a divisão à porta `TextChunker` sem importar o domínio concreto.
    #  */
    def execute(
        self,
        document_id: str,
        path: str | Path,
        *,
        project_id: str = "",
        chunk_size: int | None = None,
        overlap: int | None = None,
        max_tokens: int = 500,
        overlap_tokens: int = 60,
    ) -> tuple[DocumentChunk, ...]:
        """Executa a indexação mantendo o domínio isolado de arquivos e frameworks."""

        """Executa a indexação mantendo o domínio isolado de arquivos e frameworks."""
        text = self._text_extractor.extract(path)
        return self._text_chunker.chunk(
            text,
            document_id=document_id,
            project_id=project_id,
            chunk_size=chunk_size,
            overlap=overlap,
            max_tokens=max_tokens,
            overlap_tokens=overlap_tokens,
        )
