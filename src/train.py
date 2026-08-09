"""Training utilities for GNN node-classification experiments."""

import time
from typing import Any, Dict, Tuple

import torch
import torch.nn.functional as F
from torch.optim import Adam


def train_one_epoch(
    model: torch.nn.Module,
    x: torch.Tensor,
    edge_index: torch.Tensor,
    y: torch.Tensor,
    train_idx: torch.Tensor,
    optimizer: Adam,
) -> float:
    """Train a model for one epoch and return the batch loss."""
    model.train()
    optimizer.zero_grad()

    logits, _ = model(x, edge_index)
    loss = F.cross_entropy(logits[train_idx], y[train_idx])
    loss.backward()
    optimizer.step()

    return float(loss.item())


def evaluate_accuracy(
    model: torch.nn.Module,
    x: torch.Tensor,
    edge_index: torch.Tensor,
    y: torch.Tensor,
    idx: torch.Tensor,
) -> Tuple[float, torch.Tensor]:
    """Evaluate a model on a split and return accuracy plus predictions."""
    model.eval()
    with torch.no_grad():
        logits, _ = model(x, edge_index)
        predictions = logits[idx].argmax(dim=1)
        accuracy = float((predictions == y[idx]).sum().item() / len(idx))

    return accuracy, predictions


def evaluate_train_validation(
    model: torch.nn.Module,
    x: torch.Tensor,
    edge_index: torch.Tensor,
    y: torch.Tensor,
    train_idx: torch.Tensor,
    valid_idx: torch.Tensor,
) -> Dict[str, float]:
    """Return training and validation accuracies for the current model state."""
    train_acc, _ = evaluate_accuracy(model, x, edge_index, y, train_idx)
    valid_acc, _ = evaluate_accuracy(model, x, edge_index, y, valid_idx)
    return {"train_acc": train_acc, "valid_acc": valid_acc}


def train_model(
    model: torch.nn.Module,
    x: torch.Tensor,
    edge_index: torch.Tensor,
    y: torch.Tensor,
    train_idx: torch.Tensor,
    valid_idx: torch.Tensor,
    config: Dict[str, Any],
    patience: int = 3,
) -> Tuple[Dict[str, list], Dict[str, Any], float, int, float]:
    """Train a model with early stopping and return training history and best state."""
    start_time = time.time()
    optimizer = Adam(
        model.parameters(),
        lr=config.get("learning_rate", 0.01),
        weight_decay=config.get("weight_decay", 0.0),
    )

    history: Dict[str, list] = {
        "epoch": [],
        "train_loss": [],
        "train_acc": [],
        "valid_acc": [],
    }
    best_val_acc = 0.0
    best_epoch = 0
    patience_counter = 0
    best_state: Dict[str, Any] | None = None
    epochs = int(config.get("epochs", 100))

    for epoch in range(epochs):
        train_loss = train_one_epoch(model, x, edge_index, y, train_idx, optimizer)
        train_acc, _ = evaluate_accuracy(model, x, edge_index, y, train_idx)
        valid_acc, _ = evaluate_accuracy(model, x, edge_index, y, valid_idx)

        history["epoch"].append(epoch)
        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["valid_acc"].append(valid_acc)

        if valid_acc > best_val_acc:
            best_val_acc = valid_acc
            best_epoch = epoch
            patience_counter = 0
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
        else:
            patience_counter += 1
            if patience_counter >= patience:
                break

    elapsed_time = time.time() - start_time
    return history, best_state or {}, best_val_acc, best_epoch, elapsed_time
