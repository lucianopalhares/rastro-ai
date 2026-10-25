"""Fachada pública para indexar e recuperar chunks localmente."""

from __future__ import annotations

from collections.abc import Sequence
from .bootstrap.container import build_retrieval_container
from .document_indexing.application.use_cases.answer_question import Answer
from .document_indexing.domain.entities import DocumentChunk, RetrievedChunk


# /**
#  * Indexa chunks na store vetorial local compartilhada pela fachada.
#  * Histórico: v1 — expõe a operação mínima para ligar chunking e retrieval.
#  */
def index_chunks(chunks: Sequence[DocumentChunk]) -> None:
    """Disponibiliza chunks para consultas posteriores no processo."""

    build_retrieval_container().vector_store.upsert(chunks)


# /**
#  * Recupera chunks relevantes dentro de um único projeto.
#  * Histórico: v1 — expõe a consulta pública com limite configurável.
#  */
def retrieve_chunks(project_id: str, query: str, *, limit: int = 5) -> tuple[RetrievedChunk, ...]:
    """Retorna resultados ordenados pela similaridade vetorial do repository configurado."""

    return build_retrieval_container().retrieve_chunks.execute(project_id, query, limit=limit)


# /**
#  * Responde uma pergunta com os trechos recuperados e suas citações.
#  * Histórico: v1 — expõe a resposta extrativa sem evidência inventada.
#  */
def answer_question(project_id: str, question: str, *, limit: int = 5) -> Answer:
    """Retorna evidências citáveis ou informa que não há suporte documental."""

    return build_retrieval_container().answer_question.execute(
        project_id, question, limit=limit
    )
