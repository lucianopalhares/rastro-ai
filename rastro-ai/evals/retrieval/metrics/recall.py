"""Recall@k para resultados de retrieval."""

from collections.abc import Collection, Sequence


# /**
#  * Mede a fração dos chunks relevantes que apareceu no top-k.
#  * Existe para separar cobertura de evidências da precisão e da ordem do ranking.
#  * Ordem: etapa 5.1, depois que os IDs retornados e esperados foram normalizados.
#  * Histórico: 026-v2 — extrai Recall@k; 026-v4 — documenta a ordem.
#  */
def recall_at_k(relevant_chunk_ids: Collection[str], retrieved_chunk_ids: Sequence[str], k: int) -> float:
    """Retorna Recall@k entre zero e um; uma consulta sem relevância vale zero."""

    if k <= 0:
        raise ValueError("k must be positive")
    if not relevant_chunk_ids:
        return 0.0
    found = len(set(retrieved_chunk_ids[:k]) & set(relevant_chunk_ids))
    return found / len(set(relevant_chunk_ids))
