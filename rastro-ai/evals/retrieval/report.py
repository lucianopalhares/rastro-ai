"""Monta um relatório estruturado e independente de qualquer plataforma de observabilidade."""

from __future__ import annotations

from collections.abc import Mapping
from os import environ
from typing import Any

from .evaluate import EvaluationResult

REPORT_SCHEMA = "rastro-ai.retrieval-report.v1"


# /**
#  * Converte uma métrica agregada em score portátil para ferramentas futuras.
#  * Existe para manter nome, valor e tipo explícitos sem depender do SDK do Langfuse.
#  * Histórico: 026-v18 — cria o contrato de scores preparado para observabilidade.
#  */
def _score_records(metrics: Mapping[str, float]) -> list[dict[str, Any]]:
    """Retorna scores numéricos com formato estável para cada métrica."""

    return [
        {"name": name, "value": value, "data_type": "NUMERIC"}
        for name, value in metrics.items()
    ]


# /**
#  * Identifica problemas compreensíveis em um caso individual.
#  * Existe para que o relatório mostre por que um caso merece investigação sem exigir leitura
#  * do JSON inteiro ou de um painel externo.
#  * Histórico: 026-v18 — adiciona diagnóstico amigável por caso.
#  */
def _failure_reasons(case: Mapping[str, Any]) -> list[str]:
    """Retorna códigos de falha determinísticos para um caso do relatório."""

    returned = case["returned_chunks"]
    expected = case["expected_chunks"]
    reasons: list[str] = []
    relevant_positions = [
        position
        for position, chunk_id in enumerate(returned, start=1)
        if chunk_id in expected
    ]
    if expected and not relevant_positions:
        reasons.append("missing_relevant_chunk")
    elif relevant_positions and relevant_positions[0] > 1:
        reasons.append("relevant_chunk_below_top")
    if not expected and returned:
        reasons.append("returned_without_expected_evidence")
    if case["project_isolation"] != 1.0:
        reasons.append("project_isolation_failed")
    if case["score_ordering"] != 1.0:
        reasons.append("score_ordering_failed")
    return reasons


# /**
#  * Organiza uma execução em um contrato próprio para terminal, arquivo ou observabilidade.
#  * Existe para separar o cálculo das métricas do formato de apresentação e de uma futura
#  * integração com Langfuse, preservando o golden e os diagnósticos por caso.
#  * Histórico: 026-v18 — cria relatório com resumo, scores, falhas e casos.
#  */
def build_report(
    result: EvaluationResult,
    dataset: Mapping[str, Any],
    ks: tuple[int, ...],
) -> dict[str, Any]:
    """Retorna o relatório completo sem enviar dados para nenhuma plataforma externa."""

    case_inputs = {case["id"]: case for case in dataset["cases"]}
    report_cases: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for case in result.cases:
        source = case_inputs[case["id"]]
        reasons = _failure_reasons(case)
        returned = [
            {"rank": rank, "chunk_id": chunk_id, "score": case["scores"][rank - 1]}
            for rank, chunk_id in enumerate(case["returned_chunks"], start=1)
        ]
        record = {
            "id": case["id"],
            "input": {
                "project_id": source["project_id"],
                "query": source["query"],
            },
            "expected": {
                "chunk_ids": case["expected_chunks"],
                "answer": source.get("expected_answer"),
            },
            "retrieval": {
                "returned_chunks": returned,
                "project_isolation": case["project_isolation"],
                "score_ordering": case["score_ordering"],
            },
            "scores": _score_records(case["metrics"]),
            "diagnostics": {
                "status": "failed" if reasons else "passed",
                "failure_reasons": reasons,
            },
        }
        report_cases.append(record)
        if reasons:
            failures.append(
                {
                    "case_id": case["id"],
                    "reasons": reasons,
                    "expected_chunk_ids": case["expected_chunks"],
                    "returned_chunk_ids": case["returned_chunks"],
                }
            )

    run = {
        "type": "retrieval",
        "dataset": {
            "schema": dataset.get("schema"),
            "version": dataset.get("version"),
        },
        "ks": list(ks),
        "retriever": {
            "backend": environ.get("VECTOR_STORE_BACKEND", "postgres"),
            "collection": environ.get("PGVECTOR_COLLECTION", "rastro_document_chunks"),
            "embedding_model": environ.get("EMBEDDING_MODEL", "unknown"),
        },
    }
    return {
        "schema": REPORT_SCHEMA,
        "run": run,
        "summary": {
            "status": "observed",
            "case_count": result.case_count,
            "answerable_case_count": result.answerable_case_count,
            "no_answer_case_count": result.no_answer_case_count,
            "failure_count": len(failures),
            "metrics": result.metrics,
        },
        "scores": _score_records(result.metrics),
        "quality": {
            "status": "not_evaluated",
            "thresholds": {},
            "checks": [],
        },
        "failures": failures,
        "cases": report_cases,
    }
