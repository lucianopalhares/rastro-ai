from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from evals.evaluate import load_dataset, run_evaluation


# /**
#  * Verifica o dataset e o baseline determinístico da aplicação.
#  * Existe para impedir regressões nos contratos de evaluation antes de introduzir julgamento por LLM.
#  * Histórico: v1 — adiciona quatro verificações do dataset, baseline e isolamento.
#  */
class EvaluationTests(unittest.TestCase):
    # /** Histórico: v1 — garante tamanho e categorias obrigatórias do dataset. */
    def test_dataset_has_twenty_cases_and_required_categories(self) -> None:
        dataset = load_dataset()
        categories = {case["category"] for case in dataset["cases"]}
        self.assertEqual(len(dataset["cases"]), 20)
        self.assertTrue({"grounded_answer", "multi_evidence", "no_evidence", "conflicting_documents", "citation_verification", "prompt_injection"}.issubset(categories))

    # /** Histórico: v1 — garante identificadores únicos e campos de cada golden. */
    def test_dataset_cases_have_required_fields_and_unique_ids(self) -> None:
        cases = load_dataset()["cases"]
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        for case in cases:
            self.assertTrue(case["question"])
            self.assertTrue(case["documents"])
            self.assertIn("expected_sources", case)

    # /** Histórico: v1 — verifica que o evaluator reproduz todas as métricas do baseline. */
    def test_evaluation_reproduces_baseline(self) -> None:
        result = run_evaluation(load_dataset())
        self.assertEqual(result.case_count, 20)
        self.assertEqual(result.passed_cases, 20)
        self.assertEqual(result.metrics, {"source_recall": 1.0, "citation_precision": 1.0, "safe_abstention": 1.0, "project_isolation": 1.0})

    # /** Histórico: v1 — garante que o cenário adversarial não atravessa o projeto consultado. */
    def test_evaluation_keeps_project_isolation_case(self) -> None:
        isolation = next(case for case in load_dataset()["cases"] if case["category"] == "project_isolation")
        self.assertEqual(isolation["project_id"], "project-a")
        self.assertIn("project-b-secret", {document["id"] for document in isolation["documents"]})


if __name__ == "__main__":
    unittest.main()
