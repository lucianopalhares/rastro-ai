"""Serviços puros para normalização e divisão do texto de documentos."""

from __future__ import annotations

import re
from functools import lru_cache

from .entities import DocumentChunk


def normalize_text(text: str) -> str:
    """Normaliza finais de linha e espaços sem alterar o conteúdo semântico."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    normalized = "\n".join(line.rstrip() for line in normalized.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", normalized).strip()


def _find_chunk_end(text: str, start: int, chunk_size: int) -> int:
    """Prefere terminar em espaço sem deixar um chunk curto demais."""

    limit = min(start + chunk_size, len(text))
    if limit == len(text):
        return limit

    boundary = text.rfind(" ", start + chunk_size // 2, limit)
    return boundary if boundary > start else limit


# /**
#  * Divide texto em blocos estruturais e retorna os limites possíveis de corte.
#  * Existe para privilegiar parágrafos e títulos antes de cortar por orçamento de tokens.
#  * Histórico: v2 — adiciona fronteiras semânticas determinísticas para Markdown e texto.
#  */
def _find_structural_boundaries(text: str) -> tuple[int, ...]:
    boundaries = {len(text)}
    boundaries.update(match.end() for match in re.finditer(r"\n\n+", text))
    boundaries.update(
        match.start() for match in re.finditer(r"(?m)^#{1,6}\s+\S.*$", text) if match.start() > 0
    )
    return tuple(sorted(boundaries))


# /**
#  * Retorna o tokenizer compatível com o modelo de embedding configurado.
#  * Existe para contar tokens reais sem acoplar o domínio ao ciclo de vida do cliente OpenAI.
#  * Histórico: v4 — adiciona `tiktoken` para o orçamento de chunks.
#  */
@lru_cache(maxsize=1)
def _get_token_encoding():
    """Carrega uma vez o encoding usado pelo `text-embedding-3-small`."""

    import tiktoken

    return tiktoken.encoding_for_model("text-embedding-3-small")


# /**
#  * Converte tokens em intervalos de caracteres sem quebrar o texto normalizado.
#  * Histórico: v4 — deriva limites de chunk a partir dos bytes dos tokens reais.
#  */
def _find_token_spans(text: str) -> tuple[tuple[int, int], ...]:
    encoding = _get_token_encoding()
    encoded_text = text.encode("utf-8")
    token_spans: list[tuple[int, int]] = []
    byte_start = 0
    for token in encoding.encode(text, disallowed_special=()):
        byte_end = byte_start + len(encoding.decode_single_token_bytes(token))
        start = len(encoded_text[:byte_start].decode("utf-8", errors="ignore"))
        end = len(encoded_text[:byte_end].decode("utf-8", errors="ignore"))
        if end > start:
            token_spans.append((start, end))
        byte_start = byte_end
    return tuple(token_spans)


# /**
#  * Divide o texto usando orçamento aproximado de tokens e sobreposição por tokens.
#  * Existe para manter parágrafos/seções inteiros sempre que couberem no chunk.
#  * Histórico: v2 — cria o chunking estrutural padrão sem tokenizer externo.
#  * Histórico: v4 — passa a contar tokens com `tiktoken`.
#  */
def _chunk_text_by_tokens(
    text: str,
    *,
    document_id: str,
    project_id: str,
    max_tokens: int,
    overlap_tokens: int,
) -> tuple[DocumentChunk, ...]:
    token_spans = _find_token_spans(text)
    boundaries = _find_structural_boundaries(text)
    chunks: list[DocumentChunk] = []
    start = 0

    while start < len(text):
        start_token = next(
            (index for index, token in enumerate(token_spans) if token[1] > start),
            len(token_spans),
        )
        if start_token == len(token_spans):
            break
        target_token = min(start_token + max_tokens, len(token_spans))
        target_end = token_spans[target_token - 1][1]
        structural_ends = [
            boundary for boundary in boundaries if start < boundary <= target_end
        ]
        raw_end = max(structural_ends, default=target_end)
        content_start = start
        while content_start < raw_end and text[content_start].isspace():
            content_start += 1
        content_end = raw_end
        while content_end > content_start and text[content_end - 1].isspace():
            content_end -= 1

        if content_start < content_end:
            chunks.append(
                DocumentChunk(
                    document_id=document_id,
                    index=len(chunks),
                    content=text[content_start:content_end],
                    start_offset=content_start,
                    end_offset=content_end,
                    project_id=project_id,
                )
            )

        if raw_end >= len(text):
            break
        next_heading = next(
            (
                boundary
                for boundary in boundaries
                if boundary > raw_end
                and text[boundary : boundary + 1] == "#"
                and not text[raw_end:boundary].strip()
            ),
            None,
        )
        if next_heading is not None:
            start = next_heading
        elif raw_end in boundaries:
            start = raw_end
        else:
            end_token = next(
                (index for index, token in enumerate(token_spans) if token[1] > content_end),
                len(token_spans),
            )
            next_token = max(start_token + 1, end_token - overlap_tokens)
            start = token_spans[next_token][0] if next_token < len(token_spans) else len(text)

    return tuple(chunks)


# /**
#  * Divide texto normalizado em chunks reproduzíveis associados a um projeto.
#  * Histórico: v1 — propaga `project_id` sem alterar offsets, tamanho ou sobreposição.
#  * Histórico: v2 — usa chunking estrutural por tokens quando os parâmetros legados não são usados.
#  */
def chunk_text(
    text: str,
    *,
    document_id: str,
    project_id: str = "",
    chunk_size: int | None = None,
    overlap: int | None = None,
    max_tokens: int = 500,
    overlap_tokens: int = 60,
) -> tuple[DocumentChunk, ...]:
    """Divide texto por estrutura e tokens, preservando offsets e sobreposição."""

    normalized = normalize_text(text)
    if not normalized:
        raise ValueError("Document text is required")

    if chunk_size is None:
        if max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        if overlap_tokens < 0 or overlap_tokens >= max_tokens:
            raise ValueError("overlap_tokens must be between zero and max_tokens")
        return _chunk_text_by_tokens(
            normalized,
            document_id=document_id,
            project_id=project_id,
            max_tokens=max_tokens,
            overlap_tokens=overlap_tokens,
        )

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    legacy_overlap = 0 if overlap is None else overlap
    if legacy_overlap < 0 or legacy_overlap >= chunk_size:
        raise ValueError("overlap must be between zero and chunk_size")

    chunks: list[DocumentChunk] = []
    start = 0
    while start < len(normalized):
        raw_end = _find_chunk_end(normalized, start, chunk_size)
        content_start = start
        while content_start < raw_end and normalized[content_start].isspace():
            content_start += 1
        content_end = raw_end
        while content_end > content_start and normalized[content_end - 1].isspace():
            content_end -= 1

        if content_start < content_end:
            chunks.append(
                DocumentChunk(
                    document_id=document_id,
                    index=len(chunks),
                    content=normalized[content_start:content_end],
                    start_offset=content_start,
                    end_offset=content_end,
                    project_id=project_id,
                )
            )

        if raw_end == len(normalized):
            break

        next_start = max(content_end - legacy_overlap, content_start + 1)
        while next_start < len(normalized) and normalized[next_start].isspace():
            next_start += 1
        start = next_start

    return tuple(chunks)
