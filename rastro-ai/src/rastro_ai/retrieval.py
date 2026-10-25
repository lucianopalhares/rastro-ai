"""Fachada pública para indexar e recuperar chunks localmente."""

from __future__ import annotations

from collections.abc import Sequence
from os import environ

from .semantic_search.application.use_cases.answer_question import (
    Answer,
    AnswerQuestionUseCase,
)
from .semantic_search.application.use_cases.retrieve_chunks import RetrieveChunksUseCase
from .documents.domain.entities import DocumentChunk, RetrievedChunk
# /**
#  * Seleciona o store persistente exigido pelo runtime para indexação e busca semântica.
#  * Existe para impedir que uma configuração ausente ou inválida degrade silenciosamente para busca lexical.
#  * Histórico: v1 — adiciona `VECTOR_STORE_BACKEND=postgres` com embeddings locais.
#  * v2 — seleciona o repository externo OpenAI para o backend persistente.
#  * v3 — remove o fallback implícito em memória e exige `postgres` no runtime.
#  */
def _build_vector_store():
    """Cria o backend persistente conforme a configuração explícita do processo."""

    backend = environ.get("VECTOR_STORE_BACKEND", "").strip().casefold()
    if backend != "postgres":
        raise ValueError("VECTOR_STORE_BACKEND must be 'postgres'")

    from .embeddings.infrastructure.openai.repository import OpenAIEmbeddingRepository
    from .semantic_search.infrastructure.pgvector.repository import PostgresVectorStore

    return PostgresVectorStore.from_environment(
        OpenAIEmbeddingRepository.from_environment()
    )


_vector_store = _build_vector_store()
_retrieve_chunks = RetrieveChunksUseCase(_vector_store)
_answer_question = AnswerQuestionUseCase(_retrieve_chunks)


# /**
#  * Indexa chunks na store vetorial local compartilhada pela fachada.
#  * Histórico: v1 — expõe a operação mínima para ligar chunking e retrieval.
#  */
def index_chunks(chunks: Sequence[DocumentChunk]) -> None:
    """Disponibiliza chunks para consultas posteriores no processo."""

    _vector_store.upsert(chunks)


# /**
#  * Recupera chunks relevantes dentro de um único projeto.
#  * Histórico: v1 — expõe a consulta pública com limite configurável.
#  */
def retrieve_chunks(project_id: str, query: str, *, limit: int = 5) -> tuple[RetrievedChunk, ...]:
    """Retorna resultados ordenados pela similaridade vetorial do repository configurado."""

    return _retrieve_chunks.execute(project_id, query, limit=limit)


# /**
#  * Responde uma pergunta com os trechos recuperados e suas citações.
#  * Histórico: v1 — expõe a resposta extrativa sem evidência inventada.
#  */
def answer_question(project_id: str, question: str, *, limit: int = 5) -> Answer:
    """Retorna evidências citáveis ou informa que não há suporte documental."""

    return _answer_question.execute(project_id, question, limit=limit)
