import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from rastro_ai.document_indexing.infrastructure.embeddings.openai_embedding_repository import (
    OpenAIEmbeddingRepository,
)


class FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self.payload = payload

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


class OpenAIEmbeddingRepositoryTests(unittest.TestCase):
    # /**
    #  * Confirma o contrato OpenAI e o batching preservando a ordem dos resultados.
    #  * Histórico: v2 — cobre o repository externo sem realizar chamada de rede.
    #  */
    def test_embeds_texts_in_one_request_with_database_dimension(self) -> None:
        response = FakeResponse(
            {
                "data": [
                    {"index": 1, "embedding": [0.2, 0.3]},
                    {"index": 0, "embedding": [0.1, 0.2]},
                ]
            }
        )
        repository = OpenAIEmbeddingRepository("secret", dimensions=2)

        with patch(
            "rastro_ai.document_indexing.infrastructure.embeddings.openai_embedding_repository.urlopen",
            return_value=response,
        ) as open_url:
            embeddings = repository.embed(("first", "second"))

        request = open_url.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["model"], "text-embedding-3-small")
        self.assertEqual(payload["dimensions"], 2)
        self.assertEqual(embeddings, ((0.1, 0.2), (0.2, 0.3)))


if __name__ == "__main__":
    unittest.main()
