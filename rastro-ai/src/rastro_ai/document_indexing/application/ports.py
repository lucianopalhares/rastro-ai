"""Portas que isolam o caso de uso dos adaptadores de infraestrutura."""

from pathlib import Path
from typing import Protocol


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
