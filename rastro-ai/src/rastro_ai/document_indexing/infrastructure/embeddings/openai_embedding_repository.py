"""Repositório de embeddings usando a API externa da OpenAI."""

from __future__ import annotations

import os
from collections.abc import Sequence

import tiktoken
from langchain_openai import OpenAIEmbeddings

from ....observability import observe_operation, update_observation


# /**
#  * Implementa o contrato de embeddings sobre o endpoint externo da OpenAI.
#  * Existe para manter o domínio e o PostgreSQL independentes do fornecedor escolhido.
#  * Histórico: v2 — adiciona `text-embedding-3-small` em lote com dimensão configurável.
#  * Histórico: v5 — usa `OpenAIEmbeddings` do LangChain atrás do contrato local.
#  * Histórico: 025-v1 — registra tokens e custo opcional no observation de embedding.
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
        tokenizer_model: str | None = None,
        cost_per_input_token: float | None = None,
    ) -> None:
        self._model = model
        self._dimensions = dimensions
        self._tokenizer_model = tokenizer_model or model
        self._cost_per_input_token = cost_per_input_token
        if cost_per_input_token is not None and cost_per_input_token < 0:
            raise ValueError("cost_per_input_token must be non-negative")
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
            tokenizer_model=os.environ.get("EMBEDDING_TOKENIZER_MODEL") or None,
            cost_per_input_token=cls._read_cost_per_input_token(),
        )

    # /**
    #  * Lê o preço opcional por token sem tornar custo uma dependência do runtime.
    #  * Existe para permitir preços privados ou modelos não cadastrados no Langfuse.
    #  * Histórico: 025-v1 — adiciona fallback de custo direto configurável.
    #  */
    @staticmethod
    def _read_cost_per_input_token() -> float | None:
        """Retorna o preço configurado ou `None` para deixar o Langfuse inferir."""

        raw_value = os.environ.get("LANGFUSE_EMBEDDING_INPUT_COST_PER_TOKEN", "").strip()
        if not raw_value:
            return None
        try:
            value = float(raw_value)
        except ValueError:
            return None
        return value if value >= 0 else None

    # /**
    #  * Conta tokens localmente para alimentar usage do Langfuse sem enviar texto.
    #  * Existe para manter a contagem disponível quando o adapter LangChain retorna apenas vetores.
    #  * Histórico: 025-v1 — adiciona tokenizer local tolerante a modelos desconhecidos.
    #  */
    def _count_input_tokens(self, texts: Sequence[str]) -> int | None:
        """Conta tokens com o tokenizer do modelo ou retorna `None` se ele não for conhecido."""

        try:
            encoding = tiktoken.encoding_for_model(self._tokenizer_model)
        except (KeyError, ValueError):
            return None
        return sum(len(encoding.encode(text)) for text in texts)

    # /**
    #  * Monta detalhes de custo direto quando um preço privado foi configurado.
    #  * Existe para complementar o custo inferido por definições de modelo do Langfuse.
    #  * Histórico: 025-v1 — calcula custo apenas sobre tokens de entrada.
    #  */
    def _cost_details(self, token_count: int | None) -> dict[str, float] | None:
        """Retorna custo em USD por tipo de uso, quando há preço direto configurado."""

        if token_count is None or self._cost_per_input_token is None:
            return None
        cost = token_count * self._cost_per_input_token
        return {"input": cost, "total": cost}

    # /**
    #  * Solicita embeddings em lote pelo adaptador LangChain e valida sua resposta.
    #  * Histórico: v2 — envia modelo, dimensão e formato float para o contrato OpenAI.
    #  * Histórico: v5 — delega transporte, batching e retries a `OpenAIEmbeddings`.
    #  */
    def embed(self, texts: Sequence[str]) -> tuple[tuple[float, ...], ...]:
        """Retorna embeddings na mesma ordem dos textos enviados."""

        if not texts or any(not text.strip() for text in texts):
            raise ValueError("embedding texts are required")
        input_token_count = self._count_input_tokens(texts)
        with observe_operation(
            name="embedding-generation",
            observation_type="embedding",
            model=self._model,
            input_metadata={
                "model": self._model,
                "dimensions": self._dimensions,
                "itemCount": len(texts),
            },
        ) as observation:
            values = self._embeddings.embed_documents(list(texts))
            update_fields: dict[str, object] = {
                "output": {"dimensions": self._dimensions, "itemCount": len(values)},
                "metadata": {"model": self._model},
            }
            if input_token_count is not None:
                update_fields["usage_details"] = {
                    "input": input_token_count,
                    "total": input_token_count,
                }
            cost_details = self._cost_details(input_token_count)
            if cost_details is not None:
                update_fields["cost_details"] = cost_details
            update_observation(
                observation,
                **update_fields,
            )
        if len(values) != len(texts):
            raise RuntimeError("Embedding provider returned an invalid item count")
        embeddings = tuple(tuple(float(value) for value in embedding) for embedding in values)
        if any(len(embedding) != self._dimensions for embedding in embeddings):
            raise RuntimeError("Embedding provider returned an invalid dimension")
        return embeddings
