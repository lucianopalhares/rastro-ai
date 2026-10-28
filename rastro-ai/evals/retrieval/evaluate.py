"""Executa métricas reproduzíveis sobre o retrieval real da aplicação."""

from __future__ import annotations

import argparse
import json
from math import ceil
from time import perf_counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, Sequence

from .metrics.invariants_metrics import (
    abstention,
    project_isolation,
    score_ordering,
)
from .metrics.ranking_metrics import mean_reciprocal_rank
from .metrics.ranking_metrics.ranx_adapter import evaluate_query_metrics

DATASET_PATH = Path(__file__).parents[1] / "dataset" / "golden.json"


class RetrievedChunkLike(Protocol):
    """Descreve somente os campos do resultado necessários para a evaluation."""

    chunk: Any
    score: float


class RetrieverLike(Protocol):
    """Permite avaliar um retriever real ou um fake sem acoplar o evaluator ao runtime."""

    # /** Ordem: etapa 2; executa a busca antes da normalização e das métricas. */
    def __call__(self, project_id: str, query: str, *, limit: int) -> Sequence[RetrievedChunkLike]:
        """Executa uma consulta e devolve chunks ordenados por relevância."""


# /**
#  * Representa um chunk esperado no golden dataset e seu grau de relevância.
#  * Existe para separar a decisão humana de relevância do resultado produzido pelo retriever.
#  * Histórico: 026-v1 — cria o contrato de julgamentos do retrieval.
#  */
@dataclass(frozen=True, slots=True)
class ExpectedChunk:
    """Identifica um chunk relevante e seu peso para nDCG."""

    chunk_id: str
    relevance: int


# /**
#  * Guarda as métricas e diagnósticos de uma execução completa do golden dataset.
#  * Existe para permitir comparação reproduzível entre embeddings, chunking e configurações.
#  * Histórico: 026-v1 — cria o resultado serializável da evaluation.
#  */
@dataclass(frozen=True, slots=True)
class EvaluationResult:
    """Resultado agregado e por caso do evaluator de retrieval."""

    case_count: int
    answerable_case_count: int
    no_answer_case_count: int
    metrics: dict[str, float]
    cases: tuple[dict[str, Any], ...]

    # /**
    #  * Expõe a saída JSON para CI e comparação entre execuções.
    #  * Ordem: etapa 6.2, depois da agregação das métricas por todas as consultas.
    #  * Histórico: 026-v1 — expõe saída JSON; 026-v4 — documenta a ordem.
    #  */
    def as_dict(self) -> dict[str, Any]:
        """Converte o resultado para um documento JSON estável."""

        return {
            "case_count": self.case_count,
            "answerable_case_count": self.answerable_case_count,
            "no_answer_case_count": self.no_answer_case_count,
            "metrics": self.metrics,
            "cases": list(self.cases),
        }


# /**
#  * Carrega e valida o golden dataset versionado do retrieval.
#  * Existe para falhar cedo quando uma pergunta não possui projeto ou julgamento válido.
#  * Ordem: etapa 1, antes de chamar o retriever e as métricas.
#  * Histórico: 026-v1 — adiciona o formato de queries e chunks relevantes; 026-v4 — documenta a ordem.
#  */
def load_dataset(path: Path = DATASET_PATH) -> dict[str, Any]:
    """Retorna o dataset e rejeita estruturas que produziriam métricas ambíguas."""

    dataset = json.loads(path.read_text(encoding="utf-8"))
    cases = dataset.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("retrieval dataset must contain non-empty cases")
    seen_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("retrieval case must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip() or case_id in seen_ids:
            raise ValueError("retrieval case ids must be unique and non-empty")
        seen_ids.add(case_id)
        if not isinstance(case.get("project_id"), str) or not case["project_id"].strip():
            raise ValueError(f"{case_id}: project_id is required")
        if not isinstance(case.get("query"), str) or not case["query"].strip():
            raise ValueError(f"{case_id}: query is required")
        expected = case.get("relevant_chunks", [])
        if not isinstance(expected, list):
            raise ValueError(f"{case_id}: relevant_chunks must be a list")
        for item in expected:
            if not isinstance(item, dict) or not isinstance(item.get("chunk_id"), str):
                raise ValueError(f"{case_id}: every relevant chunk needs chunk_id")
            if not isinstance(item.get("relevance"), int) or item["relevance"] <= 0:
                raise ValueError(f"{case_id}: relevance must be a positive integer")
    return dataset


# /**
#  * Normaliza a identidade document_id/index usada pelo golden dataset.
#  * Ordem: etapa 3, depois do retrieval e antes de executar as métricas.
#  * Histórico: 026-v1 — cria a identidade; 026-v4 — documenta a ordem.
#  */
def _chunk_id(result: RetrievedChunkLike) -> str:
    """Monta o identificador estável usado pelo golden dataset."""

    return f"{result.chunk.document_id}:{result.chunk.index}"


# /**
#  * Cria o acumulador das métricas que serão calculadas em todos os casos.
#  * Existe para deixar visível, em um único lugar, quais resultados pertencem ao ranking
#  * e quais são invariantes de segurança ou consistência.
#  * Histórico: 027-v5 — separa a preparação do acumulador do fluxo principal.
#  */
def _initialize_metric_totals(ks: tuple[int, ...]) -> dict[str, float]:
    """Retorna os acumuladores vazios para ranking e invariantes."""

    totals = {f"recall_at_{k}": 0.0 for k in ks}
    totals.update({f"precision_at_{k}": 0.0 for k in ks})
    totals.update({f"ndcg_at_{k}": 0.0 for k in ks})
    totals.update({f"hit_rate_at_{k}": 0.0 for k in ks})
    totals.update(
        {
            "mrr": 0.0,
            "project_isolation": 0.0,
            "score_ordering": 0.0,
            "abstention": 0.0,
            "retrieval_latency_ms": 0.0,
            "retrieval_error_rate": 0.0,
            "empty_result_rate": 0.0,
        }
    )
    return totals


# /**
#  * Executa as invariantes sobre os resultados brutos do retriever.
#  * Existe para manter separadas as perguntas “a busca é segura e consistente?” das métricas
#  * que avaliam “a busca encontrou e ordenou bem as evidências?”.
#  * Ordem: etapa 4, depois da normalização dos chunks e antes do ranking.
#  * Histórico: 027-v5 — agrupa as chamadas de invariantes em uma etapa nomeada.
#  */
def _evaluate_invariants(
    results: Sequence[RetrievedChunkLike],
    returned_ids: Sequence[str],
    scores: Sequence[float],
    expected: dict[str, int],
    project_id: str,
) -> dict[str, float]:
    """Retorna isolamento, ordenação e abstention quando o caso não tem resposta."""

    invariant_scores = {
        "project_isolation": project_isolation(
            (result.chunk.project_id for result in results), project_id
        ),
        "score_ordering": score_ordering(scores),
    }
    if not expected:
        invariant_scores["abstention"] = abstention(returned_ids, set(expected))
    return invariant_scores


# /**
#  * Executa as métricas de ranking usando o adapter do ranx.
#  * Existe para deixar explícito que Recall, Precision, nDCG e MRR medem a qualidade do
#  * ranking, e não substituem as invariantes de segurança executadas anteriormente.
#  * Ordem: etapa 5, depois das invariantes e antes da agregação do dataset.
#  * Histórico: 027-v5 — agrupa a montagem e leitura das métricas de ranking; 027-v7 — adiciona HitRate.
#  */
def _evaluate_ranking_metrics(
    expected: dict[str, int],
    returned_ids: Sequence[str],
    scores: Sequence[float],
    ks: tuple[int, ...],
) -> dict[str, float]:
    """Retorna HitRate, Recall, Precision e nDCG por k, além do MRR do caso."""

    metric_names = [
        metric
        for k in ks
        for metric in (
            f"hit_rate@{k}",
            f"recall@{k}",
            f"precision@{k}",
            f"ndcg@{k}",
        )
    ]
    metric_names.append("mrr")
    return evaluate_query_metrics(metric_names, expected, returned_ids, scores)


# /**
#  * Calcula o percentil aproximado de latência de uma execução.
#  * Existe para mostrar o comportamento típico e também o custo das consultas mais lentas,
#  * sem depender de uma biblioteca estatística adicional.
#  * Histórico: 027-v7 — adiciona P95 de latência do retrieval.
#  */
def _percentile(values: Sequence[float], percentile: float) -> float:
    """Retorna o percentil por posição mais próxima em uma sequência não vazia."""

    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, ceil(len(ordered) * percentile) - 1))
    return ordered[index]


# /**
#  * Calcula as médias finais a partir dos acumuladores dos casos.
#  * Existe para concentrar as regras de denominador: MRR usa somente perguntas com evidência,
#  * abstention usa somente perguntas sem evidência e as demais métricas usam todos os casos.
#  * Ordem: etapa 6, depois que todos os casos foram processados.
#  * Histórico: 027-v5 — separa a agregação do processamento de cada caso; 027-v7 — agrega operação.
#  */
def _aggregate_metrics(
    metric_totals: dict[str, float],
    mrr_values: Sequence[float],
    *,
    case_count: int,
    answerable_count: int,
    no_answer_count: int,
    latency_values: Sequence[float],
) -> dict[str, float]:
    """Retorna as métricas médias com o denominador adequado para cada grupo."""

    metrics: dict[str, float] = {}
    for key, value in metric_totals.items():
        denominator = (
            answerable_count
            if key == "mrr"
            else no_answer_count
            if key == "abstention"
            else case_count
        )
        if key == "mrr":
            metrics[key] = round(mean_reciprocal_rank(mrr_values), 6)
        else:
            metrics[key] = round(value / denominator, 6) if denominator else 0.0
    metrics["retrieval_latency_p95_ms"] = (
        round(_percentile(latency_values, 0.95), 6) if latency_values else 0.0
    )
    return metrics


# /**
#  * Executa o retriever injetado e calcula ranking semântico sem gerar respostas de LLM.
#  * Existe para medir o resultado de chunks produzido pelo PGVector, mantendo a aplicação
#  * de runtime fora do módulo de evaluation.
#  * Ordem: etapa 2 chama o retriever; etapa 3 normaliza resultados; etapa 4 executa métricas
#  * de segurança e score; etapa 5 executa ranking; etapa 6 agrega o resultado final.
#  * Histórico: 026-v1 — adiciona as métricas; 026-v4 — documenta a ordem; 026-v14 — explica cada chamada interna; 026-v15 — mantém o contrato de resposta no golden; 027-v1 — delega métricas clássicas ao ranx.
#  */
def run_evaluation(
    dataset: dict[str, Any],
    retriever: RetrieverLike,
    *,
    ks: tuple[int, ...] = (1, 3, 5),
) -> EvaluationResult:
    """Executa o golden dataset contra um retriever real ou controlado."""

    if not ks or any(k <= 0 for k in ks):
        raise ValueError("ks must contain positive values")
    cases: list[dict[str, Any]] = []
    metric_totals = _initialize_metric_totals(ks)
    answerable_count = 0
    no_answer_count = 0
    mrr_values: list[float] = []
    latency_values: list[float] = []
    max_k = max(ks)

    for case in dataset["cases"]:
        expected = {
            item["chunk_id"]: item["relevance"]
            for item in case.get("relevant_chunks", [])
        }
        # Busca os chunks mais parecidos com a pergunta e mede somente o tempo do retriever.
        started_at = perf_counter()
        retrieval_error: str | None = None
        try:
            results = list(retriever(case["project_id"], case["query"], limit=max_k))
        except Exception as error:
            retrieval_error = type(error).__name__
            results = []
        latency_ms = (perf_counter() - started_at) * 1000
        latency_values.append(latency_ms)
        metric_totals["retrieval_latency_ms"] += latency_ms
        if retrieval_error:
            metric_totals["retrieval_error_rate"] += 1.0
        elif not results:
            metric_totals["empty_result_rate"] += 1.0

        # Converte cada resultado para o mesmo identificador usado no golden dataset.
        returned_ids = [_chunk_id(result) for result in results]
        scores = [float(result.score) for result in results]

        # Executa as regras de segurança e consistência antes de avaliar a qualidade do ranking.
        invariant_scores = _evaluate_invariants(
            results,
            returned_ids,
            scores,
            expected,
            case["project_id"],
        )
        if retrieval_error:
            invariant_scores["project_isolation"] = 0.0
            invariant_scores["score_ordering"] = 0.0
            invariant_scores.pop("abstention", None)
        answerable = bool(expected)
        if answerable:
            answerable_count += 1
        else:
            no_answer_count += 1
        for name, value in invariant_scores.items():
            metric_totals[name] += value

        # Executa somente as métricas que medem cobertura, precisão e posição das evidências.
        ranking_scores = _evaluate_ranking_metrics(
            expected, returned_ids, scores, ks
        )
        if answerable:
            mrr_values.append(ranking_scores["mrr"])
        case_metrics: dict[str, float] = {}
        for k in ks:
            case_metrics[f"hit_rate_at_{k}"] = ranking_scores[f"hit_rate@{k}"]
            case_metrics[f"recall_at_{k}"] = ranking_scores[f"recall@{k}"]
            case_metrics[f"precision_at_{k}"] = ranking_scores[f"precision@{k}"]
            case_metrics[f"ndcg_at_{k}"] = ranking_scores[f"ndcg@{k}"]
            metric_totals[f"recall_at_{k}"] += case_metrics[f"recall_at_{k}"]
            metric_totals[f"precision_at_{k}"] += case_metrics[f"precision_at_{k}"]
            metric_totals[f"ndcg_at_{k}"] += case_metrics[f"ndcg_at_{k}"]
            metric_totals[f"hit_rate_at_{k}"] += case_metrics[f"hit_rate_at_{k}"]
        cases.append(
            {
                "id": case["id"],
                "returned_chunks": returned_ids,
                "scores": scores,
                "expected_chunks": list(expected),
                "metrics": case_metrics,
                "project_isolation": invariant_scores["project_isolation"],
                "score_ordering": invariant_scores["score_ordering"],
                "retrieval_error": retrieval_error,
                "retrieval_latency_ms": round(latency_ms, 6),
            }
        )

    count = len(cases)
    # Consolida todos os casos somente depois que as etapas de invariantes e ranking terminaram.
    metrics = _aggregate_metrics(
        metric_totals,
        mrr_values,
        case_count=count,
        answerable_count=answerable_count,
        no_answer_count=no_answer_count,
        latency_values=latency_values,
    )
    return EvaluationResult(count, answerable_count, no_answer_count, metrics, tuple(cases))


# /**
#  * Executa a avaliação contra a fachada pública configurada para PGVector.
#  * Existe para manter o acesso ao banco explícito e impedir chamadas externas durante testes.
#  * Ordem: etapa 0 inicia o CLI, carrega dataset na etapa 1 e chama `run_evaluation` na etapa 2.
#  * Histórico: 026-v1 — adiciona o comando de integração manual; 026-v4 — documenta a ordem; 027-v8 — adiciona filtros de saída.
#  */
def main() -> None:
    """Executa o golden dataset real e imprime métricas JSON."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DATASET_PATH)
    parser.add_argument("--ks", default="1,3,5", help="valores de k separados por vírgula")
    parser.add_argument(
        "--metrics",
        default="all",
        help="all, ranking, invariants, operational ou nomes separados por vírgula",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "--summary",
        action="store_true",
        help="imprime somente métricas agregadas e metadados da execução",
    )
    output_group.add_argument(
        "--only-failures",
        action="store_true",
        help="imprime o resumo e somente os casos com falha",
    )
    arguments = parser.parse_args()
    ks = tuple(sorted({int(value) for value in arguments.ks.split(",")}))
    dataset = load_dataset(arguments.dataset)
    from rastro_ai.retrieval import search_relevant_chunks

    result = run_evaluation(dataset, search_relevant_chunks, ks=ks)
    from .report import build_report

    output_mode = "summary" if arguments.summary else "only_failures" if arguments.only_failures else "full"
    print(
        json.dumps(
            build_report(
                result,
                dataset,
                ks,
                metrics_filter=arguments.metrics,
                output_mode=output_mode,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
