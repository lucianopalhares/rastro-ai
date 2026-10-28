"""nDCG para rankings com graus de relevância."""

from collections.abc import Mapping, Sequence

from .ranx_adapter import evaluate_query_metric


# /**
#  * Calcula quanto valor o ranking entrega, dando mais importância às evidências úteis que aparecem cedo.
#  * Existe como apoio interno para comparar a ordem encontrada com a melhor ordem possível.
#  * Ordem: etapa 5.4, depois que os resultados e seus graus de relevância foram preparados.
#  * Histórico: 026-v2 — extrai DCG; 026-v4 — documenta a ordem; 027-v1 — mantém a primitiva; 027-v4 — simplifica a explicação.
#  */
def discounted_cumulative_gain(
    ranked_chunk_ids: Sequence[str], relevance: Mapping[str, int], k: int
) -> float:
    """Calcula DCG@k aplicando desconto logarítmico à posição."""

    if k <= 0:
        raise ValueError("k must be positive")
    import math

    return sum(
        (2 ** relevance.get(chunk_id, 0) - 1) / math.log2(position + 1)
        for position, chunk_id in enumerate(ranked_chunk_ids[:k], start=1)
    )


# /**
#  * Responde: “a ordem dos resultados está próxima da melhor ordem possível?”.
#  * Um resultado 1 significa que as evidências mais importantes estão nas melhores posições; 0
#  * significa que nenhuma evidência útil apareceu. Também consegue considerar relevância parcial.
#  * Exemplo: `[A, B, ruído]` recebe mais valor que `[ruído, B, A]` quando A é a evidência mais importante.
#  * Ordem: etapa 5.4, depois de Recall@k e Precision@k.
#  * Histórico: 026-v2 — extrai nDCG; 026-v4 — documenta a ordem; 027-v1 — delega ao ranx; 027-v4 — simplifica a explicação.
#  */
def ndcg_at_k(ranked_chunk_ids: Sequence[str], relevance: Mapping[str, int], k: int) -> float:
    """Retorna nDCG@k calculado pelo ranx."""

    return evaluate_query_metric("ndcg", relevance, ranked_chunk_ids, k=k)
