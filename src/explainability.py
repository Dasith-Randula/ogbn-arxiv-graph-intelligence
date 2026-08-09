"""Explainability utilities for neighborhood analysis and embedding reduction."""

from collections import Counter
from typing import Dict

import numpy as np
import torch
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


def apply_pca(embeddings: np.ndarray, n_components: int = 2) -> np.ndarray:
    """Reduce embeddings with PCA."""
    pca = PCA(n_components=n_components)
    return pca.fit_transform(embeddings)


def apply_tsne(
    embeddings: np.ndarray,
    n_components: int = 2,
    perplexity: float = 30.0,
    n_iter: int = 1000,
) -> np.ndarray:
    """Reduce embeddings with t-SNE when requested."""
    tsne = TSNE(n_components=n_components, perplexity=perplexity, n_iter=n_iter)
    return tsne.fit_transform(embeddings)


def analyze_neighborhood(
    node_id: int,
    edge_index: torch.Tensor,
    embeddings: np.ndarray,
    actual_label: int,
    predicted_label: int,
    labels: torch.Tensor,
    k: int = 5,
) -> Dict[str, object]:
    """Analyze the neighborhood of a node and summarize label agreement."""
    src = edge_index[0].cpu().numpy()
    dst = edge_index[1].cpu().numpy()

    outgoing = dst[src == node_id]
    incoming = src[dst == node_id]

    neighbor_ids = list(set(outgoing.tolist() + incoming.tolist()))
    neighbor_labels = [int(labels[neighbor].item()) for neighbor in neighbor_ids]
    neighbor_label_distribution = dict(Counter(neighbor_labels))

    agreement_with_prediction = float(np.mean(np.array(neighbor_labels) == predicted_label)) if neighbor_labels else 0.0
    agreement_with_actual = float(np.mean(np.array(neighbor_labels) == actual_label)) if neighbor_labels else 0.0

    return {
        "node_id": int(node_id),
        "neighbor_count": int(len(neighbor_ids)),
        "actual_label": int(actual_label),
        "predicted_label": int(predicted_label),
        "neighbor_label_distribution": neighbor_label_distribution,
        "agreement_with_prediction": agreement_with_prediction,
        "agreement_with_actual": agreement_with_actual,
    }
