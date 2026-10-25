from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from rastro_ai.document_indexing.application.use_cases.answer_question import (
    AnswerQuestionUseCase,
)
from rastro_ai.document_indexing.domain.entities import DocumentChunk
from rastro_ai.document_indexing.infrastructure.retrieval.in_memory_vector_store import (
    InMemoryChunkVectorStore,
)


class AnswerTests(unittest.TestCase):
    # /** Histórico: v1 — prepara retrieval isolado para respostas determinísticas. */
    def setUp(self) -> None:
        self.store = InMemoryChunkVectorStore()
        self.use_case = AnswerQuestionUseCase(self._retriever())

    def _retriever(self):
        from rastro_ai.document_indexing.application.use_cases.retrieve_chunks import (
            SearchRelevantChunksUseCase,
        )

        return SearchRelevantChunksUseCase(self.store)

    # /** Histórico: v1 — verifica que resposta e citação reproduzem a evidência recuperada. */
    def test_answer_contains_retrieved_excerpt_and_citation(self) -> None:
        self.store.upsert(
            [
                DocumentChunk(
                    "meeting-1",
                    2,
                    "A equipe escolheu PostgreSQL por causa do suporte transacional.",
                    40,
                    105,
                    "project-1",
                )
            ]
        )

        answer = self.use_case.execute("project-1", "Por que escolheram PostgreSQL?")

        self.assertIn("A equipe escolheu PostgreSQL", answer.text)
        self.assertEqual(len(answer.citations), 1)
        self.assertEqual(answer.citations[0].document_id, "meeting-1")
        self.assertEqual(answer.citations[0].chunk_index, 2)
        self.assertEqual(answer.citations[0].start_offset, 40)
        self.assertEqual(answer.citations[0].end_offset, 105)
        self.assertIn("[meeting-1#2]", answer.text)

    # /** Histórico: v1 — verifica negativa explícita quando não há evidência. */
    def test_answer_declares_absence_of_evidence(self) -> None:
        self.store.upsert(
            [DocumentChunk("meeting-1", 0, "A equipe discutiu férias.", 0, 25, "project-1")]
        )

        answer = self.use_case.execute("project-1", "Qual foi o orçamento?")

        self.assertEqual(answer.citations, ())
        self.assertIn("Não encontrei evidência suficiente", answer.text)

    # /** Histórico: v1 — verifica que o projeto continua isolado na resposta. */
    def test_answer_does_not_cite_other_projects(self) -> None:
        self.store.upsert(
            [
                DocumentChunk("project-a-doc", 0, "Decisão do projeto A", 0, 20, "project-a"),
                DocumentChunk("project-b-doc", 0, "Decisão do projeto B", 0, 20, "project-b"),
            ]
        )

        answer = self.use_case.execute("project-a", "Decisão")

        self.assertEqual([citation.document_id for citation in answer.citations], ["project-a-doc"])


if __name__ == "__main__":
    unittest.main()
