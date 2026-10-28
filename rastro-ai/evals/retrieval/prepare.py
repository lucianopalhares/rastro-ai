"""Prepara uma coleção PGVector isolada a partir do corpus do golden dataset."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from os import environ
from pathlib import Path
from typing import Any

from rastro_ai.document_indexing.domain.entities import DocumentChunk
from rastro_ai.indexing import chunk_text
from rastro_ai.retrieval import persist_document_chunks

from .evaluate import DATASET_PATH, load_dataset


# /**
#  * Gera os chunks do corpus declarado no golden dataset.
#  * Existe para que a avaliação integrada use o mesmo chunker da aplicação e mantenha IDs,
#  * projetos e respostas esperadas compatíveis com o banco de avaliação.
#  * Histórico: 026-v15 — cria a preparação reproduzível do corpus integrado.
#  */
def build_evaluation_chunks(dataset: dict[str, Any]) -> tuple[DocumentChunk, ...]:
    """Transforma os documentos do golden em chunks indexáveis e valida suas referências."""

    chunks: list[DocumentChunk] = []
    seen_documents: dict[tuple[str, str], str] = {}
    available_chunk_ids: set[str] = set()

    for case in dataset["cases"]:
        documents = case.get("documents")
        if not isinstance(documents, list) or not documents:
            raise ValueError(f"{case['id']}: documents must be a non-empty list")
        expected_answer = case.get("expected_answer")
        if not isinstance(expected_answer, dict):
            raise ValueError(f"{case['id']}: expected_answer is required")
        if not isinstance(expected_answer.get("abstain"), bool):
            raise ValueError(f"{case['id']}: expected_answer.abstain must be boolean")
        source_ids = expected_answer.get("source_document_ids", [])
        if not isinstance(source_ids, list) or not all(isinstance(value, str) for value in source_ids):
            raise ValueError(f"{case['id']}: expected_answer.source_document_ids must be a list of strings")

        case_document_ids: set[str] = set()
        for document in documents:
            if not isinstance(document, dict):
                raise ValueError(f"{case['id']}: every document must be an object")
            document_id = document.get("id")
            text = document.get("text")
            if not isinstance(document_id, str) or not document_id.strip():
                raise ValueError(f"{case['id']}: document id is required")
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f"{case['id']}: document text is required")
            project_id = document.get("project_id", case["project_id"])
            if not isinstance(project_id, str) or not project_id.strip():
                raise ValueError(f"{case['id']}: document project_id is required")
            case_document_ids.add(document_id)
            key = (project_id, document_id)
            previous_text = seen_documents.get(key)
            if previous_text is not None:
                if previous_text != text:
                    raise ValueError(f"document content differs for {project_id}/{document_id}")
                continue
            document_chunks = chunk_text(text, document_id=document_id, project_id=project_id)
            chunks.extend(document_chunks)
            available_chunk_ids.update(f"{chunk.document_id}:{chunk.index}" for chunk in document_chunks)
            seen_documents[key] = text

        if not set(source_ids).issubset(case_document_ids):
            raise ValueError(f"{case['id']}: expected answer source is not present in documents")
        expected_chunk_ids = {item["chunk_id"] for item in case.get("relevant_chunks", [])}
        if not expected_chunk_ids.issubset(available_chunk_ids):
            missing = sorted(expected_chunk_ids - available_chunk_ids)
            raise ValueError(f"{case['id']}: relevant chunks are not present in corpus: {missing}")

    return tuple(chunks)


# /**
#  * Persiste o corpus do golden na coleção configurada para evaluation.
#  * Existe para separar documentos controlados dos dados de desenvolvimento e tornar a execução
#  * integrada idempotente, pois o vector store usa IDs determinísticos para upsert.
#  * Histórico: 026-v15 — adiciona a preparação do índice real de evaluation.
#  */
def prepare_index(
    dataset: dict[str, Any],
    persist: Callable[[tuple[DocumentChunk, ...]], None] = persist_document_chunks,
) -> int:
    """Gera e persiste o corpus, retornando a quantidade de chunks preparados."""

    chunks = build_evaluation_chunks(dataset)
    persist(chunks)
    return len(chunks)


# /**
#  * Executa a preparação do corpus pelo container de evaluation.
#  * Existe para oferecer um comando explícito antes da consulta real, sem misturar indexação
#  * de fixtures com o processo que calcula as métricas.
#  * Histórico: 026-v15 — adiciona o comando de preparação do banco de evaluation.
#  */
def main() -> None:
    """Lê o golden, indexa seu corpus e imprime um resumo da preparação."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DATASET_PATH)
    arguments = parser.parse_args()
    dataset = load_dataset(arguments.dataset)
    chunk_count = prepare_index(dataset)
    print(
        json.dumps(
            {
                "dataset": str(arguments.dataset),
                "collection": environ.get("PGVECTOR_COLLECTION", "rastro_document_chunks"),
                "case_count": len(dataset["cases"]),
                "chunk_count": chunk_count,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
