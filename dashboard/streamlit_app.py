import streamlit as st

from dashboard.utils.styles import get_dashboard_css
from dashboard.views.embedding_visualization import render_embedding_visualization
from dashboard.views.graph_statistics import render_graph_statistics
from dashboard.views.model_performance import render_model_performance
from dashboard.views.node_classification import render_node_classification
from dashboard.views.overview import render_overview


PAGES = {
    "Overview": render_overview,
    "Graph Statistics": render_graph_statistics,
    "Model Performance": render_model_performance,
    "Node Classification": render_node_classification,
    "Embedding Analysis": render_embedding_visualization,
}


def _init_state() -> None:
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Overview"
    if "theme" not in st.session_state:
        st.session_state.theme = "light"


def _get_theme() -> str:
    if st.session_state.get("theme") in {"light", "dark"}:
        return st.session_state.theme
    st.session_state.theme = "light"
    return "light"


def navigate_to(page_name: str) -> None:
    st.session_state.current_page = page_name


def set_theme(theme_name: str) -> None:
    st.session_state.theme = theme_name


def _render_sidebar() -> None:
    theme = _get_theme()
    current_page = st.session_state.current_page
    with st.sidebar:
        st.markdown(
            """
            <div class='section-card' style='padding: 1rem 1rem 0.8rem; margin-bottom: 1rem;'>
                <div class='eyebrow'>Graph Intelligence</div>
                <div class='section-title'>OGBN-Arxiv</div>
                <div class='section-subtitle'>Citation network analytics for GCN and GraphSAGE experiments.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='section-subtitle' style='margin: 0.5rem 0 0.35rem;'>Navigation</div>", unsafe_allow_html=True)
        for page_name in PAGES.keys():
            icon = "◈" if page_name == "Overview" else "◌"
            if page_name == "Graph Statistics":
                icon = "⬢"
            elif page_name == "Model Performance":
                icon = "▤"
            elif page_name == "Node Classification":
                icon = "◎"
            elif page_name == "Embedding Analysis":
                icon = "⬡"
            st.button(
                f"{icon} {page_name}",
                key=f"nav_{page_name}",
                on_click=navigate_to,
                args=(page_name,),
                use_container_width=True,
                type="primary" if current_page == page_name else "secondary",
            )

        st.markdown("<div style='height: 0.8rem'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Appearance</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.button(
                "☀ Light",
                key="theme_light",
                on_click=set_theme,
                args=("light",),
                use_container_width=True,
                type="primary" if theme == "light" else "secondary",
            )
        with col2:
            st.button(
                "☾ Dark",
                key="theme_dark",
                on_click=set_theme,
                args=("dark",),
                use_container_width=True,
                type="primary" if theme == "dark" else "secondary",
            )

        st.markdown(
            """
            <div class='section-card' style='margin-top: 1rem; padding: 0.8rem 0.9rem;'>
                <div class='metric-label'>Project</div>
                <div class='section-title' style='font-size: 0.95rem;'>CCS4354</div>
                <div class='section-subtitle' style='margin-bottom: 0;'>Tensors and Graphs</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main() -> None:
    st.set_page_config(
        page_title="OGBN-Arxiv Graph Intelligence",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    _init_state()
    theme = _get_theme()
    st.markdown(get_dashboard_css(theme), unsafe_allow_html=True)
    _render_sidebar()

    hero_col_left, hero_col_right = st.columns([1.2, 0.8])
    with hero_col_left:
        st.markdown(
            """
            <div class='hero-shell'>
                <div class='eyebrow'>Graph Intelligence Platform</div>
                <div class='hero-title'>OGBN-Arxiv Graph Intelligence</div>
                <div class='hero-subtitle'>Explore citation networks, compare GNN models, and investigate research-paper classifications through an interactive analytics platform.</div>
                <div class='hero-badges'>
                    <span class='hero-badge'>OGBN-Arxiv</span>
                    <span class='hero-badge'>GCN</span>
                    <span class='hero-badge'>GraphSAGE</span>
                    <span class='hero-badge'>40 Categories</span>
                    <span class='hero-badge'>Models Ready</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        hero_btn_col_1, hero_btn_col_2 = st.columns(2)
        current_page = st.session_state.current_page
        # Hero CTA active state follows the single source of truth: st.session_state['current_page']
        model_cta_type = "primary" if current_page in ("Model Performance", "Overview") else "secondary"
        predictions_cta_type = "primary" if current_page == "Node Classification" else "secondary"

        with hero_btn_col_1:
            st.button(
                "Explore Models",
                key="hero_models",
                on_click=navigate_to,
                args=("Model Performance",),
                use_container_width=True,
                type=model_cta_type,
            )
        with hero_btn_col_2:
            st.button(
                "Explore Predictions",
                key="hero_predictions",
                on_click=navigate_to,
                args=("Node Classification",),
                use_container_width=True,
                type=predictions_cta_type,
            )

    with hero_col_right:
        st.markdown(
            """
            <div class='hero-shell hero-graphic'>
                <div class='node' style='top:18%; left:20%;'></div>
                <div class='node' style='top:30%; left:63%;'></div>
                <div class='node' style='top:68%; left:28%;'></div>
                <div class='node' style='top:58%; left:74%;'></div>
                <svg width='100%' height='220' viewBox='0 0 320 220' style='position: absolute; inset: 0;'>
                    <path d='M65 80 L120 55 L190 75 L245 110' stroke='rgba(96,165,250,0.45)' stroke-width='2' fill='none' />
                    <path d='M120 55 L180 115 L245 110' stroke='rgba(124,58,237,0.35)' stroke-width='2' fill='none' />
                    <path d='M190 75 L180 115 L95 140' stroke='rgba(6,182,212,0.35)' stroke-width='2' fill='none' />
                </svg>
            </div>
            """,
            unsafe_allow_html=True,
        )

    current_page = st.session_state.current_page
    if current_page not in PAGES:
        current_page = "Overview"
    PAGES[current_page]()


if __name__ == "__main__":
    main()
