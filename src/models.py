"""Graph Neural Network models for node classification on OGBN-Arxiv."""

import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv, SAGEConv


class GCN(nn.Module):
    """Graph Convolutional Network for node classification."""

    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        num_layers: int = 2,
        dropout: float = 0.3,
    ):
        """
        Initialize GCN model.
        
        Args:
            input_dim: Input feature dimension
            hidden_dim: Hidden layer dimension
            output_dim: Output dimension (number of classes)
            num_layers: Number of GCN layers
            dropout: Dropout rate
        """
        super().__init__()
        self.num_layers = num_layers
        self.dropout_rate = dropout

        layers = []
        for i in range(num_layers):
            in_dim = input_dim if i == 0 else hidden_dim
            out_dim = output_dim if i == num_layers - 1 else hidden_dim
            layers.append(GCNConv(in_dim, out_dim))

        self.layers = nn.ModuleList(layers)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor):
        """
        Forward pass through the GCN model.
        
        Args:
            x: Node feature matrix [num_nodes, input_dim]
            edge_index: Edge index tensor [2, num_edges]
            
        Returns:
            logits: Classification logits [num_nodes, output_dim]
            embeddings: Hidden embeddings [num_nodes, hidden_dim]
        """
        embeddings = None

        for idx, layer in enumerate(self.layers):
            x = layer(x, edge_index)

            if idx < self.num_layers - 1:
                x = self.relu(x)
                x = self.dropout(x)
                embeddings = x
            else:
                # Store embeddings before final output layer
                if embeddings is None:
                    embeddings = x

        logits = x
        return logits, embeddings


class GraphSAGE(nn.Module):
    """GraphSAGE model for node classification."""

    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        output_dim: int,
        num_layers: int = 2,
        dropout: float = 0.3,
    ):
        """
        Initialize GraphSAGE model.
        
        Args:
            input_dim: Input feature dimension
            hidden_dim: Hidden layer dimension
            output_dim: Output dimension (number of classes)
            num_layers: Number of SAGE layers
            dropout: Dropout rate
        """
        super().__init__()
        self.num_layers = num_layers
        self.dropout_rate = dropout

        layers = []
        for i in range(num_layers):
            in_dim = input_dim if i == 0 else hidden_dim
            out_dim = output_dim if i == num_layers - 1 else hidden_dim
            layers.append(SAGEConv(in_dim, out_dim))

        self.layers = nn.ModuleList(layers)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor):
        """
        Forward pass through the GraphSAGE model.
        
        Args:
            x: Node feature matrix [num_nodes, input_dim]
            edge_index: Edge index tensor [2, num_edges]
            
        Returns:
            logits: Classification logits [num_nodes, output_dim]
            embeddings: Hidden embeddings [num_nodes, hidden_dim]
        """
        embeddings = None

        for idx, layer in enumerate(self.layers):
            x = layer(x, edge_index)

            if idx < self.num_layers - 1:
                x = self.relu(x)
                x = self.dropout(x)
                embeddings = x
            else:
                # Store embeddings before final output layer
                if embeddings is None:
                    embeddings = x

        logits = x
        return logits, embeddings
