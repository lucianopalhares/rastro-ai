"""Caso de uso para recuperar chunks relevantes dentro de um projeto."""

from __future__ import annotations

from ...domain.entities import RetrievedChunk
from ..ports import VectorStore


# /**
#  * Coordena a consulta ao store e protege o limite do contrato de retrieval.
#  * Existe para manter validações e isolamento por projeto fora da infraestrutura.
#  * Histórico: v1 — adiciona consulta vetorial determinística por projeto.
#  */
class SearchRelevantChunksUseCase:
    """Busca chunks relevantes sem conhecer a implementação do store."""

    # /** Histórico: v1 — injeta o contrato de store sem acoplar infraestrutura. */
    def __init__(self, vector_store: VectorStore) -> None:
        self._vector_store = vector_store

    # /**
    #  * Valida a consulta e retorna os melhores chunks do projeto solicitado.
    #  * Histórico: v1 — aplica validação de projeto, texto e limite antes da busca.
    #  */
    def execute(self, project_id: str, query: str, *, limit: int = 5) -> tuple[RetrievedChunk, ...]:
        """Executa retrieval filtrado por projeto com limite positivo."""

        if not project_id.strip():
            raise ValueError("project_id is required")
        if not query.strip():
            raise ValueError("query is required")
        if limit <= 0:
            raise ValueError("limit must be positive")
        return self._vector_store.search(project_id, query, limit=limit)
