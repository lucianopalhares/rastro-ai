"""Entidades do domínio de indexação de documentos."""

from dataclasses import dataclass


# /**
#  * Identifica um trecho indexável, sua posição e o projeto proprietário.
#  * Existe para preservar offsets e permitir isolamento no retrieval.
#  * Histórico: v1 — adiciona `project_id` com valor vazio compatível com chamadas anteriores.
#  */
@dataclass(frozen=True, slots=True)
class DocumentChunk:
    """Representa um trecho indexável e sua posição no texto normalizado."""

    document_id: str
    index: int
    content: str
    start_offset: int
    end_offset: int
    project_id: str = ""


# /**
#  * Carrega um chunk encontrado e sua relevância calculada pelo store.
#  * Existe para separar o conteúdo retornado do score usado no ranking.
#  * Histórico: v1 — adiciona o contrato mínimo de resultado do retrieval.
#  */
@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    """Representa um chunk recuperado com sua similaridade determinística."""

    chunk: DocumentChunk
    score: float
