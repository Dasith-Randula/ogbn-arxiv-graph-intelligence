import streamlit as st
import plotly.graph_objects as go
from PIL import Image

from dashboard.utils.loaders import load_figure_path, load_graph_statistics, load_model_metrics
from dashboard.utils.styles import get_plotly_theme


def render_overview() -> None:
    graph_stats = load_graph_statistics()
    metrics = load_model_metrics()
    theme = st.session_state.get("theme", "light")
    plot_theme = get_plotly_theme(theme)

    st.markdown(
        """
        <div class='section-card'>
            <div class='section-title'>Overview</div>
            <div class='section-subtitle'>A high-level view of the citation network, model quality, and the analytical capabilities available in the workspace.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if graph_stats is not None:
        cols = st.columns(4)
        cards = [
            ("Total Papers", int(graph_stats.get("number_of_nodes", 0)), "Research papers in graph"),
            ("Citation Links", int(graph_stats.get("number_of_edges", 0)), "Directed citation relationships"),
            ("Research Categories", int(graph_stats.get("number_of_classes", 0)), "Prediction targets represented"),
            ("Feature Dimension", int(graph_stats.get("feature_dimension", 0)), "Input embedding size"),
        ]
        for col, (label, value, caption) in zip(cols, cards):
            with col:
                st.markdown(
                    f"""
                    <div class='kpi-card'>
                        <div class='metric-label'>{label}</div>
                        <div class='metric-value'>{value:,}</div>
                        <div class='metric-caption'>{caption}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.warning("Graph statistics are currently unavailable.")

    main_cols = st.columns([1.7, 0.95])
    with main_cols[0]:
        st.markdown("<div class='section-card'><div class='section-title'>Model Performance Overview</div><div class='section-subtitle'>Comparison of GCN and GraphSAGE over the available test metrics.</div></div>", unsafe_allow_html=True)
        if metrics is not None and not metrics.empty:
            test_rows = metrics[metrics["Dataset Split"] == "Test"].copy()
            if not test_rows.empty:
                plot_df = test_rows[["Model", "Accuracy", "Precision", "Recall", "F1 Score"]].copy()
                plot_df["Accuracy"] = plot_df["Accuracy"] * 100
                plot_df["Precision"] = plot_df["Precision"] * 100
                plot_df["Recall"] = plot_df["Recall"] * 100
                plot_df["F1 Score"] = plot_df["F1 Score"] * 100

                fig = go.Figure()
                fig.add_trace(go.Bar(x=plot_df["Model"], y=plot_df["Accuracy"], name="Accuracy", marker_color="#3B82F6"))
                fig.add_trace(go.Bar(x=plot_df["Model"], y=plot_df["Precision"], name="Precision", marker_color="#8B5CF6"))
                fig.add_trace(go.Bar(x=plot_df["Model"], y=plot_df["Recall"], name="Recall", marker_color="#06B6D4"))
                fig.add_trace(go.Bar(x=plot_df["Model"], y=plot_df["F1 Score"], name="F1 Score", marker_color="#10B981"))
                fig.update_layout(
                    barmode="group",
                    margin=dict(l=10, r=10, t=25, b=10),
                    height=360,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
                    xaxis_title="Model",
                    yaxis_title="Score (%)",
                    paper_bgcolor=plot_theme["paper_bgcolor"],
                    plot_bgcolor=plot_theme["plot_bgcolor"],
                    font=dict(color=plot_theme["font_color"]),
                    xaxis=dict(gridcolor=plot_theme["grid_color"]),
                    yaxis=dict(gridcolor=plot_theme["grid_color"]),
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No test metrics could be read from the metrics file.")
        else:
            st.info("Model metrics are currently unavailable.")

    with main_cols[1]:
        st.markdown("<div class='section-card'><div class='section-title'>Best Performing Model</div><div class='section-subtitle'>Best performance observed in this experiment, based on the available test metrics.</div></div>", unsafe_allow_html=True)
        if metrics is not None and not metrics.empty:
            test_rows = metrics[metrics["Dataset Split"] == "Test"].copy()
            if not test_rows.empty:
                best_row = test_rows.sort_values("F1 Score", ascending=False).iloc[0]
                st.markdown(
                    f"""
                    <div class='kpi-card'>
                        <div class='metric-label'>Model</div>
                        <div class='metric-value'>{best_row['Model']}</div>
                        <div class='metric-caption'>Selected from the available test metrics.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"""
                    <div class='kpi-card'>
                        <div class='metric-label'>Test Accuracy</div>
                        <div class='metric-value'>{best_row['Accuracy'] * 100:.2f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"""
                    <div class='kpi-card'>
                        <div class='metric-label'>Test F1 Score</div>
                        <div class='metric-value'>{best_row['F1 Score'] * 100:.2f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info("Metrics were not available for the best-model summary.")
        else:
            st.info("Metrics were not available for the best-model summary.")

    snapshot_cols = st.columns([1.15, 0.85])
    with snapshot_cols[0]:
        st.markdown("<div class='section-card'><div class='section-title'>Citation Network Snapshot</div><div class='section-subtitle'>A representative graph sample from the project figures.</div></div>", unsafe_allow_html=True)
        sample_path = load_figure_path("sample_subgraph.png")
        if sample_path is not None:
            try:
                st.image(Image.open(sample_path), use_container_width=True)
            except Exception:
                st.info("The sample subgraph figure could not be displayed.")
        else:
            st.info("The sample graph figure is not available.")

    with snapshot_cols[1]:
        st.markdown("<div class='section-card'><div class='section-title'>Dataset Structure</div><div class='section-subtitle'>Key structural indicators from the graph statistics file.</div></div>", unsafe_allow_html=True)
        if graph_stats is not None:
            info_items = [
                ("Graph Density", f"{graph_stats.get('density', 0):.3e}"),
                ("Average In-Degree", f"{graph_stats.get('average_in_degree', 0):.2f}"),
                ("Average Out-Degree", f"{graph_stats.get('average_out_degree', 0):.2f}"),
                ("Connected Components", int(graph_stats.get('connected_components', 0))),
                ("Largest Component", int(graph_stats.get('largest_component_size', 0))),
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
        else:
            st.info("Graph statistics were not available for the snapshot section.")

    st.markdown("<div class='section-card'><div class='section-title'>Analytical Capabilities</div></div>", unsafe_allow_html=True)
    capability_cols = st.columns(4)
    capabilities = [
        ("Graph Analytics", "Structural metrics and degree analysis."),
        ("Model Evaluation", "Validation and test metric comparisons."),
        ("Node Classification", "Inspect predictions and confidence patterns."),
        ("Embedding Analysis", "Visualize learned representation space."),
    ]
    for col, (title, body) in zip(capability_cols, capabilities):
        with col:
            st.markdown(
                f"""
                <div class='kpi-card'>
                    <div class='section-title'>{title}</div>
                    <div class='metric-caption'>{body}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
