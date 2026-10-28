"""Monta um relatório estruturado e independente de qualquer plataforma de observabilidade."""

from __future__ import annotations

from collections.abc import Mapping
from os import environ
from typing import Any

from .evaluate import EvaluationResult

REPORT_SCHEMA = "rastro-ai.retrieval-report.v1"

RANKING_METRIC_PREFIXES = (
    "hit_rate_at_",
    "recall_at_",
    "precision_at_",
    "ndcg_at_",
)
INVARIANT_METRICS = {"project_isolation", "score_ordering", "abstention"}
OPERATIONAL_METRICS = {
    "retrieval_latency_ms",
    "retrieval_latency_p95_ms",
    "retrieval_error_rate",
    "empty_result_rate",
}


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
#  * Seleciona as métricas que devem aparecer no relatório.
#  * Existe para permitir uma visão resumida ou uma análise isolada sem alterar o cálculo
#  * completo do evaluator nem deixar de executar as invariantes de segurança.
#  * Histórico: 027-v8 — adiciona seleção por métrica e por grupo.
#  */
def _select_metric_names(
    metrics: Mapping[str, float], selection: str,
) -> list[str]:
    """Retorna as métricas selecionadas e rejeita nomes desconhecidos."""

    available = list(metrics)
    tokens = [token.strip().lower() for token in selection.split(",") if token.strip()]
    if not tokens or tokens == ["all"]:
        return available

    selected: set[str] = set()
    unknown: list[str] = []
    for token in tokens:
        if token == "ranking":
            selected.update(
                name
                for name in available
                if name == "mrr" or name.startswith(RANKING_METRIC_PREFIXES)
            )
        elif token == "invariants":
            selected.update(name for name in available if name in INVARIANT_METRICS)
        elif token == "operational":
            selected.update(name for name in available if name in OPERATIONAL_METRICS)
        else:
            normalized = token.replace("@", "_at_")
            if normalized.startswith("hit_at_"):
                normalized = normalized.replace("hit_at_", "hit_rate_at_", 1)
            if normalized in metrics:
                selected.add(normalized)
            else:
                unknown.append(token)
    if unknown:
        available_text = ", ".join(available)
        raise ValueError(
            f"unknown retrieval metric(s): {', '.join(unknown)}; available: {available_text}"
        )
    return [name for name in available if name in selected]


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
    if case.get("retrieval_error"):
        reasons.append("retrieval_error")
    return reasons


# /**
#  * Organiza uma execução em um contrato próprio para terminal, arquivo ou observabilidade.
#  * Existe para separar o cálculo das métricas do formato de apresentação e de uma futura
#  * integração com Langfuse, preservando o golden e os diagnósticos por caso.
#  * Histórico: 026-v18 — cria relatório com resumo, scores, falhas e casos; 027-v8 — adiciona modos de saída e seleção.
#  */
def build_report(
    result: EvaluationResult,
    dataset: Mapping[str, Any],
    ks: tuple[int, ...],
    *,
    metrics_filter: str = "all",
    output_mode: str = "full",
) -> dict[str, Any]:
    """Retorna o relatório filtrado sem enviar dados para nenhuma plataforma externa."""

    if output_mode not in {"full", "summary", "only_failures"}:
        raise ValueError("output_mode must be full, summary or only_failures")
    selected_names = set(_select_metric_names(result.metrics, metrics_filter))
    selected_metrics = {
        name: value for name, value in result.metrics.items() if name in selected_names
    }

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
                "retrieval_error": case.get("retrieval_error"),
                "latency_ms": case.get("retrieval_latency_ms", 0.0),
            },
            "scores": _score_records(
                {
                    name: value
                    for name, value in case["metrics"].items()
                    if name in selected_names
                }
            ),
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
    report = {
        "schema": REPORT_SCHEMA,
        "run": run,
        "summary": {
            "status": "observed",
            "case_count": result.case_count,
            "answerable_case_count": result.answerable_case_count,
            "no_answer_case_count": result.no_answer_case_count,
            "failure_count": len(failures),
            "metrics": selected_metrics,
        },
        "scores": _score_records(selected_metrics),
        "quality": {
            "status": "not_evaluated",
            "thresholds": {},
            "checks": [],
        },
    }
    if output_mode == "summary":
        return report
    report["failures"] = failures
    report["cases"] = (
        [case for case in report_cases if case["diagnostics"]["status"] == "failed"]
        if output_mode == "only_failures"
        else report_cases
    )
    return report
