"""Store vetorial PostgreSQL compatível com pgvector e Supabase."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from os import environ
from typing import Any

from ...domain.entities import DocumentChunk, RetrievedChunk
from ...application.ports import EmbeddingRepository


# /**
#  * Persiste chunks e consulta sua similaridade semântica no PostgreSQL.
#  * Existe para substituir o índice efêmero em memória em ambientes persistentes.
#  * Histórico: v1 — adiciona upsert, filtro por projeto e consulta cosine via pgvector.
#  */
class PostgresVectorStore:
    """Implementa a porta de store com SQL portátil para pgvector e Supabase."""

    def __init__(
        self,
        connection_factory: Callable[[], Any],
        embedding_repository: EmbeddingRepository,
    ) -> None:
        self._connection_factory = connection_factory
        self._embedding_repository = embedding_repository

    # /**
    #  * Cria um store configurado pelas variáveis de ambiente da aplicação.
    #  * Existe para permitir alternar entre memória e PostgreSQL sem mudar os casos de uso.
    #  * Histórico: v1 — aceita DATABASE_URL ou SUPABASE_DB_URL e modelo configurável.
    #  */
    @classmethod
    def from_environment(cls, embedding_repository: EmbeddingRepository) -> "PostgresVectorStore":
        """Monta o adaptador usando a URL de banco configurada."""

        database_url = environ.get("SUPABASE_DB_URL") or environ.get("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL or SUPABASE_DB_URL is required")

        def connect() -> Any:
            import psycopg

            return psycopg.connect(database_url)

        return cls(connect, embedding_repository)

    # /**
    #  * Insere ou atualiza os chunks e seus embeddings em uma transação.
    #  * Existe para tornar a indexação repetível sem duplicar a identidade do chunk.
    #  * Histórico: v1 — grava offsets, projeto, conteúdo e vetor no schema compartilhado.
    #  */
    def upsert(self, chunks: Sequence[DocumentChunk]) -> None:
        """Persiste os chunks no índice vetorial do projeto."""

        with self._connection_factory() as connection:
            with connection.cursor() as cursor:
                embeddings = self._embedding_repository.embed(tuple(chunk.content for chunk in chunks))
                if len(embeddings) != len(chunks):
                    raise ValueError("embedding count must match chunk count")
                for chunk, embedding in zip(chunks, embeddings, strict=True):
                    if not chunk.project_id.strip():
                        raise ValueError("project_id is required")
                    self._validate_dimension(embedding)
                    cursor.execute(
                        """
                        INSERT INTO document_chunks
                            (project_id, document_id, chunk_index, content,
                             start_offset, end_offset, embedding)
                        VALUES (%s, %s, %s, %s, %s, %s, %s::vector)
                        ON CONFLICT (project_id, document_id, chunk_index)
                        DO UPDATE SET content = EXCLUDED.content,
                                      start_offset = EXCLUDED.start_offset,
                                      end_offset = EXCLUDED.end_offset,
                                      embedding = EXCLUDED.embedding
                        """,
                        (
                            chunk.project_id,
                            chunk.document_id,
                            chunk.index,
                            chunk.content,
                            chunk.start_offset,
                            chunk.end_offset,
                            self._vector_literal(embedding),
                        ),
                    )

    # /**
    #  * Recupera somente chunks do projeto e ordena pela distância cosine do pgvector.
    #  * Existe para manter isolamento entre projetos durante a consulta semântica.
    #  * Histórico: v1 — substitui o ranking lexical por busca vetorial persistente.
    #  */
    def search(self, project_id: str, query: str, *, limit: int) -> tuple[RetrievedChunk, ...]:
        """Retorna os chunks semanticamente mais próximos da consulta."""

        embeddings = self._embedding_repository.embed((query,))
        if len(embeddings) != 1:
            raise ValueError("query embedding count must be one")
        embedding = embeddings[0]
        self._validate_dimension(embedding)
        with self._connection_factory() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT document_id, chunk_index, content, start_offset, end_offset,
                           project_id, 1 - (embedding <=> %s::vector) AS score
                    FROM document_chunks
                    WHERE project_id = %s
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                    """,
                    (
                        self._vector_literal(embedding),
                        project_id,
                        self._vector_literal(embedding),
                        limit,
                    ),
                )
                rows = cursor.fetchall()

        return tuple(
            RetrievedChunk(
                chunk=DocumentChunk(
                    document_id=row[0],
                    index=row[1],
                    content=row[2],
                    start_offset=row[3],
                    end_offset=row[4],
                    project_id=row[5],
                ),
                score=float(row[6]),
            )
            for row in rows
        )

    @staticmethod
    def _vector_literal(vector: Sequence[float]) -> str:
        """Serializa o vetor no formato aceito pelo cast `::vector`."""

        return "[" + ",".join(str(value) for value in vector) + "]"

    @staticmethod
    def _validate_dimension(vector: Sequence[float]) -> None:
        """Impede que um modelo incompatível seja gravado silenciosamente."""

        if len(vector) != 384:
            raise ValueError("embedding dimension must be 384")
