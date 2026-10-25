from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from rastro_ai.document_indexing.domain.entities import DocumentChunk
from rastro_ai.document_indexing.infrastructure.retrieval.postgres_vector_store import (
    PostgresVectorStore,
)


class FakeEmbeddingRepository:
    """Fornece vetores controlados sem chamar um provedor externo nos testes."""

    def embed(self, texts: tuple[str, ...]) -> tuple[tuple[float, ...], ...]:
        return tuple((float(len(text)),) + (0.0,) * 383 for text in texts)


class FakeCursor:
    """Registra SQL e devolve uma linha controlada de retrieval."""

    def __init__(self) -> None:
        self.commands: list[tuple[str, tuple[object, ...]]] = []

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def execute(self, query: str, params: tuple[object, ...]) -> None:
        self.commands.append((query, params))

    def fetchall(self):
        return [("doc-1", 0, "conteúdo", 0, 9, "project-1", 0.91)]


class FakeConnection:
    """Simula o ciclo transacional esperado pelo adaptador PostgreSQL."""

    def __init__(self, cursor: FakeCursor) -> None:
        self.cursor_instance = cursor

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def cursor(self):
        return self.cursor_instance


class PostgresVectorStoreTests(unittest.TestCase):
    """Verifica o contrato do adaptador sem depender de um banco real."""

    def setUp(self) -> None:
        self.cursor = FakeCursor()
        self.store = PostgresVectorStore(
            lambda: FakeConnection(self.cursor), FakeEmbeddingRepository()
        )

    def test_upsert_persists_chunk_with_vector(self) -> None:
        self.store.upsert(
            [DocumentChunk("doc-1", 0, "conteúdo", 0, 9, "project-1")]
        )

        query, params = self.cursor.commands[0]
        self.assertIn("ON CONFLICT", query)
        self.assertEqual(params[0:3], ("project-1", "doc-1", 0))
        self.assertTrue(str(params[-1]).startswith("[8.0,0.0"))

    def test_search_returns_chunk_and_project_score(self) -> None:
        results = self.store.search("project-1", "consulta", limit=5)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].chunk.document_id, "doc-1")
        self.assertEqual(results[0].chunk.project_id, "project-1")
        self.assertEqual(results[0].score, 0.91)
        self.assertIn("project_id = %s", self.cursor.commands[0][0])

    def test_rejects_incompatible_embedding_dimension(self) -> None:
        class InvalidEmbeddingProvider:
            def embed(self, _texts: tuple[str, ...]) -> tuple[tuple[float, ...], ...]:
                return ((1.0,),)

        store = PostgresVectorStore(
            lambda: FakeConnection(self.cursor), InvalidEmbeddingProvider()
        )

        with self.assertRaisesRegex(ValueError, "dimension"):
            store.upsert([DocumentChunk("doc-1", 0, "texto", 0, 5, "project-1")])


if __name__ == "__main__":
    unittest.main()
