"""Fachada pública para indexar e recuperar chunks localmente."""

from __future__ import annotations

from collections.abc import Sequence

from .document_indexing.application.use_cases.answer_question import (
    Answer,
    AnswerQuestionUseCase,
)
from .document_indexing.application.use_cases.retrieve_chunks import RetrieveChunksUseCase
from .document_indexing.domain.entities import DocumentChunk, RetrievedChunk
from .document_indexing.infrastructure.retrieval.in_memory_vector_store import (
    InMemoryVectorStore,
)

_vector_store = InMemoryVectorStore()
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
    """Retorna resultados ordenados pela similaridade vetorial determinística."""

    return _retrieve_chunks.execute(project_id, query, limit=limit)


# /**
#  * Responde uma pergunta com os trechos recuperados e suas citações.
#  * Histórico: v1 — expõe a resposta extrativa sem evidência inventada.
#  */
def answer_question(project_id: str, question: str, *, limit: int = 5) -> Answer:
    """Retorna evidências citáveis ou informa que não há suporte documental."""

    return _answer_question.execute(project_id, question, limit=limit)
