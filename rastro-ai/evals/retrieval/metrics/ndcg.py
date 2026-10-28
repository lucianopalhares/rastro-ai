"""nDCG para rankings com graus de relevância."""

import math
from collections.abc import Mapping, Sequence


# /**
#  * Calcula o ganho acumulado descontado de um ranking.
#  * Existe como primitiva isolada para permitir testar o cálculo sem dataset ou retriever.
#  * Ordem: etapa 5.4, usada pela nDCG depois que o ranking real e o ideal foram preparados.
#  * Histórico: 026-v2 — extrai DCG; 026-v4 — documenta a ordem.
#  */
def discounted_cumulative_gain(
    ranked_chunk_ids: Sequence[str], relevance: Mapping[str, int], k: int
) -> float:
    """Calcula DCG@k aplicando desconto logarítmico à posição."""

    if k <= 0:
        raise ValueError("k must be positive")
    return sum(
        (2 ** relevance.get(chunk_id, 0) - 1) / math.log2(position + 1)
        for position, chunk_id in enumerate(ranked_chunk_ids[:k], start=1)
    )


# /**
#  * Compara o DCG real com o ranking ideal possível para os mesmos julgamentos.
#  * Existe para avaliar a ordenação sem exigir que cada score tenha valor absoluto conhecido.
#  * Ordem: etapa 5.4, depois de Recall@k e Precision@k para cada valor de k.
#  * Histórico: 026-v2 — extrai nDCG; 026-v4 — documenta a ordem.
#  */
def ndcg_at_k(ranked_chunk_ids: Sequence[str], relevance: Mapping[str, int], k: int) -> float:
    """Retorna nDCG@k entre zero e um."""

    ideal_relevance = sorted(relevance.values(), reverse=True)[:k]
    ideal_ids = [f"__ideal__:{index}" for index in range(len(ideal_relevance))]
    ideal = dict(zip(ideal_ids, ideal_relevance))
    ideal_dcg = discounted_cumulative_gain(ideal_ids, ideal, k)
    return discounted_cumulative_gain(ranked_chunk_ids, relevance, k) / ideal_dcg if ideal_dcg else 0.0
