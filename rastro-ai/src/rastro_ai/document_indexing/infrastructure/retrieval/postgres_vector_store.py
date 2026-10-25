"""Adapter LangChain para persistência e busca em PostgreSQL/pgvector."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from os import environ
from typing import Any

from langchain_core.embeddings import Embeddings
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import DistanceStrategy

from ...application.ports import EmbeddingRepository
from ...domain.entities import DocumentChunk, RetrievedChunk


# /**
#  * Adapta o contrato local de embeddings à interface esperada pelo PGVector.
#  * Existe para manter o provider e as validações da Rastro independentes do vector store.
#  * Histórico: v6 — cria a ponte entre `EmbeddingRepository` e `Embeddings`.
#  */
class RepositoryEmbeddings(Embeddings):
    """Expõe embeddings da aplicação para as operações do LangChain PGVector."""

    def __init__(self, repository: EmbeddingRepository) -> None:
        self._repository = repository

    # /**
    #  * Gera vetores em lote preservando a ordem definida pelo contrato local.
    #  * Histórico: v6 — implementa a operação de documentos do LangChain.
    #  */
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [list(embedding) for embedding in self._repository.embed(tuple(texts))]

    # /**
    #  * Gera o vetor de uma consulta usando o mesmo provider dos documentos.
    #  * Histórico: v6 — implementa a operação de consulta do LangChain.
    #  */
    def embed_query(self, text: str) -> list[float]:
        embeddings = self._repository.embed((text,))
        if len(embeddings) != 1:
            raise ValueError("query embedding count must be one")
        return list(embeddings[0])


# /**
#  * Persiste e consulta chunks usando o vector store PGVector do LangChain.
#  * Existe para adotar a integração padrão sem expor `Document` ou metadata aos casos de uso.
#  * Histórico: v1 — adiciona upsert, filtro por projeto e consulta cosine via pgvector.
#  * Histórico: v6 — delega persistência e similaridade a `langchain-postgres`.
#  */
class PostgresVectorStore:
    """Implementa a porta local sobre o vector store PGVector."""

    def __init__(self, vector_store: Any, embedding_repository: EmbeddingRepository) -> None:
        self._vector_store = vector_store
        self._embedding_repository = embedding_repository

    # /**
    #  * Cria o adapter LangChain com a conexão e coleção configuradas pelo processo.
    #  * A biblioteca cria suas tabelas se necessário, enquanto o adapter mantém os metadados
    #  * obrigatórios da Rastro em cada documento persistido.
    #  * Histórico: v1 — aceita DATABASE_URL ou SUPABASE_DB_URL e modelo configurável.
    #  * Histórico: v6 — cria `PGVector` com dimensão e distância cosine explícitas.
    #  */
    @classmethod
    def from_environment(cls, embedding_repository: EmbeddingRepository) -> "PostgresVectorStore":
        """Monta o adapter usando a URL de banco e a coleção do ambiente."""

        database_url = environ.get("SUPABASE_DB_URL") or environ.get("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL or SUPABASE_DB_URL is required")

        vector_store = PGVector(
            embeddings=RepositoryEmbeddings(embedding_repository),
            connection=database_url,
            collection_name=environ.get("PGVECTOR_COLLECTION", "rastro_document_chunks"),
            embedding_length=384,
            distance_strategy=DistanceStrategy.COSINE,
            create_extension=False,
        )
        return cls(vector_store, embedding_repository)

    # /**
    #  * Insere ou atualiza chunks com IDs determinísticos e metadata completa.
    #  * O ID preserva a idempotência por projeto, documento e índice; a validação local
    #  * impede gravar chunks sem isolamento ou vetores incompatíveis.
    #  * Histórico: v1 — grava offsets, projeto, conteúdo e vetor no schema compartilhado.
    #  * Histórico: v6 — usa `PGVector.add_embeddings` com metadata e IDs estáveis.
    #  */
    def upsert(self, chunks: Sequence[DocumentChunk]) -> None:
        """Persiste os chunks no índice vetorial da coleção configurada."""

        if not chunks:
            return
        texts = tuple(chunk.content for chunk in chunks)
        embeddings = self._embedding_repository.embed(texts)
        if len(embeddings) != len(chunks):
            raise ValueError("embedding count must match chunk count")

        metadatas: list[dict[str, Any]] = []
        ids: list[str] = []
        for index, chunk in enumerate(chunks):
            if not chunk.project_id.strip():
                raise ValueError("project_id is required")
            self._validate_dimension(embeddings[index])
            metadatas.append(
                {
                    "project_id": chunk.project_id,
                    "document_id": chunk.document_id,
                    "chunk_index": chunk.index,
                    "start_offset": chunk.start_offset,
                    "end_offset": chunk.end_offset,
                }
            )
            ids.append(self._chunk_id(chunk))

        self._vector_store.add_embeddings(
            texts=list(texts),
            embeddings=[list(embedding) for embedding in embeddings],
            metadatas=metadatas,
            ids=ids,
        )

    # /**
    #  * Recupera somente chunks do projeto e converte documentos LangChain em entidades locais.
    #  * O filtro de metadata é sempre aplicado pelo adapter, nunca pelo chamador, protegendo o
    #  * isolamento multi-projeto e preservando score, offsets e identidade das citações.
    #  * Histórico: v1 — substitui o ranking lexical por busca vetorial persistente.
    #  * Histórico: v6 — usa `similarity_search_with_score_by_vector` e filtro obrigatório.
    #  */
    def search(self, project_id: str, query: str, *, limit: int) -> tuple[RetrievedChunk, ...]:
        """Retorna os chunks semanticamente mais próximos do projeto informado."""

        if not project_id.strip():
            raise ValueError("project_id is required")
        if limit <= 0:
            raise ValueError("limit must be positive")
        embeddings = self._embedding_repository.embed((query,))
        if len(embeddings) != 1:
            raise ValueError("query embedding count must be one")
        self._validate_dimension(embeddings[0])
        results = self._vector_store.similarity_search_with_score_by_vector(
            embedding=list(embeddings[0]),
            k=limit,
            filter={"project_id": project_id},
        )

        retrieved: list[RetrievedChunk] = []
        for document, distance in results:
            metadata = document.metadata
            if metadata.get("project_id") != project_id:
                continue
            retrieved.append(
                RetrievedChunk(
                    chunk=DocumentChunk(
                        document_id=str(metadata["document_id"]),
                        index=int(metadata["chunk_index"]),
                        content=document.page_content,
                        start_offset=int(metadata["start_offset"]),
                        end_offset=int(metadata["end_offset"]),
                        project_id=str(metadata["project_id"]),
                    ),
                    score=1.0 - float(distance),
                )
            )
        return tuple(retrieved)

    # /**
    #  * Cria um ID estável para que a reindexação atualize o mesmo chunk.
    #  * Histórico: v6 — substitui a chave composta do SQL por um ID determinístico do adapter.
    #  */
    @staticmethod
    def _chunk_id(chunk: DocumentChunk) -> str:
        value = "\x1f".join((chunk.project_id, chunk.document_id, str(chunk.index)))
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    # /**
    #  * Impede que um embedding incompatível seja gravado silenciosamente.
    #  * Histórico: v1 — valida dimensão fixa do schema pgvector.
    #  * Histórico: v6 — preserva a validação antes da chamada ao PGVector.
    #  */
    @staticmethod
    def _validate_dimension(vector: Sequence[float]) -> None:
        if len(vector) != 384:
            raise ValueError("embedding dimension must be 384")
