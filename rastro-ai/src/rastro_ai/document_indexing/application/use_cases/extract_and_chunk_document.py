"""Caso de uso de extração e chunking sem dependência de infraestrutura concreta."""

from __future__ import annotations

from pathlib import Path

from ...domain.entities import DocumentChunk
from ..ports import TextChunker, TextExtractor


# /**
#  * Orquestra a leitura de um documento e a geração dos seus chunks.
#  * Existe para deixar explícito que esta etapa ainda não persiste embeddings ou chunks.
#  * Histórico: v1 — renomeia `IndexDocumentUseCase` para refletir o comportamento real.
#  */
class ExtractAndChunkDocumentUseCase:
    """Extrai texto e gera chunks por meio das portas da aplicação."""

    # /**
    #  * Injeta as portas de extração e chunking usadas pelo caso de uso.
    #  * Existe para impedir que a aplicação conheça implementações de infraestrutura.
    #  * Histórico: v1 — renomeia o caso de uso sem alterar suas dependências.
    #  */
    def __init__(self, text_extractor: TextExtractor, text_chunker: TextChunker) -> None:
        self._text_extractor = text_extractor
        self._text_chunker = text_chunker

    # /**
    #  * Extrai e divide o documento, carregando o projeto no metadado de cada chunk.
    #  * Histórico: v1 — substitui a descrição ambígua de indexação por extração e chunking.
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
        """Extrai o texto e devolve chunks sem acessar persistência externa."""

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
