"""Caso de uso para responder perguntas somente com evidências recuperadas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ...domain.entities import RetrievedChunk


# /**
#  * Representa a referência verificável de um trecho usado na resposta.
#  * Existe para permitir que a resposta exponha documento, posição e conteúdo
#  * sem depender de um modelo generativo.
#  * Histórico: v1 — cria o contrato mínimo de citação da resposta.
#  */
@dataclass(frozen=True, slots=True)
class Citation:
    """Identifica exatamente o trecho recuperado que sustenta a resposta."""

    document_id: str
    chunk_index: int
    start_offset: int
    end_offset: int
    excerpt: str


# /**
#  * Contém a resposta extrativa e as fontes que a sustentam.
#  * Existe para separar texto exibível de metadados determinísticos de evidência.
#  * Histórico: v1 — adiciona resposta explícita para evidência e ausência dela.
#  */
@dataclass(frozen=True, slots=True)
class Answer:
    """Resposta produzida a partir dos chunks retornados pelo retrieval."""

    text: str
    citations: tuple[Citation, ...]


# /**
#  * Define uma porta mínima para consultar evidências por projeto.
#  * Existe para testar a resposta sem acoplar o caso de uso ao store concreto.
#  * Histórico: v1 — cria o contrato de retrieval usado pela geração extrativa.
#  */
class ChunkRetriever(Protocol):
    """Contrato mínimo de retrieval usado pelo caso de uso de respostas."""

    def execute(
        self,
        project_id: str,
        query: str,
        *,
        limit: int,
    ) -> tuple[RetrievedChunk, ...]:
        """Retorna evidências relevantes para a pergunta."""


# /**
#  * Responde de forma extrativa e impede afirmações sem evidência recuperada.
#  * Existe como etapa segura antes da introdução de um modelo generativo e
#  * transforma cada resultado do retrieval em uma citação verificável.
#  * Histórico: v1 — implementa resposta com fontes e negativa sem evidência.
#  */
class AnswerQuestionUseCase:
    """Orquestra retrieval e formatação determinística da resposta."""

    # /** Histórico: v1 — injeta o retrieval para manter o caso de uso testável. */
    def __init__(self, retriever: ChunkRetriever) -> None:
        self._retriever = retriever

    # /**
    #  * Recupera evidências e monta uma resposta que só cita trechos existentes.
    #  * Histórico: v1 — preserva o isolamento por projeto e explicita ausência de evidência.
    #  */
    def execute(self, project_id: str, question: str, *, limit: int = 5) -> Answer:
        """Retorna trechos sustentados por citações ou uma negativa fundamentada."""

        results = self._retriever.execute(project_id, question, limit=limit)
        citations = tuple(
            Citation(
                document_id=result.chunk.document_id,
                chunk_index=result.chunk.index,
                start_offset=result.chunk.start_offset,
                end_offset=result.chunk.end_offset,
                excerpt=result.chunk.content,
            )
            for result in results
        )
        if not citations:
            return Answer(
                text="Não encontrei evidência suficiente nos documentos deste projeto para responder.",
                citations=(),
            )

        evidence = "\n".join(
            f"[{citation.document_id}#{citation.chunk_index}] {citation.excerpt}"
            for citation in citations
        )
        return Answer(text=f"Evidências encontradas:\n{evidence}", citations=citations)
