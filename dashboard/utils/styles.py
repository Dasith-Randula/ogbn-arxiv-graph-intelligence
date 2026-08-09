def get_dashboard_css(theme: str = "light") -> str:
    if theme == "dark":
        colors = {
            "bg_primary": "#070B14",
            "bg_secondary": "#05060A",
            # Sidebar and surface tuned for dark
            "surface": "rgba(10,16,29,0.94)",
            "surface_solid": "#0B1220",
            "surface_hover": "#111827",
            "text_primary": "#F8FAFC",
            "text_secondary": "#CBD5E1",
            "text_muted": "#94A3B8",
            "border": "rgba(148, 163, 184, 0.13)",
            "primary": "#3B82F6",
            "primary_light": "#60A5FA",
            "purple": "#8B5CF6",
            "cyan": "#22D3EE",
            "success": "#34D399",
            "warning": "#FBBF24",
            "danger": "#F87171",
        }
    else:
        colors = {
            "bg_primary": "#F4F7FC",
            "bg_secondary": "#EFF6FF",
            # Sidebar and surface tuned for light
            "surface": "rgba(248,250,252,0.92)",
            "surface_solid": "rgba(255,255,255,0.92)",
            "surface_hover": "#F8FAFF",
            "text_primary": "#0F172A",
            "text_secondary": "#475569",
            "text_muted": "#64748B",
            "border": "rgba(148, 163, 184, 0.18)",
            "primary": "#2563EB",
            "primary_light": "#60A5FA",
            "purple": "#7C3AED",
            "cyan": "#06B6D4",
            "success": "#10B981",
            "warning": "#F59E0B",
            "danger": "#EF4444",
        }

    close_background = 'rgba(15,23,42,0.72)' if theme == 'dark' else 'rgba(255,255,255,0.85)'
    close_border = 'rgba(148,163,184,0.16)' if theme == 'dark' else 'rgba(148,163,184,0.22)'
    close_icon = '#CBD5E1' if theme == 'dark' else '#475569'
    reopen_background = 'rgba(15,23,42,0.88)' if theme == 'dark' else 'rgba(255,255,255,0.90)'
    reopen_border = 'rgba(96,165,250,0.22)' if theme == 'dark' else 'rgba(37,99,235,0.20)'
    reopen_icon = '#60A5FA' if theme == 'dark' else '#2563EB'
    reopen_hover = 'rgba(96,165,250,0.16)' if theme == 'dark' else 'rgba(59,130,246,0.14)'

    return f"""
    <style>
    :root {{
        --bg-primary: {colors['bg_primary']};
        --bg-secondary: {colors['bg_secondary']};
        --surface: {colors['surface']};
        --surface-solid: {colors['surface_solid']};
        --surface-hover: {colors['surface_hover']};
        --text-primary: {colors['text_primary']};
        --text-secondary: {colors['text_secondary']};
        --text-muted: {colors['text_muted']};
        --border: {colors['border']};
        --primary: {colors['primary']};
        --primary-light: {colors['primary_light']};
        --purple: {colors['purple']};
        --cyan: {colors['cyan']};
        --success: {colors['success']};
        --warning: {colors['warning']};
        --danger: {colors['danger']};
    }}


    html, body {{
        background: var(--bg-primary);
        color: var(--text-primary);
    }}

    /* Animated multi-layered background tuned per theme */
    .stApp {{
        min-height: 100vh;
        color: var(--text-primary);
        background-color: var(--bg-primary);
        background-image: {('radial-gradient(circle at 15% 20%, rgba(59,130,246,0.16), transparent 34%),\n            radial-gradient(circle at 85% 18%, rgba(139,92,246,0.14), transparent 32%),\n            radial-gradient(circle at 70% 78%, rgba(34,211,238,0.08), transparent 36%),\n            radial-gradient(rgba(148,163,184,0.10) 1px, transparent 1px)') if theme=='dark' else ('radial-gradient(circle at 10% 18%, rgba(37,99,235,0.10), transparent 34%),\n            radial-gradient(circle at 86% 14%, rgba(124,58,237,0.08), transparent 32%),\n            radial-gradient(circle at 70% 84%, rgba(6,182,212,0.07), transparent 36%),\n            radial-gradient(rgba(100,116,139,0.08) 1px, transparent 1px)')};
        background-size: {('cover, cover, cover, 28px 28px') if theme=='dark' else ('cover, cover, cover, 28px 28px')};
        background-position: 0% 0%, 100% 0%, 50% 100%, 0 0;
        animation: backgroundShift 18s ease-in-out infinite alternate;
        position: relative;
    }}

    /* Make header transparent and not add extra vertical height */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        border-bottom: none !important;
        box-shadow: none !important;
        padding: 0.35rem 0.5rem !important;
        height: auto !important;
        display: flex !important;
        align-items: center !important;
    }}

    /* Keep decorations/toolbars from adding extra chrome */
    [data-testid="stToolbar"], [data-testid="stDecoration"] {{
        display: none !important;
    }}

    /* Main app content should be transparent so background flows behind everything */
    [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        background: transparent !important;
    }}

    /* Gentle padding for main blocks (keeps hero visible) */
    [data-testid="stMainBlockContainer"], .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 1500px;
    }}

    .block-container {{
        padding: 1.25rem 1rem 2.5rem;
        max-width: 1500px;
    }}

    /* Subtle dot/grid layer with slow motion */
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image: radial-gradient(rgba(148,163,184,0.10) 1px, transparent 1px);
        background-size: 28px 28px;
        opacity: 0.12;
        animation: floatGrid 18s linear infinite;
    }}

    /* Floating decorative orbs to add 3D depth */
    .stApp::after {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
    }}

    /* Sidebar styling to belong to the same visual world */
    .stSidebar {{
        background: var(--surface) !important;
        border-right: 1px solid var(--border);
        backdrop-filter: blur(16px);
        box-shadow: 0 20px 60px rgba(2, 6, 23, 0.08);
    }}

    .stSidebar .sidebar-content {{
        background: transparent;
        padding: 1rem 0.65rem 1rem 0.65rem;
    }}

    /* Keep main app containers overflow-visible so controls are not clipped */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        overflow: visible !important;
    }}

    /* Force sidebar visible (prevent Streamlit from collapsing visually) */
    .stSidebar[aria-expanded="false"], .stSidebar {{
        width: 300px !important;
        min-width: 300px !important;
        display: block !important;
    }}

    /* Hide native Streamlit collapse/expand controls so the sidebar stays permanently open */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    button[data-testid="stExpandSidebarButton"],
    button[data-testid="stCollapseSidebarButton"] {{
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    

    .hero-shell, .premium-card, .kpi-card, .section-card, .inspector-card {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 22px;
        box-shadow: 0 16px 34px rgba(15, 23, 42, 0.08);
        backdrop-filter: blur(18px);
        transition: transform 260ms ease, box-shadow 260ms ease, border-color 260ms ease;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
    }}

    .hero-shell::before, .premium-card::before, .kpi-card::before, .section-card::before {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.08), transparent 60%);
        pointer-events: none;
    }}

    .hero-shell:hover, .premium-card:hover, .kpi-card:hover, .section-card:hover, .inspector-card:hover {{
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 20px 38px rgba(15, 23, 42, 0.14);
        border-color: rgba(96, 165, 250, 0.24);
    }}

    .hero-shell {{
        padding: 1.7rem 1.7rem 1.9rem;
        margin-bottom: 1.1rem;
        background: linear-gradient(135deg, rgba(37,99,235,0.16), rgba(124,58,237,0.12)), var(--surface);
        animation: fadeUp 0.65s ease both;
    }}

    .eyebrow {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        color: var(--primary);
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }}

    .hero-title {{
        font-size: 2.15rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 0.4rem;
        line-height: 1.12;
    }}

    .hero-subtitle {{
        font-size: 1rem;
        color: var(--text-secondary);
        line-height: 1.65;
        margin: 0;
    }}

    .hero-badges {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 1rem;
    }}

    .hero-badge {{
        display: inline-flex;
        align-items: center;
        padding: 0.45rem 0.7rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(148,163,184,0.18);
        color: var(--text-primary);
        font-size: 0.8rem;
        font-weight: 600;
    }}

    .hero-actions {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.7rem;
        margin-top: 1rem;
    }}

    .hero-graphic {{
        min-height: 220px;
        border-radius: 20px;
        border: 1px solid rgba(148,163,184,0.16);
        background: linear-gradient(135deg, rgba(37,99,235,0.10), rgba(59,130,246,0.06));
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem;
    }}

    .hero-graphic .node {{
        position: absolute;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), var(--cyan));
        box-shadow: 0 0 22px rgba(59,130,246,0.28);
        animation: float 5s ease-in-out infinite;
    }}

    .hero-graphic .node:nth-child(2) {{ animation-delay: 1s; }}
    .hero-graphic .node:nth-child(3) {{ animation-delay: 2s; }}
    .hero-graphic .node:nth-child(4) {{ animation-delay: 3s; }}

    .section-card, .kpi-card, .premium-card, .inspector-card {{
        padding: 1rem 1.1rem;
        margin-bottom: 1rem;
        animation: fadeUp 0.8s ease both;
    }}

    .section-title {{
        font-size: 1.08rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.2rem;
    }}

    .section-subtitle {{
        color: var(--text-secondary);
        font-size: 0.93rem;
        margin-bottom: 0.75rem;
    }}

    .metric-label {{
        font-size: 0.78rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.35rem;
    }}

    .metric-value {{
        font-size: 1.42rem;
        font-weight: 700;
        color: var(--text-primary);
    }}

    .metric-caption {{
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }}

    .pill, .status-pill {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.45rem 0.7rem;
        border-radius: 999px;
        border: 1px solid var(--border);
        background: rgba(255,255,255,0.12);
        color: var(--text-primary);
        font-size: 0.78rem;
        font-weight: 600;
    }}

    .status-pill-success {{
        color: var(--success);
        background: rgba(52, 211, 153, 0.14);
        border-color: rgba(52, 211, 153, 0.2);
    }}

    .status-pill-warning {{
        color: var(--warning);
        background: rgba(251, 191, 36, 0.13);
        border-color: rgba(251, 191, 36, 0.2);
    }}

    .status-pill-danger {{
        color: var(--danger);
        background: rgba(248, 113, 113, 0.12);
        border-color: rgba(248, 113, 113, 0.2);
    }}

    .stButton > button {{
        border-radius: 999px;
        padding: 0.6rem 0.95rem;
        border: 1px solid var(--border);
        background: var(--surface-solid);
        color: var(--text-primary);
        font-weight: 600;
        transition: transform 250ms ease, box-shadow 250ms ease, background 250ms ease;
    }}

    /* Inactive / secondary */
    .stButton > button[kind="secondary"] {{
        background: {('rgba(15,23,42,0.72)' if theme=='dark' else 'rgba(255,255,255,0.70)')};
        color: {('var(--text-secondary)' if theme=='dark' else 'var(--text-secondary)')};
        border: 1px solid {('rgba(148,163,184,0.16)' if theme=='dark' else 'rgba(148,163,184,0.25)')};
        box-shadow: none;
    }}

    /* Primary / active */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {colors['primary']}, {colors['purple']});
        color: #FFFFFF;
        border: 1px solid {('rgba(96,165,250,0.35)' if theme=='dark' else 'rgba(37,99,235,0.24)')};
        box-shadow: 0 8px 24px {('rgba(59,130,246,0.22)' if theme=='dark' else 'rgba(37,99,235,0.18)')};
        transform: translateZ(0);
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
    }}

    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stNumberInput input, .stTextArea textarea, .stMultiSelect > div > div {{
        background: var(--surface-solid) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }}

    .stSelectbox [data-baseweb="select"] > div {{
        background: var(--surface-solid) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }}

    .stDataFrame {{
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid var(--border);
    }}

    .stMetric {{
        background: var(--surface-solid);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 0.85rem 0.95rem;
    }}

    .stAlert, .stInfo, .stError, .stWarning {{
        border-radius: 16px;
        border: 1px solid var(--border);
        background: var(--surface-solid);
    }}

    .stTabs [role="tablist"] button {{
        color: var(--text-secondary);
        border-radius: 999px;
        border: 1px solid transparent;
    }}

    .stTabs [role="tablist"] button[aria-selected="true"] {{
        background: rgba(59,130,246,0.12);
        color: var(--primary);
        border-color: rgba(59,130,246,0.16);
    }}

    .stRadio > div {{
        gap: 0.45rem;
    }}

    .stRadio label {{
        border: 1px solid var(--border);
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        padding: 0.45rem 0.8rem;
        color: var(--text-secondary);
        margin-bottom: 0.35rem;
    }}

    .stRadio input:checked + div {{
        background: rgba(59,130,246,0.16);
    }}

    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(14px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
    }}

    @keyframes floatGrid {{
        0% {{ transform: translate3d(0, 0, 0); }}
        100% {{ transform: translate3d(12px, 12px, 0); }}
    }}

    @keyframes backgroundShift {{
        0% {{
            background-position: 0% 0%, 100% 0%, 50% 100%, 0 0;
        }}
        50% {{
            background-position: 5% 3%, 95% 5%, 55% 95%, 12px 12px;
        }}
        100% {{
            background-position: 0% 0%, 100% 0%, 50% 100%, 0 0;
        }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        *, *::before, *::after {{
            animation: none !important;
            transition: none !important;
        }}
    }}
    </style>
    """


def get_plotly_theme(theme: str = "light") -> dict:
    if theme == "dark":
        return {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font_color": "#CBD5E1",
            "grid_color": "rgba(148,163,184,0.10)",
            "line_color": "#3B82F6",
        }
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font_color": "#0F172A",
        "grid_color": "rgba(100,116,139,0.12)",
        "line_color": "#2563EB",
    }
