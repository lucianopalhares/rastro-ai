from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from rastro_ai.document_indexing.application.use_cases.retrieve_chunks import SearchRelevantChunksUseCase
from rastro_ai.document_indexing.domain.entities import DocumentChunk
from rastro_ai.document_indexing.infrastructure.retrieval.in_memory_vector_store import (
    InMemoryChunkVectorStore,
)


class RetrievalTests(unittest.TestCase):
    # /** Histórico: v1 — prepara store isolado para cada cenário de retrieval. */
    def setUp(self) -> None:
        self.store = InMemoryChunkVectorStore()
        self.use_case = SearchRelevantChunksUseCase(self.store)

    # /** Histórico: v1 — verifica ranking por termos coincidentes. */
    def test_retrieval_ranks_matching_chunks(self) -> None:
        self.store.upsert(
            [
                DocumentChunk("doc-1", 0, "decisão sobre banco PostgreSQL", 0, 30, "project-1"),
                DocumentChunk("doc-2", 0, "o time discutiu férias", 0, 22, "project-1"),
            ]
        )

        results = self.use_case.execute("project-1", "PostgreSQL banco")

        self.assertEqual([result.chunk.document_id for result in results], ["doc-1"])
        self.assertGreater(results[0].score, 0)

    # /** Histórico: v1 — verifica isolamento obrigatório entre projetos. */
    def test_retrieval_filters_chunks_from_other_projects(self) -> None:
        self.store.upsert(
            [
                DocumentChunk("doc-1", 0, "decisão confidencial", 0, 19, "project-1"),
                DocumentChunk("doc-2", 0, "decisão pública", 0, 15, "project-2"),
            ]
        )

        results = self.use_case.execute("project-1", "decisão")

        self.assertEqual([result.chunk.project_id for result in results], ["project-1"])

    # /** Histórico: v1 — verifica validação do contrato de consulta. */
    def test_retrieval_validates_query_and_limit(self) -> None:
        with self.assertRaisesRegex(ValueError, "project_id"):
            self.use_case.execute("", "consulta")
        with self.assertRaisesRegex(ValueError, "query"):
            self.use_case.execute("project-1", " ")
        with self.assertRaisesRegex(ValueError, "positive"):
            self.use_case.execute("project-1", "consulta", limit=0)

    # /** Histórico: v1 — verifica limite e ausência de resultados positivos. */
    def test_retrieval_applies_limit_and_ignores_no_match(self) -> None:
        self.store.upsert(
            [
                DocumentChunk("doc-1", 0, "alpha beta", 0, 10, "project-1"),
                DocumentChunk("doc-2", 0, "alpha gamma", 0, 11, "project-1"),
            ]
        )

        self.assertEqual(len(self.use_case.execute("project-1", "alpha", limit=1)), 1)
        self.assertEqual(self.use_case.execute("project-1", "inexistente"), ())


if __name__ == "__main__":
    unittest.main()
