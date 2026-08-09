import streamlit as st
from PIL import Image

from dashboard.utils.loaders import load_figure_path, load_graph_statistics


def render_graph_statistics() -> None:
    st.markdown(
        """
        <div class='section-card'>
            <div class='section-title'>Graph Statistics</div>
            <div class='section-subtitle'>Explore the structural characteristics of the OGBN-Arxiv citation network.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    graph_stats = load_graph_statistics()
    if graph_stats is None:
        st.error("Graph statistics are currently unavailable.")
        return

    cards = [
        ("Nodes", f"{int(graph_stats.get('number_of_nodes', 0)):,}"),
        ("Edges", f"{int(graph_stats.get('number_of_edges', 0)):,}"),
        ("Density", f"{graph_stats.get('density', 0):.3e}"),
        ("Avg In-Degree", f"{graph_stats.get('average_in_degree', 0):.2f}"),
        ("Avg Out-Degree", f"{graph_stats.get('average_out_degree', 0):.2f}"),
        ("Connected Components", f"{int(graph_stats.get('connected_components', 0))}"),
    ]

    cols = st.columns(3)
    for idx, (label, value) in enumerate(cards):
        col = cols[idx % 3]
        with col:
            st.markdown(
                f"""
                <div class='kpi-card'>
                    <div class='metric-label'>{label}</div>
                    <div class='metric-value'>{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div class='section-card'><div class='section-title'>Degree Distribution</div><div class='section-subtitle'>The distribution of node degrees across the citation graph.</div></div>", unsafe_allow_html=True)
    degree_path = load_figure_path("degree_distribution.png")
    if degree_path is not None:
        try:
            st.image(Image.open(degree_path), use_container_width=True)
        except Exception:
            st.info("Could not load the degree distribution figure.")
    else:
        st.info("The degree distribution figure is not available.")

    graph_cols = st.columns([1.15, 0.85])
    with graph_cols[0]:
        st.markdown("<div class='section-card'><div class='section-title'>Citation Network Sample</div><div class='section-subtitle'>A representative view of the citation relationships in the dataset.</div></div>", unsafe_allow_html=True)
        sample_path = load_figure_path("sample_subgraph.png")
        if sample_path is not None:
            try:
                st.image(Image.open(sample_path), use_container_width=True)
            except Exception:
                st.info("Could not load the sample subgraph figure.")
        else:
            st.info("The sample subgraph figure is not available.")

    with graph_cols[1]:
        st.markdown("<div class='section-card'><div class='section-title'>Structural Summary</div><div class='section-subtitle'>Additional graph-level details from the project statistics.</div></div>", unsafe_allow_html=True)
        info_items = [
            ("Features", int(graph_stats.get("feature_dimension", 0))),
            ("Classes", int(graph_stats.get("number_of_classes", 0))),
            ("Largest Component %", f"{graph_stats.get('largest_component_size', 0) / max(graph_stats.get('number_of_nodes', 1), 1) * 100:.1f}%"),
        ]
        for label, value in info_items:
            st.markdown(
                f"""
                <div class='kpi-card'>
                    <div class='metric-label'>{label}</div>
                    <div class='metric-value'>{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
