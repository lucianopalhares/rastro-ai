"""Precision@k para resultados de retrieval."""

from collections.abc import Collection, Sequence


# /**
#  * Mede a proporção do top-k que contém chunks anotados como relevantes.
#  * Existe para penalizar ruído mesmo quando o retrieval encontra alguma evidência.
#  * Ordem: etapa 5.2, executada por k depois da normalização do ranking.
#  * Histórico: 026-v2 — extrai Precision@k; 026-v4 — documenta a ordem.
#  */
def precision_at_k(relevant_chunk_ids: Collection[str], retrieved_chunk_ids: Sequence[str], k: int) -> float:
    """Retorna Precision@k usando k como denominador estável."""

    if k <= 0:
        raise ValueError("k must be positive")
    found = len(set(retrieved_chunk_ids[:k]) & set(relevant_chunk_ids))
    return found / k
