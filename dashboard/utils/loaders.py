import json
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = PROJECT_ROOT / "results"
METRICS_DIR = RESULTS_DIR / "metrics"
PREDICTIONS_DIR = RESULTS_DIR / "predictions"
EMBEDDINGS_DIR = RESULTS_DIR / "embeddings"
FIGURES_DIR = RESULTS_DIR / "figures"


@st.cache_data(show_spinner=False)
def load_graph_statistics() -> Optional[dict]:
    """Load graph statistics from JSON file."""
    path = METRICS_DIR / "graph_statistics.json"
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_model_metrics() -> Optional[pd.DataFrame]:
    """Load model metrics from CSV file."""
    path = METRICS_DIR / "model_metrics.csv"
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_hyperparameter_results() -> Optional[pd.DataFrame]:
    """Load hyperparameter tuning results from CSV file."""
    path = METRICS_DIR / "hyperparameter_tuning.csv"
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_predictions() -> Optional[pd.DataFrame]:
    """Load node predictions from CSV file."""
    path = PREDICTIONS_DIR / "node_predictions.csv"
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_embeddings(model_name: str) -> Optional[pd.DataFrame]:
    """Load embedding data from CSV file for specified model."""
    if model_name.lower() == "gcn":
        path = EMBEDDINGS_DIR / "gcn_embeddings_pca.csv"
    elif model_name.lower() == "graphsage":
        path = EMBEDDINGS_DIR / "graphsage_embeddings_pca.csv"
    else:
        return None

    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_figure_path(filename: str) -> Optional[Path]:
    """Return path to a figure if it exists."""
    path = FIGURES_DIR / filename
    return path if path.exists() else None
