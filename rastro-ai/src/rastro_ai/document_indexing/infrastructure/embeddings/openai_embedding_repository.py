"""Repositório de embeddings usando a API externa da OpenAI."""

from __future__ import annotations

import json
import os
from collections.abc import Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# /**
#  * Implementa o contrato de embeddings sobre o endpoint externo da OpenAI.
#  * Existe para manter o domínio e o PostgreSQL independentes do fornecedor escolhido.
#  * Histórico: v2 — adiciona `text-embedding-3-small` em lote com dimensão configurável.
#  */
class OpenAIEmbeddingRepository:
    """Consulta embeddings de texto em lote e preserva a ordem recebida."""

    def __init__(
        self,
        api_key: str,
        *,
        model: str = "text-embedding-3-small",
        dimensions: int = 384,
        base_url: str = "https://api.openai.com/v1/embeddings",
        timeout: float = 30.0,
    ) -> None:
        self._api_key = api_key
        self._model = model
        self._dimensions = dimensions
        self._base_url = base_url
        self._timeout = timeout

    # /** Histórico: v2 — cria o repositório a partir da configuração do processo. */
    @classmethod
    def from_environment(cls) -> "OpenAIEmbeddingRepository":
        """Monta o cliente usando `OPENAI_API_KEY` e parâmetros opcionais de ambiente."""

        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for postgres embeddings")
        return cls(
            api_key,
            model=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small"),
            dimensions=int(os.environ.get("EMBEDDING_DIMENSIONS", "384")),
            base_url=os.environ.get(
                "OPENAI_EMBEDDINGS_URL", "https://api.openai.com/v1/embeddings"
            ),
            timeout=float(os.environ.get("EMBEDDING_TIMEOUT_SECONDS", "30")),
        )

    # /**
    #  * Solicita embeddings em lote e valida a resposta externa.
    #  * Histórico: v2 — envia modelo, dimensão e formato float para o contrato OpenAI.
    #  */
    def embed(self, texts: Sequence[str]) -> tuple[tuple[float, ...], ...]:
        """Retorna embeddings na mesma ordem dos textos enviados."""

        if not texts or any(not text.strip() for text in texts):
            raise ValueError("embedding texts are required")
        payload = json.dumps(
            {
                "input": list(texts),
                "model": self._model,
                "dimensions": self._dimensions,
                "encoding_format": "float",
            }
        ).encode("utf-8")
        request = Request(
            self._base_url,
            data=payload,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self._timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError) as error:
            raise RuntimeError(f"Embedding provider request failed: {error}") from error

        data = result.get("data")
        if not isinstance(data, list) or len(data) != len(texts):
            raise RuntimeError("Embedding provider returned an invalid item count")
        ordered = sorted(data, key=lambda item: item.get("index", -1))
        embeddings = tuple(tuple(float(value) for value in item["embedding"]) for item in ordered)
        if any(len(embedding) != self._dimensions for embedding in embeddings):
            raise RuntimeError("Embedding provider returned an invalid dimension")
        return embeddings
