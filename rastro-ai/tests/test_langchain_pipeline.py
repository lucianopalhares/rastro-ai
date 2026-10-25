from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from rastro_ai.document_indexing.application.use_cases.rerank_chunks import RerankChunksUseCase
from rastro_ai.document_indexing.application.workflows.answer_graph import build_answer_graph
from rastro_ai.document_indexing.domain.entities import DocumentChunk, RetrievedChunk
from rastro_ai.document_indexing.infrastructure.generation.langchain_answer_generator import (
    LangChainAnswerGenerator,
    build_answer_prompt,
)
from rastro_ai.document_indexing.infrastructure.reranking.langchain_reranker import (
    LangChainReranker,
)


class FakeRunnable:
    """Devolve uma saída LangChain controlada sem chamar modelo externo."""

    def __init__(self, result: object) -> None:
        self.result = result
        self.inputs: list[dict[str, object]] = []

    def invoke(self, value: dict[str, object]) -> object:
        self.inputs.append(value)
        return self.result


# /**
#  * Verifica as portas e adapters que preparam o pipeline LangChain/LangGraph.
#  * Histórico: v7 — cobre reranking, prompt, geração estruturada e estado do grafo.
#  */
class LangChainPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.chunks = (
            RetrievedChunk(
                DocumentChunk("doc-1", 0, "primeiro contexto", 0, 17, "project-1"),
                0.7,
            ),
            RetrievedChunk(
                DocumentChunk("doc-2", 1, "segundo contexto", 18, 34, "project-1"),
                0.6,
            ),
        )

    # /**
    #  * Confirma que o reranker LangChain só pode devolver uma permutação válida.
    #  * Histórico: v7 — cobre adapter e preservação das entidades recuperadas.
    #  */
    def test_reranker_reorders_existing_chunks(self) -> None:
        runnable = FakeRunnable({"order": [1, 0]})
        reranker = RerankChunksUseCase(LangChainReranker(runnable))

        result = reranker.execute("qual contexto?", self.chunks)

        self.assertEqual([item.chunk.document_id for item in result], ["doc-2", "doc-1"])
        self.assertEqual(runnable.inputs[0]["documents"], ["primeiro contexto", "segundo contexto"])

    # /**
    #  * Confirma que a geração transforma índices de evidência em citações verificáveis.
    #  * Histórico: v7 — cobre o adapter de chain sem chamada de modelo.
    #  */
    def test_answer_generator_validates_and_maps_citations(self) -> None:
        runnable = FakeRunnable({"text": "Resposta fundamentada.", "citation_indexes": [1]})
        generator = LangChainAnswerGenerator(runnable)

        answer = generator.generate("pergunta", self.chunks)

        self.assertEqual(answer.text, "Resposta fundamentada.")
        self.assertEqual(answer.citations[0].document_id, "doc-2")
        self.assertIn("[doc-1#0]", runnable.inputs[0]["context"])

    # /**
    #  * Confirma que o prompt possui placeholders estáveis para futura chain.
    #  * Histórico: v7 — cobre a preparação do prompt LangChain em isolamento.
    #  */
    def test_answer_prompt_has_question_and_context_variables(self) -> None:
        prompt = build_answer_prompt()

        self.assertEqual(set(prompt.input_variables), {"question", "context"})

    # /**
    #  * Confirma que o grafo coordena retrieval, reranking e geração sem mudar a resposta padrão.
    #  * Histórico: v7 — cobre o workflow LangGraph opcional com componentes fake.
    #  */
    def test_answer_graph_composes_optional_steps(self) -> None:
        class Retriever:
            def __init__(self, chunks):
                self.chunks = chunks

            def execute(self, _project_id: str, _query: str, *, limit: int):
                return self.chunks[:limit]

        reranker = RerankChunksUseCase(LangChainReranker(FakeRunnable({"order": [1, 0]})))
        generator = LangChainAnswerGenerator(
            FakeRunnable({"text": "Resposta do grafo.", "citation_indexes": [0]})
        )
        graph = build_answer_graph(Retriever(self.chunks), reranker=reranker, generator=generator)

        state = graph.invoke(
            {"project_id": "project-1", "question": "pergunta", "limit": 2}
        )

        self.assertEqual(state["answer"].text, "Resposta do grafo.")
        self.assertEqual(state["answer"].citations[0].document_id, "doc-2")


if __name__ == "__main__":
    unittest.main()
