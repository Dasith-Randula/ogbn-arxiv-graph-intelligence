"""Reusable preprocessing helpers for GNN experiments."""

from typing import Dict, Tuple

import numpy as np
import torch
from sklearn.preprocessing import StandardScaler


def extract_node_features(features: torch.Tensor | np.ndarray) -> torch.Tensor:
    """Convert node features to a float tensor."""
    if isinstance(features, torch.Tensor):
        return features.float()
    return torch.tensor(features, dtype=torch.float32)


def extract_labels(labels: torch.Tensor | np.ndarray) -> torch.Tensor:
    """Convert labels to a long tensor."""
    if isinstance(labels, torch.Tensor):
        return labels.long()
    return torch.tensor(labels, dtype=torch.long)


def get_train_valid_test_idx(
    num_nodes: int,
    train_ratio: float = 0.6,
    valid_ratio: float = 0.2,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Create a simple random train/validation/test split without leakage."""
    indices = np.arange(num_nodes)
    np.random.shuffle(indices)

    train_size = int(num_nodes * train_ratio)
    valid_size = int(num_nodes * valid_ratio)
    train_idx = torch.tensor(indices[:train_size], dtype=torch.long)
    valid_idx = torch.tensor(indices[train_size : train_size + valid_size], dtype=torch.long)
    test_idx = torch.tensor(indices[train_size + valid_size :], dtype=torch.long)

    return train_idx, valid_idx, test_idx


def get_official_splits(
    train_idx: torch.Tensor,
    valid_idx: torch.Tensor,
    test_idx: torch.Tensor,
) -> Dict[str, torch.Tensor]:
    """Wrap split indices in a reusable dictionary."""
    return {"train": train_idx, "valid": valid_idx, "test": test_idx}


def normalize_features(
    features: torch.Tensor,
    train_idx: torch.Tensor,
) -> torch.Tensor:
    """Normalize features using training statistics only."""
    feature_array = features.cpu().numpy()
    train_features = feature_array[train_idx.cpu().numpy()]

    scaler = StandardScaler()
    scaler.fit(train_features)
    normalized = scaler.transform(feature_array)
    return torch.tensor(normalized, dtype=torch.float32)


def safe_std(values: torch.Tensor) -> float:
    """Return a safe standard deviation, avoiding divide-by-zero issues."""
    std = torch.std(values.float())
    return float(std.item()) if std.numel() else 0.0


def convert_to_undirected(edge_index: torch.Tensor) -> torch.Tensor:
    """Create an undirected edge index for message passing while preserving the original graph."""
    reverse_edge_index = torch.stack([edge_index[1], edge_index[0]])
    undirected = torch.cat([edge_index, reverse_edge_index], dim=1)
    return torch.unique(undirected, dim=1)
