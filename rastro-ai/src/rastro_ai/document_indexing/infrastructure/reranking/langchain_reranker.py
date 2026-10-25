"""Adapter para componentes LangChain que retornam a ordem dos candidatos."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from ...domain.entities import RetrievedChunk


# /**
#  * Adapta um Runnable LangChain para a porta de reranking da aplicação.
#  * O runnable recebe pergunta/documentos e deve retornar índices inteiros na nova ordem,
#  * mantendo offsets, projeto e identidade dos chunks sob controle da Rastro.
#  * Histórico: v7 — cria adapter sem escolher um provedor externo específico.
#  */
class LangChainReranker:
    """Converte a saída estruturada de um Runnable em chunks recuperados."""

    def __init__(self, runnable: Any) -> None:
        self._runnable = runnable

    # /**
    #  * Invoca o componente LangChain e valida que a saída é uma permutação dos candidatos.
    #  * Histórico: v7 — protege contra índices ausentes, duplicados ou fora do intervalo.
    #  */
    def rerank(
        self,
        query: str,
        chunks: Sequence[RetrievedChunk],
    ) -> tuple[RetrievedChunk, ...]:
        candidates = tuple(chunks)
        if not candidates:
            return ()
        result = self._runnable.invoke(
            {
                "query": query,
                "documents": [chunk.chunk.content for chunk in candidates],
            }
        )
        order = result.get("order") if isinstance(result, dict) else result
        if not isinstance(order, (list, tuple)):
            raise ValueError("reranker must return an order of candidate indexes")
        indexes = tuple(int(index) for index in order)
        if set(indexes) != set(range(len(candidates))) or len(indexes) != len(candidates):
            raise ValueError("reranker order must contain each candidate exactly once")
        return tuple(candidates[index] for index in indexes)
