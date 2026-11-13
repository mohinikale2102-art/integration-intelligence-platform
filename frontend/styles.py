import streamlit as st


def apply():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --navy: #071B3A;
        --navy-light: #102B50;
        --teal: #12A89D;
        --teal-dark: #07877F;
        --canvas: #F5F7FA;
        --text: #17233B;
        --muted: #718096;
        --border: #E6EAF0;
        --white: #FFFFFF;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: var(--canvas);
        color: var(--text);
    }

    .block-container {
        max-width: 1600px;
        padding: 1.5rem 2rem 3rem;
    }

    h1, h2, h3, h4 {
        color: var(--text);
        letter-spacing: -0.035em;
        font-weight: 700;
    }

    h1 {
        font-size: 2rem !important;
    }

    h2 {
        font-size: 1.35rem !important;
    }

    h3 {
        font-size: 1.05rem !important;
    }

    p, label {
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: var(--navy);
        border-right: none;
    }

    [data-testid="stSidebar"] > div:first-child {
        background: var(--navy);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #D5DFEE;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.14);
    }

    [data-testid="stSidebar"] .stCaption {
        color: #91A5C0;
    }

    [data-testid="stSidebar"] div.stButton > button {
        width: 100%;
        min-height: 43px;
        text-align: left;
        border: 1px solid transparent;
        border-radius: 8px;
        background: transparent;
        color: #D5DFEE;
        font-weight: 500;
        padding: 0.55rem 0.9rem;
        transition: all 0.15s ease;
    }

    [data-testid="stSidebar"] div.stButton > button:hover {
        background: var(--navy-light);
        border-color: rgba(255,255,255,0.10);
        color: white;
    }

    [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background: #123B5C;
        color: white;
        border-left: 3px solid var(--teal);
        border-radius: 5px 8px 8px 5px;
    }

    div.stButton > button {
        border-radius: 8px;
        border: 1px solid var(--border);
        font-weight: 600;
        min-height: 38px;
    }

    div.stButton > button[kind="primary"] {
        background: var(--teal);
        border-color: var(--teal);
        color: white;
    }

    div.stButton > button[kind="primary"]:hover {
        background: var(--teal-dark);
        border-color: var(--teal-dark);
    }

    [data-testid="stMetric"] {
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 7px rgba(15, 23, 42, 0.035);
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
        font-size: 0.85rem;
        font-weight: 500;
    }

    [data-testid="stMetricValue"] {
        color: var(--text);
        font-weight: 700;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.78rem;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }

    [data-testid="stPlotlyChart"] {
        background: white;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 10px;
    }

    [data-testid="stTextInput"] input {
        border-radius: 8px;
        border-color: var(--border);
    }

    [data-testid="stSelectbox"] > div > div {
        border-radius: 8px;
    }

    .brand {
        color: white;
        font-size: 19px;
        font-weight: 800;
        line-height: 1.35;
        letter-spacing: -0.5px;
        padding: 12px 4px 5px;
    }

    .brand-mark {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        margin-right: 8px;
        border-radius: 9px;
        background: var(--teal);
        color: white;
        font-size: 19px;
        vertical-align: middle;
    }

    .sidebar-caption {
        color: #91A5C0 !important;
        font-size: 12px;
        margin: 0 4px 15px;
    }

    .page-subtitle {
        color: var(--muted);
        font-size: 0.91rem;
        margin-top: -12px;
        margin-bottom: 24px;
    }

    .eyebrow {
        color: var(--teal-dark);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .panel-title {
        color: var(--text);
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .status-pill {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }

    .status-healthy {
        background: #E5F7F1;
        color: #087B58;
    }

    .status-warning {
        background: #FFF4DF;
        color: #A56A08;
    }

    .status-error {
        background: #FDECEC;
        color: #C03939;
    }

    .status-info {
        background: #EAF2FF;
        color: #2861A8;
    }

    .info-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 17px 19px;
        margin-bottom: 12px;
    }

    .info-card-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 5px;
    }

    .info-card-description {
        color: var(--muted);
        font-size: 0.82rem;
        line-height: 1.5;
    }

    .system-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        padding: 11px 0;
        border-bottom: 1px solid #EEF1F5;
        font-size: 0.84rem;
    }

    .system-row:last-child {
        border-bottom: none;
    }

    .system-name {
        color: var(--text);
        font-weight: 500;
    }

    .muted-text {
        color: var(--muted);
        font-size: 0.8rem;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    </style>
    """, unsafe_allow_html=True)


def header(title, subtitle):
    st.markdown(f"""
        <div class="eyebrow">INTEGRATION INTELLIGENCE PLATFORM</div>
        <h1 style="margin-bottom: 16px;">{title}</h1>
        <div class="page-subtitle">{subtitle}</div>
    """, unsafe_allow_html=True)


def section_title(title, description=None):
    st.markdown(f'<div class="panel-title">{title}</div>', unsafe_allow_html=True)
    if description:
        st.caption(description)