"""Reciprocal rank e MRR para rankings de chunks."""

from collections.abc import Collection, Iterable


# /**
#  * Mede a posição inversa do primeiro chunk relevante de uma consulta.
#  * Existe para avaliar a rapidez com que o ranking encontra a primeira evidência útil.
#  * Ordem: etapa 5.3, executada antes da média final e somente em consultas respondíveis.
#  * Histórico: 026-v2 — extrai reciprocal rank; 026-v4 — documenta a ordem.
#  */
def reciprocal_rank(retrieved_chunk_ids: Iterable[str], relevant_chunk_ids: Collection[str]) -> float:
    """Retorna um sobre a posição do primeiro relevante ou zero quando ausente."""

    relevant = set(relevant_chunk_ids)
    for position, chunk_id in enumerate(retrieved_chunk_ids, start=1):
        if chunk_id in relevant:
            return 1.0 / position
    return 0.0


# /**
#  * Calcula a média dos reciprocal ranks de várias consultas.
#  * Existe para manter a agregação de MRR desacoplada do dataset e do retriever.
#  * Ordem: etapa 6.1, após todas as consultas respondíveis terem produzido seu reciprocal rank.
#  * Histórico: 026-v2 — adiciona agregador puro de MRR; 026-v4 — documenta a ordem.
#  */
def mean_reciprocal_rank(values: Iterable[float]) -> float:
    """Retorna a média dos valores; uma coleção vazia produz zero."""

    ranks = tuple(values)
    return sum(ranks) / len(ranks) if ranks else 0.0
