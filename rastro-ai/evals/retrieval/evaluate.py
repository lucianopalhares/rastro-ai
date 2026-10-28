"""Executa métricas reproduzíveis sobre o retrieval real da aplicação."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, Sequence

from .metrics import (
    abstention,
    mean_reciprocal_rank,
    ndcg_at_k,
    precision_at_k,
    project_isolation,
    recall_at_k,
    reciprocal_rank,
    score_ordering,
)

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
#  * Executa o retriever injetado e calcula ranking semântico sem gerar respostas de LLM.
#  * Existe para medir o resultado de chunks produzido pelo PGVector, mantendo a aplicação
#  * de runtime fora do módulo de evaluation.
#  * Ordem: etapa 2 chama o retriever; etapa 3 normaliza resultados; etapa 4 executa métricas
#  * de segurança e score; etapa 5 executa ranking; etapa 6 agrega o resultado final.
#  * Histórico: 026-v1 — adiciona as métricas; 026-v4 — documenta a ordem; 026-v14 — explica cada chamada interna; 026-v15 — mantém o contrato de resposta no golden.
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
    metric_totals = {f"recall_at_{k}": 0.0 for k in ks}
    metric_totals.update({f"precision_at_{k}": 0.0 for k in ks})
    metric_totals.update({f"ndcg_at_{k}": 0.0 for k in ks})
    metric_totals.update({"mrr": 0.0, "project_isolation": 0.0, "score_ordering": 0.0, "abstention": 0.0})
    answerable_count = 0
    no_answer_count = 0
    mrr_values: list[float] = []
    max_k = max(ks)

    for case in dataset["cases"]:
        expected = {
            item["chunk_id"]: item["relevance"]
            for item in case.get("relevant_chunks", [])
        }
        # Busca os chunks mais parecidos com a pergunta usando o retriever configurado.
        results = list(retriever(case["project_id"], case["query"], limit=max_k))

        # Converte cada resultado para o mesmo identificador usado no golden dataset.
        returned_ids = [_chunk_id(result) for result in results]
        scores = [float(result.score) for result in results]
        relevant_ids = set(expected)

        # Confirma que nenhum chunk veio de outro projeto.
        isolated = project_isolation(
            (result.chunk.project_id for result in results), case["project_id"]
        )

        # Confirma que os scores estão ordenados do melhor para o pior resultado.
        score_ordered = score_ordering(scores)
        answerable = bool(expected)
        if answerable:
            answerable_count += 1

            # Mede a posição do primeiro chunk relevante encontrado.
            mrr_values.append(reciprocal_rank(returned_ids, relevant_ids))
        else:
            no_answer_count += 1
        metric_totals["project_isolation"] += isolated
        metric_totals["score_ordering"] += score_ordered
        if not answerable:

            # Verifica se o retriever ficou vazio quando o golden não tem evidência.
            metric_totals["abstention"] += abstention(returned_ids, relevant_ids)
        case_metrics: dict[str, float] = {}
        for k in ks:

            # Mede quantos chunks relevantes apareceram entre os primeiros k resultados.
            case_metrics[f"recall_at_{k}"] = recall_at_k(relevant_ids, returned_ids, k)

            # Mede quanto dos primeiros k resultados realmente é relevante.
            case_metrics[f"precision_at_{k}"] = precision_at_k(relevant_ids, returned_ids, k)

            # Mede se os chunks mais relevantes ficaram nas melhores posições.
            case_metrics[f"ndcg_at_{k}"] = ndcg_at_k(returned_ids, expected, k)
            metric_totals[f"recall_at_{k}"] += case_metrics[f"recall_at_{k}"]
            metric_totals[f"precision_at_{k}"] += case_metrics[f"precision_at_{k}"]
            metric_totals[f"ndcg_at_{k}"] += case_metrics[f"ndcg_at_{k}"]
        cases.append(
            {
                "id": case["id"],
                "returned_chunks": returned_ids,
                "scores": scores,
                "expected_chunks": list(expected),
                "metrics": case_metrics,
                "project_isolation": isolated,
                "score_ordering": score_ordered,
            }
        )

    count = len(cases)
    metrics = {}
    for key, value in metric_totals.items():
        denominator = answerable_count if key == "mrr" else no_answer_count if key == "abstention" else count
        if key == "mrr":

            # Calcula a média do MRR de todas as perguntas com evidência esperada.
            metrics[key] = round(mean_reciprocal_rank(mrr_values), 6)
        else:
            metrics[key] = round(value / denominator, 6) if denominator else 0.0
    # Agrupa as métricas e os detalhes de cada caso em um resultado serializável.
    return EvaluationResult(count, answerable_count, no_answer_count, metrics, tuple(cases))


# /**
#  * Executa a avaliação contra a fachada pública configurada para PGVector.
#  * Existe para manter o acesso ao banco explícito e impedir chamadas externas durante testes.
#  * Ordem: etapa 0 inicia o CLI, carrega dataset na etapa 1 e chama `run_evaluation` na etapa 2.
#  * Histórico: 026-v1 — adiciona o comando de integração manual; 026-v4 — documenta a ordem.
#  */
def main() -> None:
    """Executa o golden dataset real e imprime métricas JSON."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DATASET_PATH)
    parser.add_argument("--ks", default="1,3,5", help="valores de k separados por vírgula")
    arguments = parser.parse_args()
    ks = tuple(sorted({int(value) for value in arguments.ks.split(",")}))
    dataset = load_dataset(arguments.dataset)
    from rastro_ai.retrieval import search_relevant_chunks

    result = run_evaluation(dataset, search_relevant_chunks, ks=ks)
    from .report import build_report

    print(json.dumps(build_report(result, dataset, ks), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
