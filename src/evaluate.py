"""Evaluation helpers for node-classification models."""

from typing import Dict, Tuple

import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Compute accuracy, precision, recall, and F1 using weighted averaging."""
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average="weighted", zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average="weighted", zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
    }


def evaluate_model(
    model: torch.nn.Module,
    x: torch.Tensor,
    edge_index: torch.Tensor,
    labels: torch.Tensor,
    split_idx: torch.Tensor,
) -> Dict[str, float]:
    """Evaluate a model on the supplied node split and return metrics."""
    model.eval()
    with torch.no_grad():
        logits, _ = model(x, edge_index)
        predictions = logits[split_idx].argmax(dim=1).cpu().numpy()
        true_labels = labels[split_idx].cpu().numpy()

    return compute_metrics(true_labels, predictions)


def generate_predictions(
    model: torch.nn.Module,
    x: torch.Tensor,
    edge_index: torch.Tensor,
    split_idx: torch.Tensor,
) -> np.ndarray:
    """Return predicted labels for the requested node split."""
    model.eval()
    with torch.no_grad():
        logits, _ = model(x, edge_index)
        predictions = logits[split_idx].argmax(dim=1).cpu().numpy()

    return predictions
