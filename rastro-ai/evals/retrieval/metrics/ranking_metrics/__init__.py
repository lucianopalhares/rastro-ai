"""Métricas padronizadas de ranking para avaliação de retrieval."""

from .mrr import mean_reciprocal_rank, reciprocal_rank
from .ndcg import ndcg_at_k
from .precision import precision_at_k
from .ranx_adapter import evaluate_query_metric, evaluate_query_metrics
from .recall import recall_at_k

__all__ = [
    "evaluate_query_metric",
    "evaluate_query_metrics",
    "mean_reciprocal_rank",
    "ndcg_at_k",
    "precision_at_k",
    "recall_at_k",
    "reciprocal_rank",
]
