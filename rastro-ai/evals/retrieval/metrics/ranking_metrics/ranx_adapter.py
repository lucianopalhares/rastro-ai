"""Adapta os julgamentos do projeto para as métricas de ranking do ranx."""

from collections.abc import Collection, Mapping, Sequence

from ranx import Qrels, Run, evaluate


# /**
#  * Converte a resposta esperada e os resultados encontrados para o formato que o `ranx` entende.
#  * Existe para manter o cálculo padronizado em uma biblioteca externa sem espalhar detalhes dela
#  * pelo evaluator. Não escolhe chunks nem altera o resultado do retriever.
#  * Histórico: 027-v1 — cria a normalização do adapter; 027-v4 — simplifica a explicação.
#  */
def _relevance_mapping(relevant_chunk_ids: Mapping[str, int] | Collection[str]) -> dict[str, int]:
    """Normaliza julgamentos de relevância para o formato aceito pelo ranx."""

    if isinstance(relevant_chunk_ids, Mapping):
        return dict(relevant_chunk_ids)
    return {chunk_id: 1 for chunk_id in relevant_chunk_ids}


# /**
#  * Calcula de uma vez as métricas pedidas para uma pergunta e seus resultados.
#  * Existe para compartilhar o trabalho de inicialização do `ranx` e manter a avaliação eficiente.
#  * Histórico: 027-v1 — adiciona avaliação agrupada por consulta; 027-v4 — simplifica a explicação.
#  */
def evaluate_query_metrics(
    metrics: Sequence[str] | str,
    relevant_chunk_ids: Mapping[str, int] | Collection[str],
    retrieved_chunk_ids: Sequence[str],
    scores: Sequence[float] | None = None,
) -> dict[str, float]:
    """Retorna as métricas ranx solicitadas para uma consulta."""

    metric_names = [metrics] if isinstance(metrics, str) else list(metrics)
    if not metric_names:
        return {}
    # /**
    #  * Normaliza o gabarito para um dicionário que associa cada chunk esperado ao seu grau
    #  * de relevância, permitindo que o ranx compare a resposta correta com o Run.
    #  * Exemplo: ["chunk-a", "chunk-b"] vira {"chunk-a": 1, "chunk-b": 1}; já
    #  * {"chunk-a": 3} preserva o grau explícito informado pelo dataset.
    #  * Histórico: ajuste documental solicitado pelo usuário.
    #  */
    relevance = _relevance_mapping(relevant_chunk_ids)
    # /**
    #  * Trata uma busca vazia antes de criar o `Run` do ranx.
    #  * Uma lista vazia representa zero acertos quando havia relevância esperada; a causa
    #  * operacional continua registrada separadamente pelo evaluator.
    #  * Histórico: 027-v7 — protege o adapter contra resultados vazios.
    #  */
    if not relevance or not retrieved_chunk_ids:
        return {metric: 0.0 for metric in metric_names}
    query_id = "query"
    # /**
    #  * Representa o gabarito de relevância esperado para cada consulta, associando cada
    #  * chunk correto ao seu grau de relevância para o ranx comparar com o Run.
    #  * Exemplo: relevance={"chunk-a": 3, "chunk-b": 1} produz
    #  * Qrels({"query": {"chunk-a": 3, "chunk-b": 1}}).
    #  * Histórico: ajuste documental solicitado pelo usuário.
    #  */
    qrels = Qrels({query_id: relevance})
    ranking_scores = scores or [
        float(len(retrieved_chunk_ids) - position)
        for position in range(len(retrieved_chunk_ids))
    ]
    # /**
    #  * Representa os resultados reais encontrados para cada consulta, associando cada
    #  * chunk retornado ao seu score para o ranx comparar com o gabarito do Qrels.
    #  * Exemplo: query_id="query" e chunks ["chunk-a", "chunk-b"] com scores [0.9, 0.6]
    #  * produzem Run({"query": {"chunk-a": 0.9, "chunk-b": 0.6}}).
    #  * Histórico: ajuste documental solicitado pelo usuário.
    #  */
    run = Run(
        {
            query_id: {
                chunk_id: float(score)
                for chunk_id, score in zip(retrieved_chunk_ids, ranking_scores)
            }
        }
    )
    # /**
    #  * Compara o gabarito do Qrels com os resultados do Run e calcula as métricas
    #  * solicitadas, como Recall, Precision, MRR e nDCG.
    #  * Exemplo: Qrels identifica os chunks corretos e Run informa os chunks encontrados;
    #  * o resultado pode ser {"recall@3": 1.0, "precision@3": 0.67}.
    #  * Histórico: ajuste documental solicitado pelo usuário.
    #  */
    evaluated = evaluate(qrels, run, metric_names)
    if len(metric_names) == 1:
        evaluated = {metric_names[0]: evaluated}
    return {metric: float(value) for metric, value in evaluated.items()}


# /**
#  * Calcula uma métrica padronizada para uma pergunta sem expor a estrutura interna do `ranx`.
#  * Existe para que os testes e o evaluator continuem usando funções pequenas e fáceis de ler.
#  * Histórico: 027-v1 — introduz o adapter ranx para Recall, Precision, MRR e nDCG; 027-v4 — simplifica a explicação.
#  */
def evaluate_query_metric(
    metric: str,
    relevant_chunk_ids: Mapping[str, int] | Collection[str],
    retrieved_chunk_ids: Sequence[str],
    *,
    k: int | None = None,
) -> float:
    """Calcula uma métrica ranx para uma consulta."""

    if k is not None and k <= 0:
        raise ValueError("k must be positive")
    metric_name = f"{metric}@{k}" if k is not None else metric
    return evaluate_query_metrics(metric_name, relevant_chunk_ids, retrieved_chunk_ids)[metric_name]
