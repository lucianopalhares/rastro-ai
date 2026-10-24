"""Portas que isolam o caso de uso dos adaptadores de infraestrutura."""

from pathlib import Path
from typing import Protocol, Sequence

from ..domain.entities import DocumentChunk, RetrievedChunk


class TextExtractor(Protocol):
    """Contrato para adaptadores que extraem texto de uma origem."""

    def extract(self, path: str | Path) -> str:
        """Retorna o texto normalizado de uma origem suportada."""


class TextChunker(Protocol):
    """Contrato para a política de divisão de texto do domínio."""

    def chunk(
        self,
        text: str,
        *,
        document_id: str,
        chunk_size: int,
        overlap: int,
    ) -> tuple[object, ...]:
        """Retorna os chunks produzidos para um documento."""


# /**
#  * Define a persistência mínima necessária para indexar e consultar chunks.
#  * Existe para manter o caso de uso independente de embeddings e banco concretos.
#  * Histórico: v1 — adiciona indexação e busca filtradas por projeto.
#  */
class VectorStore(Protocol):
    """Contrato de armazenamento vetorial usado pela aplicação."""

    # /** Histórico: v1 — define a operação de indexação do store. */
    def upsert(self, chunks: Sequence[DocumentChunk]) -> None:
        """Insere ou substitui chunks indexáveis."""

    # /** Histórico: v1 — define a consulta limitada e filtrada por projeto. */
    def search(
        self,
        project_id: str,
        query: str,
        *,
        limit: int,
    ) -> tuple[RetrievedChunk, ...]:
        """Retorna os chunks mais relevantes dentro de um projeto."""
