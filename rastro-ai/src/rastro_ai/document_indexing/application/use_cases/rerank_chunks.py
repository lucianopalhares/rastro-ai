"""Caso de uso opcional para reordenar candidatos recuperados."""

from __future__ import annotations

from collections.abc import Sequence

from ...domain.entities import RetrievedChunk
from ..ports import ChunkReranker


# /**
#  * Executa reranking sem conhecer o provedor que calcula a nova ordem.
#  * Existe para manter retrieval inicial e reranking como etapas substituíveis.
#  * Histórico: v7 — cria o caso de uso preparatório para o pipeline RAG.
#  */
class RerankChunksUseCase:
    """Coordena a etapa opcional de reranking."""

    def __init__(self, reranker: ChunkReranker) -> None:
        self._reranker = reranker

    # /**
    #  * Reordena candidatos e preserva os objetos `RetrievedChunk` originais.
    #  * Histórico: v7 — adiciona delegação testável ao contrato de reranking.
    #  */
    def execute(
        self,
        query: str,
        chunks: Sequence[RetrievedChunk],
    ) -> tuple[RetrievedChunk, ...]:
        return self._reranker.rerank(query, tuple(chunks))
