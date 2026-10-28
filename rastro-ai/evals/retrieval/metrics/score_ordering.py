"""Validação da ordem dos scores retornados."""

from collections.abc import Iterable
from math import isfinite


# /**
#  * Verifica se scores finitos estão em ordem não crescente.
#  * Existe para detectar divergência entre distância, score exposto e ordem retornada.
#  * Ordem: etapa 4.2, junto do isolamento e antes das métricas de ranking.
#  * Histórico: 026-v2 — extrai ordenação; 026-v4 — documenta a ordem.
#  */
def score_ordering(scores: Iterable[float]) -> float:
    """Retorna um para uma sequência finita e não crescente, senão zero."""

    values = tuple(float(score) for score in scores)
    return float(all(isfinite(score) for score in values) and all(left >= right for left, right in zip(values, values[1:])))
