"""Validação da ordem dos scores retornados."""

from collections.abc import Iterable
from math import isfinite


# /**
#  * Responde: “os resultados estão realmente ordenados do mais forte para o mais fraco?”.
#  * Um resultado 1 significa que os scores são válidos e não aumentam ao longo da lista; 0 significa
#  * que há score inválido ou resultado fora de ordem. Isso verifica a lista, não a relevância do conteúdo.
#  * Exemplo: `[0,9, 0,7, 0,3]` resulta em 1; `[0,7, 0,9]` resulta em 0.
#  * Ordem: etapa 4.2, junto do isolamento e antes das métricas de ranking.
#  * Histórico: 026-v2 — extrai ordenação; 026-v4 — documenta a ordem; 027-v4 — simplifica a explicação.
#  */
def score_ordering(scores: Iterable[float]) -> float:
    """Retorna um para uma sequência finita e não crescente, senão zero."""

    values = tuple(float(score) for score in scores)
    return float(all(isfinite(score) for score in values) and all(left >= right for left, right in zip(values, values[1:])))
