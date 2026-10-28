"""Reciprocal rank e MRR para rankings de chunks."""

from collections.abc import Collection, Iterable

from .ranx_adapter import evaluate_query_metric


# /**
#  * Responde: “quão cedo aparece a primeira evidência útil?”.
#  * O resultado é 1 quando ela está em primeiro, 0,5 quando está em segundo e 0 quando não aparece.
#  * A média do MRR resume essa rapidez em várias perguntas que possuem resposta.
#  * Exemplo: em `[ruído, A, B]`, se A é relevante, o primeiro acerto está na posição 2 e o resultado é 0,5.
#  * Ordem: etapa 5.3, depois do ranking e somente em consultas com evidência esperada.
#  * Histórico: 026-v2 — extrai reciprocal rank; 026-v4 — documenta a ordem; 027-v1 — delega ao ranx; 027-v4 — simplifica a explicação.
#  */
def reciprocal_rank(retrieved_chunk_ids: Iterable[str], relevant_chunk_ids: Collection[str]) -> float:
    """Retorna o reciprocal rank calculado pelo ranx."""

    return evaluate_query_metric("mrr", relevant_chunk_ids, tuple(retrieved_chunk_ids))


# /**
#  * Resume em um número a posição da primeira evidência útil em várias perguntas.
#  * Existe para mostrar se, em média, o sistema encontra rapidamente algo que pode fundamentar a resposta.
#  * Ordem: etapa 6.1, após cada pergunta respondível produzir seu resultado.
#  * Histórico: 026-v2 — adiciona agregador puro de MRR; 026-v4 — documenta a ordem; 027-v4 — simplifica a explicação.
#  */
def mean_reciprocal_rank(values: Iterable[float]) -> float:
    """Retorna a média dos valores; uma coleção vazia produz zero."""

    ranks = tuple(values)
    return sum(ranks) / len(ranks) if ranks else 0.0
