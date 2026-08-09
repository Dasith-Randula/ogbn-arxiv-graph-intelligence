import streamlit as st

from dashboard.utils.loaders import load_predictions


def render_node_classification() -> None:
    st.markdown(
        """
        <div class='section-card'>
            <div class='section-title'>Node Classification Explorer</div>
            <div class='section-subtitle'>Inspect real test-set predictions produced by GCN and GraphSAGE.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    predictions = load_predictions()
    if predictions is None or predictions.empty:
        st.error("Node prediction data is currently unavailable.")
        return

    required_cols = ["node_id", "actual_label", "gcn_prediction", "graphsage_prediction"]
    missing_cols = [col for col in required_cols if col not in predictions.columns]
    if missing_cols:
        st.error(f"Missing required columns: {', '.join(missing_cols)}")
        return

    summary_cols = st.columns(4)
    labels = [
        ("Test Nodes", len(predictions)),
        ("GCN Correct", int((predictions["actual_label"] == predictions["gcn_prediction"]).sum())),
        ("GraphSAGE Correct", int((predictions["actual_label"] == predictions["graphsage_prediction"]).sum())),
        ("Categories", int(predictions["actual_label"].nunique())),
    ]
    for col, (label, value) in zip(summary_cols, labels):
        with col:
            st.markdown(
                f"""
                <div class='kpi-card'>
                    <div class='metric-label'>{label}</div>
                    <div class='metric-value'>{value:,}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div class='section-card'><div class='section-title'>Filters</div><div class='section-subtitle'>Refine the view of paper-level predictions by model and outcome.</div></div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        model_choice = st.selectbox("Model", ["GCN", "GraphSAGE"], index=0)
    with col2:
        status_choice = st.selectbox("Status", ["All", "Correct", "Incorrect"], index=0)
    with col3:
        rows_to_show = st.selectbox("Rows", [25, 50, 100, 250], index=2)
    with col4:
        node_search = st.text_input("Node ID", placeholder="search")

    display_df = predictions.copy()
    if model_choice == "GCN":
        display_df["Predicted_Label"] = display_df["gcn_prediction"].astype(int)
        display_df["Predicted_Category"] = display_df.get("gcn_predicted_category", "—")
    else:
        display_df["Predicted_Label"] = display_df["graphsage_prediction"].astype(int)
        display_df["Predicted_Category"] = display_df.get("graphsage_predicted_category", "—")

    display_df["Correct"] = display_df["actual_label"].astype(int) == display_df["Predicted_Label"]
    if status_choice == "Correct":
        display_df = display_df[display_df["Correct"]]
    elif status_choice == "Incorrect":
        display_df = display_df[~display_df["Correct"]]

    if node_search:
        try:
            node_id = int(node_search)
            display_df = display_df[display_df["node_id"] == node_id]
        except ValueError:
            pass

    result_cols = ["node_id", "actual_label", "Predicted_Label", "Predicted_Category", "Correct"]
    result_cols = [col for col in result_cols if col in display_df.columns]
    if result_cols:
        result_df = display_df[result_cols].copy()
        result_df["Status"] = result_df["Correct"].map({True: "Correct", False: "Incorrect"})
        display_cols = ["node_id", "actual_label", "Predicted_Label", "Status"]
        result_df = result_df[display_cols].rename(columns={
            "node_id": "Node ID",
            "actual_label": "Actual Label",
            "Predicted_Label": "Predicted",
        })
        st.dataframe(result_df.head(rows_to_show), use_container_width=True, hide_index=True)
        st.caption(f"Showing {min(len(result_df), rows_to_show)} of {len(result_df)} records")

    st.markdown("<div class='section-card'><div class='section-title'>Node Inspector</div><div class='section-subtitle'>Inspect a paper by node ID and compare the actual and predicted categories.</div></div>", unsafe_allow_html=True)
    inspector_id = st.text_input("Enter node ID to inspect", placeholder="e.g., 346")
    if inspector_id:
        try:
            selected_id = int(inspector_id)
            row = predictions[predictions["node_id"] == selected_id]
            if row.empty:
                st.info(f"Node {selected_id} not found.")
            else:
                row = row.iloc[0]
                info_cols = st.columns(3)
                with info_cols[0]:
                    st.markdown(
                        f"""
                        <div class='kpi-card'>
                            <div class='metric-label'>Node ID</div>
                            <div class='metric-value'>{row['node_id']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with info_cols[1]:
                    actual_cat = row.get("actual_category", "—")
                    st.markdown(
                        f"""
                        <div class='kpi-card'>
                            <div class='metric-label'>Actual Category</div>
                            <div class='metric-value' style='font-size: 0.95rem;'>{actual_cat}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with info_cols[2]:
                    gcn_cat = row.get("gcn_predicted_category", "—")
                    sage_cat = row.get("graphsage_predicted_category", "—")
                    st.markdown(
                        f"""
                        <div class='kpi-card'>
                            <div class='metric-label'>GCN / GraphSAGE</div>
                            <div class='metric-value' style='font-size: 0.8rem;'>{gcn_cat} / {sage_cat}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        except ValueError:
            st.warning("Please enter a valid node ID.")
