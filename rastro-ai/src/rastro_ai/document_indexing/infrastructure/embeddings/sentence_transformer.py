"""Embedding local baseado em Sentence Transformers."""

from __future__ import annotations

from threading import Lock


# /**
#  * Gera embeddings locais multilíngues para documentos e consultas.
#  * Existe para manter a busca semântica executável sem um provedor externo.
#  * Histórico: v1 — adiciona o modelo multilíngue de 384 dimensões compatível com o schema.
#  */
class SentenceTransformerEmbeddingProvider:
    """Carrega o modelo sob demanda e reutiliza-o no processo."""

    _model_lock = Lock()
    _models: dict[str, object] = {}

    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2") -> None:
        self._model_name = model_name

    # /**
    #  * Converte o texto em uma tupla de floats com dimensão estável.
    #  * Existe para compartilhar exatamente o mesmo espaço vetorial entre upsert e busca.
    #  * Histórico: v1 — normaliza o retorno do Sentence Transformer para o contrato da aplicação.
    #  */
    def embed(self, text: str) -> tuple[float, ...]:
        """Gera um embedding normalizado para o texto."""

        model = self._get_model()
        vector = model.encode(text, normalize_embeddings=True)
        return tuple(float(value) for value in vector.tolist())

    def _get_model(self) -> object:
        """Carrega o modelo uma vez por nome para reduzir latência após o primeiro uso."""

        with self._model_lock:
            if self._model_name not in self._models:
                from sentence_transformers import SentenceTransformer

                self._models[self._model_name] = SentenceTransformer(self._model_name)
            return self._models[self._model_name]
