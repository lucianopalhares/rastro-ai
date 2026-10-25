"""Workflow LangGraph opcional para retrieval, reranking e geração fundamentada."""

from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from ..use_cases.answer_question import Answer, AnswerGenerator
from ..use_cases.rerank_chunks import RerankChunksUseCase
from ...domain.entities import RetrievedChunk
from ...application.use_cases.answer_question import ChunkRetriever, AnswerQuestionUseCase


class AnswerGraphState(TypedDict, total=False):
    """Estado serializável entre as etapas do workflow de resposta."""

    project_id: str
    question: str
    limit: int
    retrieved_chunks: tuple[RetrievedChunk, ...]
    reranked_chunks: tuple[RetrievedChunk, ...]
    answer: Answer


class _StaticRetriever:
    def __init__(self, chunks: tuple[RetrievedChunk, ...]) -> None:
        self._chunks = chunks

    def execute(self, _project_id: str, _query: str, *, limit: int) -> tuple[RetrievedChunk, ...]:
        return self._chunks[:limit]


# /**
#  * Monta um grafo opcional mantendo retrieval, reranking e geração como portas.
#  * O grafo não é conectado ao runtime nesta versão; serve como composição testável para
#  * ativar quando houver modelo, prompt e política de observabilidade definidos.
#  * Histórico: v7 — cria o workflow LangGraph preparatório sem alterar o caminho atual.
#  */
def build_answer_graph(
    retriever: ChunkRetriever,
    *,
    reranker: RerankChunksUseCase | None = None,
    generator: AnswerGenerator | None = None,
):
    """Retorna um grafo compilado para o fluxo opcional de resposta."""

    def retrieve_node(state: AnswerGraphState) -> dict[str, object]:
        chunks = retriever.execute(
            state["project_id"], state["question"], limit=state.get("limit", 5)
        )
        return {"retrieved_chunks": chunks}

    def rerank_node(state: AnswerGraphState) -> dict[str, object]:
        chunks = state.get("retrieved_chunks", ())
        return {
            "reranked_chunks": reranker.execute(state["question"], chunks)
            if reranker
            else chunks
        }

    def answer_node(state: AnswerGraphState) -> dict[str, object]:
        chunks = state.get("reranked_chunks", state.get("retrieved_chunks", ()))
        if generator:
            answer = generator.generate(state["question"], chunks)
        else:
            answer = AnswerQuestionUseCase(_StaticRetriever(chunks)).execute(
                state["project_id"], state["question"], limit=len(chunks) or 1
            )
        return {"answer": answer}

    graph = StateGraph(AnswerGraphState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("rerank", rerank_node)
    graph.add_node("answer", answer_node)
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "rerank")
    graph.add_edge("rerank", "answer")
    graph.add_edge("answer", END)
    return graph.compile()
