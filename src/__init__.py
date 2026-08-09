"""Source code modules for OGBN-Arxiv Graph Intelligence project."""

from .models import GCN, GraphSAGE
from .train import train_one_epoch, evaluate_accuracy, train_model
from .evaluate import compute_metrics
from .data_preprocessing import normalize_features, convert_to_undirected, get_train_valid_test_idx
from .graph_analysis import compute_graph_stats, compute_connected_components, compute_degree_distribution
from .explainability import apply_pca, apply_tsne, analyze_neighborhood

__all__ = [
    "GCN",
    "GraphSAGE",
    "train_one_epoch",
    "evaluate_accuracy",
    "train_model",
    "compute_metrics",
    "normalize_features",
    "convert_to_undirected",
    "get_train_valid_test_idx",
    "compute_graph_stats",
    "compute_connected_components",
    "compute_degree_distribution",
    "apply_pca",
    "apply_tsne",
    "analyze_neighborhood",
]
