import streamlit as st
import plotly.graph_objects as go
from PIL import Image

from dashboard.utils.loaders import load_figure_path, load_hyperparameter_results, load_model_metrics
from dashboard.utils.styles import get_plotly_theme


def render_model_performance() -> None:
    st.markdown(
        """
        <div class='section-card'>
            <div class='section-title'>Model Performance</div>
            <div class='section-subtitle'>Compare GCN and GraphSAGE across validation and test evaluation metrics.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metrics = load_model_metrics()
    if metrics is None or metrics.empty:
        st.error("Model metrics are currently unavailable.")
        return

    required_cols = ["Model", "Dataset Split", "Accuracy", "Precision", "Recall", "F1 Score"]
    missing_cols = [col for col in required_cols if col not in metrics.columns]
    if missing_cols:
        st.error(f"Missing required columns: {', '.join(missing_cols)}")
        return

    theme = st.session_state.get("theme", "light")
    plot_theme = get_plotly_theme(theme)

    metric_cols = st.columns(2)
    for idx, model_name in enumerate(["GCN", "GraphSAGE"]):
        with metric_cols[idx]:
            model_rows = metrics[metrics["Model"] == model_name]
            if not model_rows.empty:
                val_acc = model_rows[model_rows["Dataset Split"] == "Validation"]["Accuracy"]
                test_acc = model_rows[model_rows["Dataset Split"] == "Test"]["Accuracy"]
                test_prec = model_rows[model_rows["Dataset Split"] == "Test"]["Precision"]
                test_rec = model_rows[model_rows["Dataset Split"] == "Test"]["Recall"]
                test_f1 = model_rows[model_rows["Dataset Split"] == "Test"]["F1 Score"]

                val_acc_str = f"{val_acc.iloc[0] * 100:.2f}%" if not val_acc.empty else "—"
                test_acc_str = f"{test_acc.iloc[0] * 100:.2f}%" if not test_acc.empty else "—"
                test_prec_str = f"{test_prec.iloc[0] * 100:.2f}%" if not test_prec.empty else "—"
                test_rec_str = f"{test_rec.iloc[0] * 100:.2f}%" if not test_rec.empty else "—"
                test_f1_str = f"{test_f1.iloc[0] * 100:.2f}%" if not test_f1.empty else "—"

                st.markdown(
                    f"""
                    <div class='kpi-card'>
                        <div class='section-title'>{model_name}</div>
                        <div class='metric-caption'>Validation Accuracy: <strong>{val_acc_str}</strong></div>
                        <div class='metric-caption'>Test Accuracy: <strong>{test_acc_str}</strong></div>
                        <div class='metric-caption'>Test F1: <strong>{test_f1_str}</strong></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div class='section-card'><div class='section-title'>Metric Comparison</div><div class='section-subtitle'>Select a metric and split to inspect the available evaluation values.</div></div>", unsafe_allow_html=True)
    metric_choice = st.selectbox("Metric", ["Accuracy", "Precision", "Recall", "F1 Score"], index=0)
    split_choice = st.selectbox("Dataset Split", ["Validation", "Test"], index=1)

    filtered = metrics[metrics["Dataset Split"] == split_choice]
    if not filtered.empty:
        plot_df = filtered[["Model", metric_choice]].copy()
        plot_df[metric_choice] = plot_df[metric_choice] * 100

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=plot_df["Model"],
            y=plot_df[metric_choice],
            marker_color=["#3B82F6", "#8B5CF6"],
            text=[f"{value:.2f}%" for value in plot_df[metric_choice]],
            textposition="outside",
        ))
        fig.update_layout(
            margin=dict(l=10, r=10, t=20, b=12),
            height=330,
            showlegend=False,
            xaxis_title="Model",
            yaxis_title="Score (%)",
            paper_bgcolor=plot_theme["paper_bgcolor"],
            plot_bgcolor=plot_theme["plot_bgcolor"],
            font=dict(color=plot_theme["font_color"]),
            xaxis=dict(gridcolor=plot_theme["grid_color"]),
            yaxis=dict(gridcolor=plot_theme["grid_color"]),
        )
        st.plotly_chart(fig, use_container_width=True)

        best_row = filtered.sort_values(metric_choice, ascending=False).iloc[0]
        st.markdown(
            f"""
            <div class='kpi-card'>
                <div class='metric-label'>Best Model ({split_choice})</div>
                <div class='metric-value'>{best_row['Model']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    tuning_df = load_hyperparameter_results()
    with st.expander("Hyperparameter Optimization", expanded=False):
        if tuning_df is None or tuning_df.empty:
            st.info("Hyperparameter tuning results are not available.")
        else:
            display_cols = [col for col in ["model", "learning_rate", "hidden_channels", "dropout", "num_layers", "validation_accuracy"] if col in tuning_df.columns]
            if display_cols:
                st.dataframe(tuning_df[display_cols], use_container_width=True, hide_index=True)

    st.markdown("<div class='section-card'><div class='section-title'>Training History</div><div class='section-subtitle'>The training progression associated with the project experiments.</div></div>", unsafe_allow_html=True)
    training_path = load_figure_path("training_history.png")
    if training_path is not None:
        try:
            st.image(Image.open(training_path), use_container_width=True)
        except Exception:
            st.info("Could not load training history.")
    else:
        st.info("Training history figure is not available.")

