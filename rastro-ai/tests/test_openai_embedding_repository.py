import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from rastro_ai.document_indexing.infrastructure.embeddings.openai_embedding_repository import (
    OpenAIEmbeddingRepository,
)


class FakeEmbeddings:
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[float(index), 0.2] for index, _text in enumerate(texts)]


class OpenAIEmbeddingRepositoryTests(unittest.TestCase):
    # /**
    #  * Confirma o contrato de embeddings e o batching preservando a ordem dos resultados.
    #  * Histórico: v2 — cobre o repository externo sem realizar chamada de rede.
    #  * Histórico: v5 — injeta o adapter LangChain fake sem realizar chamada de rede.
    #  */
    def test_embeds_texts_in_one_request_with_database_dimension(self) -> None:
        repository = OpenAIEmbeddingRepository(
            "secret",
            dimensions=2,
            embeddings=FakeEmbeddings(),
        )

        embeddings = repository.embed(("first", "second"))

        self.assertEqual(embeddings, ((0.0, 0.2), (1.0, 0.2)))


if __name__ == "__main__":
    unittest.main()
