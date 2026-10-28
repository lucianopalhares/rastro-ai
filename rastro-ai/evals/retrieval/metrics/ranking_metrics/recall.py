"""Recall@k para resultados de retrieval."""

from collections.abc import Collection, Sequence

from .ranx_adapter import evaluate_query_metric


# /**
#  * Responde: “de tudo que era necessário para esta pergunta, quanto foi encontrado?”.
#  * Um resultado 1 significa que todas as evidências esperadas apareceram no top-k; 0 significa
#  * que nenhuma apareceu. Valores entre 0 e 1 mostram que parte das evidências ficou de fora.
#  * Exemplo: se A e B são necessários e o top-2 contém apenas A, Recall@2 é 0,5.
#  * Ordem: etapa 5.1, depois que a pergunta e os resultados foram comparados ao golden.
#  * Histórico: 026-v2 — extrai Recall@k; 026-v4 — documenta a ordem; 027-v1 — delega ao ranx; 027-v4 — simplifica a explicação.
#  */
def recall_at_k(relevant_chunk_ids: Collection[str], retrieved_chunk_ids: Sequence[str], k: int) -> float:
    """Retorna Recall@k calculado pelo ranx."""

    return evaluate_query_metric("recall", relevant_chunk_ids, retrieved_chunk_ids, k=k)
