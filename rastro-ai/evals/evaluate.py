"""Executa o baseline determinístico do fluxo atual de respostas."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rastro_ai.document_indexing.application.use_cases.answer_question import AnswerQuestionUseCase
from rastro_ai.document_indexing.application.use_cases.retrieve_chunks import SearchRelevantChunksUseCase
from rastro_ai.document_indexing.domain.entities import DocumentChunk
from rastro_ai.document_indexing.infrastructure.retrieval.in_memory_vector_store import InMemoryChunkVectorStore

DATASET_PATH = Path(__file__).with_name("dataset") / "golden.json"
BASELINE_PATH = Path(__file__).with_name("baseline.json")


# /**
#  * Resultado agregado da avaliação determinística do dataset.
#  * Existe para versionar métricas reproduzíveis antes de introduzir julgamento por LLM.
#  * Histórico: v1 — cria cobertura de fontes, citações, abstinência e isolamento.
#  */
@dataclass(frozen=True, slots=True)
class EvaluationResult:
    """Contém contagens e métricas calculadas sem dependências externas."""

    case_count: int
    passed_cases: int
    metrics: dict[str, float]

    def as_dict(self) -> dict[str, Any]:
        """Serializa o resultado para comparação com o baseline versionado."""

        return {
            "case_count": self.case_count,
            "passed_cases": self.passed_cases,
            "metrics": self.metrics,
        }


# /**
#  * Lê o dataset curado que representa os comportamentos essenciais da aplicação.
#  * Existe para manter os goldens independentes de uma execução específica.
#  * Histórico: v1 — adiciona o dataset versionado de 20 casos.
#  */
def load_dataset(path: Path = DATASET_PATH) -> dict[str, Any]:
    """Retorna o documento JSON do dataset de evaluation."""

    return json.loads(path.read_text(encoding="utf-8"))


# /**
#  * Executa cada caso contra o store, retrieval e resposta reais da aplicação.
#  * Existe para detectar regressões determinísticas sem fingir métricas semânticas.
#  * Histórico: v1 — calcula recall de fontes, precisão de citações, abstinência e isolamento.
#  */
def run_evaluation(dataset: dict[str, Any]) -> EvaluationResult:
    """Executa o dataset completo e retorna métricas normalizadas entre zero e um."""

    counters = {"source_recall": 0, "citation_precision": 0, "safe_abstention": 0, "project_isolation": 0}
    passed_cases = 0
    cases = dataset["cases"]

    for case in cases:
        store = InMemoryChunkVectorStore()
        chunks = []
        for document in case["documents"]:
            project_id = document.get("project_id", case["project_id"])
            chunks.append(DocumentChunk(document["id"], 0, document["text"], 0, len(document["text"]), project_id))
        store.upsert(chunks)
        retriever = SearchRelevantChunksUseCase(store)
        answer = AnswerQuestionUseCase(retriever).execute(case["project_id"], case["query"])
        retrieved_ids = {result.chunk.document_id for result in retriever.execute(case["project_id"], case["query"])}
        expected_answer = case["expected_answer"]
        expected_sources = set(expected_answer.get("source_document_ids", []))
        source_ok = expected_sources.issubset(retrieved_ids) and (bool(expected_sources) or not retrieved_ids)
        citation_ok = all(
            citation.document_id in expected_sources
            and citation.excerpt == next(document["text"] for document in case["documents"] if document["id"] == citation.document_id)
            for citation in answer.citations
        ) and (bool(answer.citations) == bool(expected_sources))
        abstention_ok = (not answer.citations) == expected_answer.get("abstain", False)
        isolation_ok = all(citation.document_id in {document["id"] for document in case["documents"] if document.get("project_id", case["project_id"]) == case["project_id"]} for citation in answer.citations)
        for key, passed in (("source_recall", source_ok), ("citation_precision", citation_ok), ("safe_abstention", abstention_ok), ("project_isolation", isolation_ok)):
            counters[key] += int(passed)
        passed_cases += int(all((source_ok, citation_ok, abstention_ok, isolation_ok)))

    count = len(cases)
    return EvaluationResult(count, passed_cases, {key: round(value / count, 6) for key, value in counters.items()})


# /**
#  * Executa o baseline e imprime uma saída curta para uso local e CI futuro.
#  * Existe para tornar a verificação manual copiável sem alterar o runtime da aplicação.
#  * Histórico: v1 — adiciona comando de execução do baseline versionado.
#  */
def main() -> None:
    """Executa o dataset e falha se o resultado divergir do baseline salvo."""

    dataset = load_dataset()
    result = run_evaluation(dataset)
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    expected = {"case_count": baseline["case_count"], "passed_cases": baseline["passed_cases"], "metrics": baseline["metrics"]}
    if result.as_dict() != expected:
        raise SystemExit(f"baseline divergente: esperado={expected} obtido={result.as_dict()}")
    print(f"evaluation baseline: {result.passed_cases}/{result.case_count} casos aprovados; métricas={result.metrics}")


if __name__ == "__main__":
    main()
