import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from evals.retrieval.evaluate import load_dataset, run_evaluation
from evals.retrieval.prepare import build_evaluation_chunks, prepare_index
from evals.retrieval.report import build_report
from evals.retrieval.metrics import (
    abstention,
    mean_reciprocal_rank,
    ndcg_at_k,
    precision_at_k,
    project_isolation,
    recall_at_k,
    reciprocal_rank,
    score_ordering,
)


class FakeChunk:
    def __init__(self, document_id: str, index: int, project_id: str) -> None:
        self.document_id = document_id
        self.index = index
        self.project_id = project_id


class FakeResult:
    def __init__(self, document_id: str, index: int, project_id: str, score: float) -> None:
        self.chunk = FakeChunk(document_id, index, project_id)
        self.score = score


class RetrievalEvaluationTests(unittest.TestCase):
    # /**
    #  * Confirma que o relatório possui resumo, scores e casos em formato independente de vendor.
    #  * Histórico: 026-v18 — cobre o contrato preparado para futura integração com Langfuse.
    #  */
    def test_report_is_structured_for_future_observability(self) -> None:
        dataset = {
            "schema": "rastro-ai.golden.v1",
            "version": "v1",
            "cases": [
                {
                    "id": "q-1",
                    "project_id": "project-1",
                    "query": "qual banco?",
                    "expected_answer": {"text": "PostgreSQL", "abstain": False},
                    "relevant_chunks": [{"chunk_id": "doc:0", "relevance": 3}],
                }
            ],
        }

        def retriever(_project_id: str, _query: str, *, limit: int):
            return [FakeResult("noise", 0, "project-1", 0.9), FakeResult("doc", 0, "project-1", 0.8)][:limit]

        result = run_evaluation(dataset, retriever, ks=(1, 3))
        report = build_report(result, dataset, (1, 3))

        self.assertEqual(report["schema"], "rastro-ai.retrieval-report.v1")
        self.assertEqual(report["summary"]["failure_count"], 1)
        self.assertEqual(report["failures"][0]["reasons"], ["relevant_chunk_below_top"])
        self.assertEqual(report["cases"][0]["scores"][0]["data_type"], "NUMERIC")
        self.assertEqual(report["cases"][0]["expected"]["answer"]["text"], "PostgreSQL")

    # /**
    #  * Confirma que a saída pode ser reduzida sem perder o contrato das métricas selecionadas.
    #  * Histórico: 027-v8 — cobre summary, only_failures e seleção do grupo ranking.
    #  */
    def test_report_supports_summary_failures_and_metric_selection(self) -> None:
        dataset = {
            "cases": [
                {
                    "id": "q-1",
                    "project_id": "project-1",
                    "query": "qual banco?",
                    "relevant_chunks": [{"chunk_id": "doc:0", "relevance": 1}],
                }
            ]
        }

        def retriever(_project_id: str, _query: str, *, limit: int):
            return [FakeResult("noise", 0, "project-1", 0.9)][:limit]

        result = run_evaluation(dataset, retriever, ks=(1,))
        summary = build_report(result, dataset, (1,), metrics_filter="ranking", output_mode="summary")
        only_failures = build_report(result, dataset, (1,), output_mode="only_failures")

        self.assertNotIn("cases", summary)
        self.assertNotIn("project_isolation", summary["summary"]["metrics"])
        self.assertIn("recall_at_1", summary["summary"]["metrics"])
        self.assertEqual(len(only_failures["cases"]), 1)

    # /**
    #  * Confirma que o corpus e a resposta esperada permanecem compatíveis no mesmo golden.
    #  * Histórico: 026-v15 — cobre a preparação do índice isolado de evaluation.
    #  */
    def test_preparation_uses_golden_documents_and_expected_answer(self) -> None:
        dataset = {
            "cases": [
                {
                    "id": "q-1",
                    "project_id": "project-1",
                    "query": "qual banco?",
                    "documents": [{"id": "doc", "text": "O banco escolhido foi PostgreSQL."}],
                    "relevant_chunks": [{"chunk_id": "doc:0", "relevance": 3}],
                    "expected_answer": {
                        "text": "O banco escolhido foi PostgreSQL.",
                        "must_contain": ["PostgreSQL"],
                        "source_document_ids": ["doc"],
                        "abstain": False,
                    },
                }
            ]
        }
        persisted: list[tuple] = []

        chunks = build_evaluation_chunks(dataset)
        count = prepare_index(dataset, persisted.append)

        self.assertEqual(count, 1)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(persisted, [chunks])
        self.assertEqual(chunks[0].project_id, "project-1")
        self.assertEqual(chunks[0].document_id, "doc")

    # /**
    #  * Confirma que cada métrica funciona sem conhecer o evaluator ou o runtime.
    #  * Histórico: 026-v2 — cobre o desacoplamento das métricas puras.
    #  */
    def test_metrics_are_independently_composable(self) -> None:
        relevant = {"a", "b"}
        ranked = ["noise", "a", "b"]

        self.assertEqual(recall_at_k(relevant, ranked, 3), 1.0)
        self.assertAlmostEqual(precision_at_k(relevant, ranked, 1), 0.0)
        self.assertAlmostEqual(reciprocal_rank(ranked, relevant), 0.5)
        self.assertAlmostEqual(mean_reciprocal_rank((1.0, 0.5)), 0.75)
        self.assertGreater(ndcg_at_k(ranked, {"a": 3, "b": 2}, 3), 0.0)
        self.assertEqual(project_isolation(("project-1",), "project-1"), 1.0)
        self.assertEqual(project_isolation(("project-2",), "project-1"), 0.0)
        self.assertEqual(score_ordering((0.9, 0.4, 0.4)), 1.0)
        self.assertEqual(score_ordering((0.4, 0.9)), 0.0)
        self.assertEqual(abstention((), set()), 1.0)
        self.assertEqual(abstention(("noise",), set()), 0.0)

    # /**
    #  * Confirma que o evaluator mede posição e cobertura sem compreender semanticamente o texto.
    #  * Histórico: 026-v1 — cobre Recall@k, Precision@k, MRR e nDCG com resultados controlados.
    #  */
    def test_evaluation_calculates_ranking_metrics(self) -> None:
        dataset = {
            "cases": [
                {
                    "id": "q-1",
                    "project_id": "project-1",
                    "query": "qual banco?",
                    "relevant_chunks": [
                        {"chunk_id": "doc:0", "relevance": 3},
                        {"chunk_id": "doc-2:0", "relevance": 2},
                    ],
                }
            ]
        }

        def retriever(_project_id: str, _query: str, *, limit: int):
            return [
                FakeResult("noise", 0, "project-1", 0.9),
                FakeResult("doc", 0, "project-1", 0.8),
                FakeResult("doc-2", 0, "project-1", 0.7),
            ][:limit]

        result = run_evaluation(dataset, retriever, ks=(1, 3))

        self.assertEqual(result.metrics["recall_at_3"], 1.0)
        self.assertEqual(result.metrics["hit_rate_at_1"], 0.0)
        self.assertEqual(result.metrics["hit_rate_at_3"], 1.0)
        self.assertAlmostEqual(result.metrics["precision_at_1"], 0.0)
        self.assertAlmostEqual(result.metrics["mrr"], 0.5)
        self.assertGreater(result.metrics["ndcg_at_3"], 0.0)
        self.assertGreaterEqual(result.metrics["retrieval_latency_ms"], 0.0)
        self.assertGreaterEqual(result.metrics["retrieval_latency_p95_ms"], 0.0)
        self.assertEqual(result.metrics["retrieval_error_rate"], 0.0)
        self.assertEqual(result.metrics["empty_result_rate"], 0.0)

    # /**
    #  * Confirma que a evaluation diferencia busca vazia de falha técnica do retriever.
    #  * Histórico: 027-v7 — cobre HitRate e indicadores operacionais básicos.
    #  */
    def test_evaluation_reports_empty_results_and_retrieval_errors(self) -> None:
        dataset = {
            "cases": [
                {
                    "id": "empty",
                    "project_id": "project-1",
                    "query": "sem resultado",
                    "relevant_chunks": [],
                },
                {
                    "id": "error",
                    "project_id": "project-1",
                    "query": "falha",
                    "relevant_chunks": [{"chunk_id": "doc:0", "relevance": 1}],
                },
            ]
        }

        def retriever(_project_id: str, query: str, *, limit: int):
            if query == "falha":
                raise RuntimeError("retriever unavailable")
            return []

        result = run_evaluation(dataset, retriever, ks=(1,))

        self.assertEqual(result.metrics["hit_rate_at_1"], 0.0)
        self.assertEqual(result.metrics["empty_result_rate"], 0.5)
        self.assertEqual(result.metrics["retrieval_error_rate"], 0.5)
        self.assertIsNone(result.cases[0]["retrieval_error"])
        self.assertEqual(result.cases[1]["retrieval_error"], "RuntimeError")

    # /**
    #  * Confirma que o evaluator detecta vazamento de projeto, score fora de ordem e falta de abstinência.
    #  * Histórico: 026-v1 — cobre invariantes de segurança e ausência de evidência.
    #  */
    def test_evaluation_reports_isolation_score_ordering_and_abstention(self) -> None:
        dataset = {
            "cases": [
                {
                    "id": "isolation",
                    "project_id": "project-a",
                    "query": "decisão",
                    "relevant_chunks": [{"chunk_id": "a:0", "relevance": 3}],
                },
                {
                    "id": "none",
                    "project_id": "project-a",
                    "query": "orçamento",
                    "relevant_chunks": [],
                },
            ]
        }

        def retriever(_project_id: str, query: str, *, limit: int):
            if query == "decisão":
                return [
                    FakeResult("b", 0, "project-b", 0.4),
                    FakeResult("a", 0, "project-a", 0.8),
                ][:limit]
            return [FakeResult("noise", 0, "project-a", 0.1)][:limit]

        result = run_evaluation(dataset, retriever)

        self.assertEqual(result.metrics["project_isolation"], 0.5)
        self.assertEqual(result.metrics["score_ordering"], 0.5)
        self.assertEqual(result.metrics["abstention"], 0.0)

    # /** Histórico: 026-v1 — garante que o golden dataset versionado possui casos essenciais. */
    def test_versioned_dataset_has_required_cases(self) -> None:
        dataset = load_dataset()
        self.assertEqual(len(dataset["cases"]), 20)
        self.assertIn("none-001", {case["id"] for case in dataset["cases"]})
        self.assertIn("isolation-001", {case["id"] for case in dataset["cases"]})


if __name__ == "__main__":
    unittest.main()
