from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from langchain_core.documents import Document

from rastro_ai.document_indexing.domain.entities import DocumentChunk
from rastro_ai.document_indexing.infrastructure.retrieval.postgres_vector_store import (
    PostgresVectorStore,
)


class FakeEmbeddingRepository:
    """Fornece vetores controlados sem chamar um provedor externo nos testes."""

    def embed(self, texts: tuple[str, ...]) -> tuple[tuple[float, ...], ...]:
        return tuple((float(len(text)),) + (0.0,) * 383 for text in texts)


class FakeLangChainVectorStore:
    """Registra operações do adapter LangChain e devolve documentos controlados."""

    def __init__(self) -> None:
        self.added: dict[str, object] = {}
        self.filter: dict[str, str] | None = None

    def add_embeddings(self, **kwargs: object) -> list[str]:
        self.added = kwargs
        return list(kwargs["ids"])

    def similarity_search_with_score_by_vector(
        self,
        *,
        embedding: list[float],
        k: int,
        filter: dict[str, str],
    ) -> list[tuple[Document, float]]:
        self.filter = filter
        return [
            (
                Document(
                    page_content="conteúdo",
                    metadata={
                        "document_id": "doc-1",
                        "chunk_index": 0,
                        "start_offset": 0,
                        "end_offset": 9,
                        "project_id": "project-1",
                    },
                ),
                0.09,
            )
        ][:k]


class PostgresVectorStoreTests(unittest.TestCase):
    """Verifica o contrato local sem depender de um banco real."""

    def setUp(self) -> None:
        self.vector_store = FakeLangChainVectorStore()
        self.store = PostgresVectorStore(self.vector_store, FakeEmbeddingRepository())

    # /**
    #  * Confirma que o adapter envia embeddings, metadata e ID determinístico ao PGVector.
    #  * Histórico: v1 — cobria o SQL próprio de persistência.
    #  * Histórico: v6 — cobre a integração com a interface LangChain `add_embeddings`.
    #  */
    def test_upsert_persists_metadata_and_stable_id(self) -> None:
        chunk = DocumentChunk("doc-1", 0, "conteúdo", 0, 9, "project-1")

        self.store.upsert([chunk])
        first_id = self.vector_store.added["ids"][0]

        self.store.upsert([chunk])

        self.assertEqual(self.vector_store.added["metadatas"][0]["project_id"], "project-1")
        self.assertEqual(self.vector_store.added["metadatas"][0]["start_offset"], 0)
        self.assertEqual(self.vector_store.added["ids"][0], first_id)

    # /**
    #  * Confirma que a busca sempre aplica o filtro do projeto e reconstrói a entidade local.
    #  * Histórico: v1 — cobria filtro SQL por projeto e score cosine.
    #  * Histórico: v6 — cobre metadata filter e conversão de distância para similaridade.
    #  */
    def test_search_returns_chunk_and_applies_project_filter(self) -> None:
        results = self.store.search("project-1", "consulta", limit=5)

        self.assertEqual(self.vector_store.filter, {"project_id": "project-1"})
        self.assertEqual(results[0].chunk.document_id, "doc-1")
        self.assertEqual(results[0].chunk.project_id, "project-1")
        self.assertEqual(results[0].chunk.start_offset, 0)
        self.assertEqual(results[0].score, 0.91)

    # /**
    #  * Confirma que vetores incompatíveis continuam bloqueados antes do PGVector.
    #  * Histórico: v1 — valida dimensão do schema próprio.
    #  * Histórico: v6 — preserva a regra ao trocar o backend concreto.
    #  */
    def test_rejects_incompatible_embedding_dimension(self) -> None:
        class InvalidEmbeddingProvider:
            def embed(self, _texts: tuple[str, ...]) -> tuple[tuple[float, ...], ...]:
                return ((1.0,),)

        store = PostgresVectorStore(self.vector_store, InvalidEmbeddingProvider())

        with self.assertRaisesRegex(ValueError, "dimension"):
            store.upsert([DocumentChunk("doc-1", 0, "texto", 0, 5, "project-1")])


if __name__ == "__main__":
    unittest.main()
