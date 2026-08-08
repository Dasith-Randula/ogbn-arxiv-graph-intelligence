# OGBN-Arxiv Graph Intelligence

A Graph Neural Network based research project developed for the **CCS4354 – Tensors and Graphs** coursework at SLTC Research University.

The project uses the **OGBN-Arxiv** citation network to analyze relationships between scientific papers and predict their research categories using Graph Neural Networks.

---

## About the Project

OGBN-Arxiv is a large-scale citation network where:

- **Nodes** represent scientific research papers
- **Edges** represent citation relationships
- Each paper contains a **128-dimensional feature vector**
- The objective is to perform **node classification** and predict the research category of each paper

The project covers graph analysis, graph data preparation, GNN development, model training, evaluation, explainability, and visualization.

---

## Main Features

- Tensor operations using PyTorch
- OGBN-Arxiv graph analysis
- Degree and graph structure analysis
- Graph Neural Network development
- Comparison of two GNN architectures
- Model training and hyperparameter optimization
- Accuracy, Precision, Recall, and F1 evaluation
- Node embedding visualization using PCA or t-SNE
- Graph explainability analysis
- Interactive Streamlit dashboard

---

## Graph Intelligence Dashboard

The Streamlit dashboard provides a simple and interactive way to explore the project results.

It includes:

- Graph statistics
- Model performance metrics
- Node classification results
- Node embedding visualizations
- Light and dark interface support

---

## Technologies

- Python
- PyTorch
- PyTorch Geometric
- Open Graph Benchmark
- NumPy
- Pandas
- Scikit-learn
- NetworkX
- Matplotlib
- Plotly
- Streamlit
- Jupyter Notebook

---

## Project Structure

```text
CCS4354-OGBN-Arxiv-GNN/
│
├── data/
├── notebooks/
├── models/
├── results/
├── dashboard/
├── report/
├── presentation/
│
├── requirements.txt
├── .gitignore
└── README.md
