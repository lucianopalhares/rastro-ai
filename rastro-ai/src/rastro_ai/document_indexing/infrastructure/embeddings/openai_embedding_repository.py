"""Repositório de embeddings usando a API externa da OpenAI."""

from __future__ import annotations

import os
from collections.abc import Sequence

from langchain_openai import OpenAIEmbeddings


# /**
#  * Implementa o contrato de embeddings sobre o endpoint externo da OpenAI.
#  * Existe para manter o domínio e o PostgreSQL independentes do fornecedor escolhido.
#  * Histórico: v2 — adiciona `text-embedding-3-small` em lote com dimensão configurável.
#  * Histórico: v5 — usa `OpenAIEmbeddings` do LangChain atrás do contrato local.
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
        embeddings: object | None = None,
    ) -> None:
        self._model = model
        self._dimensions = dimensions
        self._embeddings = embeddings or OpenAIEmbeddings(
            api_key=api_key,
            model=model,
            dimensions=dimensions,
            base_url=base_url.removesuffix("/embeddings"),
            timeout=timeout,
        )

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
    #  * Solicita embeddings em lote pelo adaptador LangChain e valida sua resposta.
    #  * Histórico: v2 — envia modelo, dimensão e formato float para o contrato OpenAI.
    #  * Histórico: v5 — delega transporte, batching e retries a `OpenAIEmbeddings`.
    #  */
    def embed(self, texts: Sequence[str]) -> tuple[tuple[float, ...], ...]:
        """Retorna embeddings na mesma ordem dos textos enviados."""

        if not texts or any(not text.strip() for text in texts):
            raise ValueError("embedding texts are required")
        values = self._embeddings.embed_documents(list(texts))
        if len(values) != len(texts):
            raise RuntimeError("Embedding provider returned an invalid item count")
        embeddings = tuple(tuple(float(value) for value in embedding) for embedding in values)
        if any(len(embedding) != self._dimensions for embedding in embeddings):
            raise RuntimeError("Embedding provider returned an invalid dimension")
        return embeddings
