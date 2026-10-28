"""Abstinência para consultas sem chunks relevantes."""

from collections.abc import Collection, Sequence


# /**
#  * Responde: “quando não há evidência, o sistema evitou inventar um resultado?”.
#  * Um resultado 1 significa que a busca ficou vazia como esperado; 0 significa que trouxe algo
#  * para uma pergunta sem evidência. Esta verificação não decide se uma resposta gerada é boa.
#  * Exemplo: pergunta sem evidência + `[]` resulta em 1; pergunta sem evidência + `[ruído]` resulta em 0.
#  * Ordem: etapa 4.3, somente em perguntas marcadas pelo golden como sem evidência.
#  * Histórico: 026-v2 — extrai abstinência; 026-v4 — documenta a ordem; 027-v4 — simplifica a explicação.
#  */
def abstention(retrieved_chunk_ids: Sequence[str], relevant_chunk_ids: Collection[str]) -> float:
    """Retorna um quando a presença/ausência de resultados coincide com o golden."""

    if relevant_chunk_ids:
        return 1.0
    return float(not retrieved_chunk_ids)
