"""Graph-analysis utilities for citation-network statistics."""

from collections import deque
from typing import Dict, List, Tuple

import numpy as np
import torch


def compute_in_degree(num_nodes: int, edge_index: torch.Tensor) -> torch.Tensor:
    """Compute in-degree for each node."""
    degree = torch.zeros(num_nodes, dtype=torch.long)
    for src, dst in edge_index.t():
        degree[dst.item()] += 1
    return degree


def compute_out_degree(num_nodes: int, edge_index: torch.Tensor) -> torch.Tensor:
    """Compute out-degree for each node."""
    degree = torch.zeros(num_nodes, dtype=torch.long)
    for src, dst in edge_index.t():
        degree[src.item()] += 1
    return degree


def compute_total_degree(num_nodes: int, edge_index: torch.Tensor) -> torch.Tensor:
    """Compute total degree for each node."""
    return compute_in_degree(num_nodes, edge_index) + compute_out_degree(num_nodes, edge_index)


def compute_density(num_nodes: int, num_edges: int) -> float:
    """Compute the graph density as edges divided by possible directed pairs."""
    if num_nodes <= 1:
        return 0.0
    max_possible = num_nodes * (num_nodes - 1)
    return float(num_edges / max_possible) if max_possible else 0.0


def compute_connected_components(num_nodes: int, edge_index: torch.Tensor) -> int:
    """Count connected components in the undirected projection of the graph."""
    adjacency: List[List[int]] = [[] for _ in range(num_nodes)]
    for src, dst in edge_index.t():
        s, d = int(src.item()), int(dst.item())
        adjacency[s].append(d)
        adjacency[d].append(s)

    visited = [False] * num_nodes
    components = 0

    for start in range(num_nodes):
        if visited[start]:
            continue
        components += 1
        queue = deque([start])
        visited[start] = True
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)

    return components


def largest_component_size(num_nodes: int, edge_index: torch.Tensor) -> int:
    """Return the size of the largest connected component."""
    adjacency: List[List[int]] = [[] for _ in range(num_nodes)]
    for src, dst in edge_index.t():
        s, d = int(src.item()), int(dst.item())
        adjacency[s].append(d)
        adjacency[d].append(s)

    visited = [False] * num_nodes
    best = 0

    for start in range(num_nodes):
        if visited[start]:
            continue
        queue = deque([start])
        visited[start] = True
        size = 0
        while queue:
            node = queue.popleft()
            size += 1
            for neighbor in adjacency[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        best = max(best, size)

    return best


def largest_component_percentage(num_nodes: int, edge_index: torch.Tensor) -> float:
    """Return the percentage size of the largest component."""
    if num_nodes <= 0:
        return 0.0
    return largest_component_size(num_nodes, edge_index) / num_nodes * 100.0


def prepare_sample_subgraph(
    edge_index: torch.Tensor,
    num_nodes: int,
    max_edges: int = 50,
) -> torch.Tensor:
    """Return a small directed subgraph for visualization."""
    if edge_index.numel() == 0:
        return edge_index

    sample_edges = edge_index[:, : min(max_edges, edge_index.size(1))]
    return sample_edges


def compute_graph_stats(
    num_nodes: int,
    num_edges: int,
    edge_index: torch.Tensor,
    labels: torch.Tensor,
    features: torch.Tensor,
) -> Dict[str, float]:
    """Build a reusable graph statistics dictionary."""
    in_degree = compute_in_degree(num_nodes, edge_index)
    out_degree = compute_out_degree(num_nodes, edge_index)

    stats = {
        "number_of_nodes": int(num_nodes),
        "number_of_edges": int(num_edges),
        "density": compute_density(num_nodes, num_edges),
        "average_in_degree": float(in_degree.float().mean().item()),
        "average_out_degree": float(out_degree.float().mean().item()),
        "connected_components": int(compute_connected_components(num_nodes, edge_index)),
        "largest_component_size": int(largest_component_size(num_nodes, edge_index)),
        "largest_component_percentage": float(largest_component_percentage(num_nodes, edge_index)),
        "feature_dimension": int(features.shape[1]),
        "number_of_classes": int(torch.unique(labels).numel()),
    }
    return stats


def compute_degree_distribution(num_nodes: int, edge_index: torch.Tensor) -> Tuple[np.ndarray, np.ndarray]:
    """Return unique degrees and their counts for the graph."""
    degree = compute_total_degree(num_nodes, edge_index).cpu().numpy()
    unique_degrees, counts = np.unique(degree, return_counts=True)
    return unique_degrees, counts
