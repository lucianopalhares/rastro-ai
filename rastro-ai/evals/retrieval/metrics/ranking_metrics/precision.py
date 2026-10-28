"""Precision@k para resultados de retrieval."""

from collections.abc import Collection, Sequence

from .ranx_adapter import evaluate_query_metric


# /**
#  * Responde: “dos primeiros k resultados, quanto realmente ajuda a responder?”.
#  * Um resultado 1 significa que os resultados do top-k são relevantes; 0 significa que eles são
#  * apenas ruído. A métrica mostra se o retriever encontrou evidência sem trazer excesso de conteúdo inútil.
#  * Exemplo: em `[ruído, A, B]`, com A e B relevantes, Precision@3 é 2/3.
#  * Ordem: etapa 5.2, depois da comparação dos resultados com o golden.
#  * Histórico: 026-v2 — extrai Precision@k; 026-v4 — documenta a ordem; 027-v1 — delega ao ranx; 027-v4 — simplifica a explicação.
#  */
def precision_at_k(relevant_chunk_ids: Collection[str], retrieved_chunk_ids: Sequence[str], k: int) -> float:
    """Retorna Precision@k calculada pelo ranx."""

    return evaluate_query_metric("precision", relevant_chunk_ids, retrieved_chunk_ids, k=k)
