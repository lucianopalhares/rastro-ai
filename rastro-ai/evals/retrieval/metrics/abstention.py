"""Abstinência para consultas sem chunks relevantes."""

from collections.abc import Collection, Sequence


# /**
#  * Verifica se o retrieval retornou vazio quando o golden não possui evidência.
#  * Existe para expor falsos positivos sem impor threshold ou comportamento novo ao runtime.
#  * Ordem: etapa 4.3, executada somente em casos sem chunks relevantes esperados.
#  * Histórico: 026-v2 — extrai abstinência; 026-v4 — documenta a ordem.
#  */
def abstention(retrieved_chunk_ids: Sequence[str], relevant_chunk_ids: Collection[str]) -> float:
    """Retorna um quando a presença/ausência de resultados coincide com o golden."""

    if relevant_chunk_ids:
        return 1.0
    return float(not retrieved_chunk_ids)
