"""Métricas puras e independentes para avaliação de retrieval."""

from .abstention import abstention
from .isolation import project_isolation
from .mrr import mean_reciprocal_rank, reciprocal_rank
from .ndcg import ndcg_at_k
from .precision import precision_at_k
from .recall import recall_at_k
from .score_ordering import score_ordering

__all__ = [
    "abstention",
    "mean_reciprocal_rank",
    "ndcg_at_k",
    "precision_at_k",
    "project_isolation",
    "recall_at_k",
    "reciprocal_rank",
    "score_ordering",
]
