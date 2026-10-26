import sys
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from rastro_ai.document_indexing.infrastructure.embeddings.openai_embedding_repository import (
    OpenAIEmbeddingRepository,
)
from rastro_ai.document_indexing.infrastructure.embeddings import (
    openai_embedding_repository,
)


class FakeEmbeddings:
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[float(index), 0.2] for index, _text in enumerate(texts)]


class RecordingObservation:
    def __init__(self) -> None:
        self.fields: dict[str, object] = {}

    def update(self, **fields: object) -> None:
        self.fields.update(fields)


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

    # /**
    #  * Confirma que o trace recebe modelo, tokens e custo sem receber o texto do chunk.
    #  * Histórico: 025-v1 — cobre usage e custo direto do embedding sem rede.
    #  */
    def test_records_embedding_usage_and_direct_cost_without_text(self) -> None:
        observation = RecordingObservation()
        operation_arguments: dict[str, object] = {}

        @contextmanager
        def fake_observe_operation(**kwargs: object):
            operation_arguments.update(kwargs)
            yield observation

        with patch.dict(
            "os.environ",
            {"LANGFUSE_EMBEDDING_INPUT_COST_PER_TOKEN": "0.5"},
            clear=False,
        ), patch.object(
            openai_embedding_repository,
            "observe_operation",
            fake_observe_operation,
        ):
            repository = OpenAIEmbeddingRepository(
                "secret",
                dimensions=2,
                embeddings=FakeEmbeddings(),
                cost_per_input_token=0.5,
            )
            repository.embed(("hello world",))

        self.assertEqual(operation_arguments["model"], "text-embedding-3-small")
        usage_details = observation.fields["usage_details"]
        cost_details = observation.fields["cost_details"]
        self.assertIsInstance(usage_details, dict)
        self.assertIsInstance(cost_details, dict)
        self.assertGreater(usage_details["input"], 0)
        self.assertEqual(cost_details["input"], usage_details["input"] * 0.5)
        self.assertNotIn("hello world", str(operation_arguments))
        self.assertNotIn("hello world", str(observation.fields))


if __name__ == "__main__":
    unittest.main()
