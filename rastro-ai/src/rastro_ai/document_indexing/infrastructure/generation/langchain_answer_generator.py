"""Prompt e adapter LangChain para respostas estruturadas com citações."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from langchain_core.prompts import ChatPromptTemplate

from ...application.use_cases.answer_question import Answer, Citation
from ...domain.entities import RetrievedChunk


# /**
#  * Cria o prompt base para respostas fundamentadas somente no contexto recebido.
#  * Existe para centralizar a política de não inventar evidências antes da chain real.
#  * Histórico: v7 — prepara prompt LangChain reutilizável para geração futura.
#  */
def build_answer_prompt() -> ChatPromptTemplate:
    """Retorna prompt com placeholders estáveis para pergunta e contexto."""

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Responda somente com base no contexto. Se não houver suporte, "
                "informe que não há evidência suficiente. Preserve as referências "
                "[document_id#chunk_index] quando elas sustentarem a resposta.",
            ),
            ("human", "Pergunta:\n{question}\n\nContexto:\n{context}"),
        ]
    )


# /**
#  * Adapta um Runnable LangChain que retorna texto e índices de citações para `Answer`.
#  * A chain deve retornar `{"text": str, "citation_indexes": list[int]}`; os índices são
#  * validados localmente para impedir citações que não pertencem ao contexto recuperado.
#  * Histórico: v7 — cria adapter de geração sem ativar chamadas de modelo no runtime atual.
#  */
class LangChainAnswerGenerator:
    """Converte a saída estruturada de uma chain em resposta verificável."""

    def __init__(self, runnable: Any) -> None:
        self._runnable = runnable

    # /**
    #  * Invoca a chain com contexto formatado e reconstrói citações verificadas.
    #  * Histórico: v7 — adiciona validação de texto e índices de evidência.
    #  */
    def generate(
        self,
        question: str,
        context: tuple[RetrievedChunk, ...],
    ) -> Answer:
        result = self._runnable.invoke(
            {
                "question": question,
                "context": self._format_context(context),
            }
        )
        if not isinstance(result, dict) or not isinstance(result.get("text"), str):
            raise ValueError("answer chain must return text and citation_indexes")
        indexes = result.get("citation_indexes", [])
        if not isinstance(indexes, (list, tuple)):
            raise ValueError("citation_indexes must be a list")
        if any(not isinstance(index, int) or index < 0 or index >= len(context) for index in indexes):
            raise ValueError("citation index is outside the retrieved context")
        citations = tuple(
            Citation(
                document_id=context[index].chunk.document_id,
                chunk_index=context[index].chunk.index,
                start_offset=context[index].chunk.start_offset,
                end_offset=context[index].chunk.end_offset,
                excerpt=context[index].chunk.content,
            )
            for index in indexes
        )
        return Answer(text=result["text"], citations=citations)

    @staticmethod
    def _format_context(context: Sequence[RetrievedChunk]) -> str:
        return "\n".join(
            f"[{item.chunk.document_id}#{item.chunk.index}] {item.chunk.content}"
            for item in context
        )
