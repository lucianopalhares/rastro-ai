"""Adaptador LangChain para o contrato de chunking da aplicação."""

from __future__ import annotations

from typing import Callable

from langchain_text_splitters import RecursiveCharacterTextSplitter

from ...application.ports import TextChunker
from ...domain.entities import DocumentChunk
from ...domain.services import _get_token_encoding, normalize_text


# /**
#  * Implementa `TextChunker` com `RecursiveCharacterTextSplitter`.
#  * Existe para manter LangChain na infraestrutura e converter seus documentos
#  * para `DocumentChunk`, preservando offsets e metadados do domínio.
#  * Histórico: v2 — cria o adaptador com contagem real de tokens e offsets relativos.
#  */
class LangChainTextChunker:
    """Divide texto normalizado usando a estratégia recursiva do LangChain."""

    # /**
    #  * Divide um documento e reconstrói entidades do domínio a partir dos metadados.
    #  * A contagem de tokens usa o encoding do embedding quando o modo padrão é usado;
    #  * o modo legado mantém limites em caracteres para preservar sua API existente.
    #  * Histórico: v2 — adiciona validação, offsets e numeração determinística.
    #  */
    def chunk(
        self,
        text: str,
        *,
        document_id: str,
        project_id: str = "",
        chunk_size: int | None = None,
        overlap: int | None = None,
        max_tokens: int = 500,
        overlap_tokens: int = 60,
    ) -> tuple[DocumentChunk, ...]:
        # Padroniza o texto antes de dividi-lo em partes menores.
        normalized = normalize_text(text)
        if not normalized:
            raise ValueError("Document text is required")

        if chunk_size is not None:
            # Usa caracteres quando a chamada segue o formato antigo da aplicação.
            if chunk_size <= 0:
                raise ValueError("chunk_size must be positive")
            legacy_overlap = 0 if overlap is None else overlap
            if legacy_overlap < 0 or legacy_overlap >= chunk_size:
                raise ValueError("overlap must be between zero and chunk_size")
            splitter_size = chunk_size
            splitter_overlap = legacy_overlap
            length_function: Callable[[str], int] = len
        else:
            # Usa tokens quando a chamada segue a configuração padrão de embeddings.
            if max_tokens <= 0:
                raise ValueError("max_tokens must be positive")
            if overlap_tokens < 0 or overlap_tokens >= max_tokens:
                raise ValueError("overlap_tokens must be between zero and max_tokens")
            splitter_size = max_tokens
            splitter_overlap = overlap_tokens
            encoding = _get_token_encoding()
            length_function = lambda value: len(encoding.encode(value, disallowed_special=()))

        # Divide o texto em partes menores, preservando parágrafos e limites configurados.
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=splitter_size,
            chunk_overlap=splitter_overlap,
            length_function=length_function,
            add_start_index=True,
            keep_separator=False,
        )
        # Pede ao LangChain os documentos menores que formarão os chunks.
        documents = splitter.create_documents([normalized])

        chunks: list[DocumentChunk] = []
        search_start = 0
        # Converte cada documento do LangChain para a entidade usada pela Rastro.
        for index, document in enumerate(documents):
            content = document.page_content
            start_offset = int(document.metadata.get("start_index", -1))
            if start_offset < 0 or normalized[start_offset : start_offset + len(content)] != content:
                # Recalcula a posição quando o LangChain não consegue informar um offset válido.
                start_offset = normalized.find(content, search_start)
            if start_offset < 0:
                raise ValueError("LangChain chunk offset could not be resolved")
            end_offset = start_offset + len(content)
            # Guarda conteúdo, posição e identificação do projeto no formato do domínio.
            chunks.append(
                DocumentChunk(
                    document_id=document_id,
                    index=index,
                    content=content,
                    start_offset=start_offset,
                    end_offset=end_offset,
                    project_id=project_id,
                )
            )
            search_start = start_offset + 1
        return tuple(chunks)


__all__ = ["LangChainTextChunker"]
