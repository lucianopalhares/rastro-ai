"""Double lexical determinístico em memória para testes e evaluation local."""

from __future__ import annotations

import math
import re
from collections import Counter
from collections.abc import Sequence

from ...domain.entities import DocumentChunk, RetrievedChunk

_TOKEN_PATTERN = re.compile(r"[\wÀ-ÿ]+", re.UNICODE)


# /** Histórico: v1 — cria a representação lexical determinística do texto. */
def _to_vector(text: str) -> Counter[str]:
    """Converte texto em frequência de termos para uma representação reproduzível."""

    return Counter(token.casefold() for token in _TOKEN_PATTERN.findall(text))


# /** Histórico: v1 — calcula o score sem dependência externa. */
def _cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    """Calcula similaridade de cosseno sem depender de bibliotecas externas."""

    if not left or not right:
        return 0.0
    dot_product = sum(value * right.get(term, 0) for term, value in left.items())
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return dot_product / (left_norm * right_norm)


# /**
#  * Armazena chunks e executa ranking lexical determinístico em memória.
#  * Existe somente para testes isolados e evaluation local, não para o runtime semântico.
#  * Histórico: v1 — adiciona upsert, filtro por projeto e ranking por cosseno.
#  * Histórico: v2 — deixa explícito que o adaptador não substitui embeddings nem pgvector.
#  */
class InMemoryVectorStore:
    """Implementa o contrato de retrieval sem banco, modelo ou rede para cenários isolados."""

    # /** Histórico: v1 — inicializa o índice efêmero do processo. */
    def __init__(self) -> None:
        self._entries: dict[tuple[str, str, int], tuple[DocumentChunk, Counter[str]]] = {}

    # /**
    #  * Insere ou substitui chunks pela identidade documento/índice/projeto.
    #  * Histórico: v1 — cria indexação local determinística para os chunks gerados.
    #  */
    def upsert(self, chunks: Sequence[DocumentChunk]) -> None:
        """Indexa o conteúdo textual dos chunks recebidos."""

        for chunk in chunks:
            if not chunk.project_id.strip():
                raise ValueError("project_id is required")
            self._entries[(chunk.project_id, chunk.document_id, chunk.index)] = (
                chunk,
                _to_vector(chunk.content),
            )

    # /**
    #  * Busca chunks somente no projeto informado e ordena por score estável.
    #  * Histórico: v1 — protege o isolamento por projeto antes de retornar resultados.
    #  */
    def search(self, project_id: str, query: str, *, limit: int) -> tuple[RetrievedChunk, ...]:
        """Retorna resultados positivos ordenados por similaridade e inserção."""

        query_vector = _to_vector(query)
        matches: list[tuple[int, RetrievedChunk]] = []
        for position, (chunk, vector) in enumerate(self._entries.values()):
            if chunk.project_id != project_id:
                continue
            score = _cosine_similarity(query_vector, vector)
            if score > 0:
                matches.append((position, RetrievedChunk(chunk=chunk, score=score)))

        matches.sort(key=lambda item: (-item[1].score, item[0]))
        return tuple(result for _, result in matches[:limit])
