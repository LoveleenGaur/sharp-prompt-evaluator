"""
Shared theme, CSS, and UI utilities for the Prompt Engineering Lab.
"""

GLOBAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root Variables ───────────────────────── */
:root {
    --bg-base:        #06090f;
    --bg-surface:     #0c1220;
    --bg-card:        #101828;
    --bg-card-hover:  #131e30;
    --border:         rgba(255,255,255,0.07);
    --border-bright:  rgba(255,255,255,0.14);

    --gold:           #e8b84b;
    --gold-dim:       rgba(232,184,75,0.12);
    --gold-glow:      rgba(232,184,75,0.25);
    --teal:           #2dd4bf;
    --teal-dim:       rgba(45,212,191,0.12);
    --red:            #f87171;
    --red-dim:        rgba(248,113,113,0.12);
    --green:          #4ade80;
    --green-dim:      rgba(74,222,128,0.12);
    --amber:          #fbbf24;
    --amber-dim:      rgba(251,191,36,0.12);

    --text-primary:   #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted:     #4b5563;

    --radius-sm:  8px;
    --radius-md:  14px;
    --radius-lg:  20px;
    --radius-xl:  28px;
}

/* ── Base & Reset ─────────────────────────── */
html, body, .stApp {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Hide Streamlit chrome ────────────────── */
#MainMenu, footer, header,
section[data-testid="stSidebarNav"] { display: none !important; }

/* ── Scrollbar ───────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: #1e2d45; border-radius: 3px; }

/* ── Sidebar ─────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080d18 0%, #0a1220 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-secondary) !important; }

/* Sidebar nav radio */
section[data-testid="stSidebar"] .stRadio label {
    display: flex !important;
    align-items: center !important;
    padding: 10px 14px !important;
    margin: 3px 0 !important;
    border-radius: var(--radius-sm) !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
    font-size: 0.9rem !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-secondary) !important;
    border: 1px solid transparent !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(232,184,75,0.07) !important;
    color: var(--gold) !important;
    border-color: var(--gold-dim) !important;
}
section[data-testid="stSidebar"] .stRadio [data-checked="true"] + div label,
section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: var(--gold-dim) !important;
    color: var(--gold) !important;
    border-color: rgba(232,184,75,0.25) !important;
}
section[data-testid="stSidebar"] .stRadio [type="radio"] { display: none !important; }

/* ── Page title typography ───────────────── */
h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; letter-spacing: -0.03em !important; }
h2 { font-family: 'Syne', sans-serif !important; font-weight: 700 !important; }
h3 { font-family: 'Syne', sans-serif !important; font-weight: 600 !important; }

/* ── Buttons ─────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #c8922a 0%, var(--gold) 100%) !important;
    color: #06090f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s ease !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px var(--gold-glow) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Text inputs & textareas ─────────────── */
.stTextInput input,
.stTextArea textarea,
.stSelectbox select,
div[data-baseweb="select"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: rgba(232,184,75,0.5) !important;
    box-shadow: 0 0 0 3px var(--gold-dim) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: var(--text-secondary) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

/* ── Selectbox dropdown ──────────────────── */
div[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border-color: var(--border-bright) !important;
    color: var(--text-primary) !important;
}
ul[data-baseweb="menu"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-bright) !important;
}
li[role="option"] { color: var(--text-primary) !important; }
li[role="option"]:hover { background: var(--bg-card-hover) !important; }

/* ── Expanders ───────────────────────────── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-secondary) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.streamlit-expanderContent {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
}

/* ── Metrics ─────────────────────────────── */
div[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 18px !important;
}
div[data-testid="metric-container"] label {
    color: var(--text-secondary) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* ── Alerts / Info boxes ─────────────────── */
.stAlert {
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--border) !important;
}

/* ── Code blocks ─────────────────────────── */
code, pre {
    font-family: 'JetBrains Mono', monospace !important;
    background: #0a0f1a !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
}

/* ── Divider ─────────────────────────────── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* ── Caption / helper text ───────────────── */
.stCaption, small, caption {
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
}

/* ── Spinner ─────────────────────────────── */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* ── Tooltips ────────────────────────────── */
.stTooltipIcon { color: var(--text-muted) !important; }

/* ── Sharp card components ───────────────── */
.sharp-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 28px 32px;
    margin-bottom: 20px;
    transition: border-color 0.2s;
}
.sharp-card:hover { border-color: var(--border-bright); }

.sharp-card-accent {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    border-radius: var(--radius-md);
    padding: 20px 24px;
    margin-bottom: 14px;
}

/* Score display */
.score-hero {
    background: radial-gradient(ellipse at 50% 0%, rgba(232,184,75,0.15) 0%, transparent 70%),
                var(--bg-card);
    border: 1px solid var(--border-bright);
    border-radius: var(--radius-xl);
    padding: 40px 32px;
    text-align: center;
    margin-bottom: 28px;
}
.score-hero .score-number {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.04em;
    margin-bottom: 8px;
}
.score-hero .score-rating {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    opacity: 0.9;
}
.score-hero .score-bar-track {
    background: rgba(255,255,255,0.07);
    border-radius: 99px;
    height: 8px;
    margin: 20px auto 0;
    max-width: 320px;
    overflow: hidden;
}
.score-hero .score-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 1s cubic-bezier(0.16,1,0.3,1);
}

/* Dimension rows */
.dim-row {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin-bottom: 10px;
}
.dim-letter {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--gold);
    min-width: 32px;
    line-height: 1;
    margin-top: 2px;
}
.dim-body { flex: 1; }
.dim-name {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.92rem;
    margin-bottom: 4px;
}
.dim-desc {
    color: var(--text-secondary);
    font-size: 0.88rem;
    line-height: 1.55;
}
.dim-badge {
    padding: 3px 12px;
    border-radius: 99px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    font-weight: 500;
    white-space: nowrap;
}
.badge-0 { background: rgba(248,113,113,0.15); color: #f87171; }
.badge-1 { background: rgba(251,191,36,0.15);  color: #fbbf24; }
.badge-2 { background: rgba(74,222,128,0.15);  color: #4ade80; }

/* Improved prompt box */
.improved-prompt-box {
    background: #080f1a;
    border: 1px solid rgba(45,212,191,0.25);
    border-radius: var(--radius-md);
    padding: 22px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.87rem;
    line-height: 1.75;
    color: #c8e6ff;
    white-space: pre-wrap;
    position: relative;
}
.improved-prompt-box::before {
    content: 'IMPROVED PROMPT';
    position: absolute;
    top: -11px;
    left: 16px;
    background: #080f1a;
    padding: 0 8px;
    font-size: 0.68rem;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.12em;
    color: var(--teal);
    border: 1px solid rgba(45,212,191,0.25);
    border-radius: 4px;
}

/* Tips */
.tip-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    background: rgba(232,184,75,0.04);
    border: 1px solid rgba(232,184,75,0.12);
    border-radius: var(--radius-sm);
}
.tip-num {
    background: var(--gold);
    color: #06090f;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 0.75rem;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}
.tip-text {
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.5;
}

/* Template card */
.template-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px 24px;
    margin-bottom: 14px;
    transition: all 0.2s ease;
    cursor: default;
}
.template-card:hover {
    border-color: var(--border-bright);
    transform: translateY(-1px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
.template-cat {
    display: inline-block;
    font-size: 0.7rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--gold);
    background: var(--gold-dim);
    padding: 3px 10px;
    border-radius: 99px;
    margin-bottom: 10px;
}
.template-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: var(--text-primary);
    margin-bottom: 6px;
}
.template-desc {
    font-size: 0.87rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

/* Section labels */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Pill badge (difficulty, domain) */
.pill {
    display: inline-block;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 3px 10px;
    border-radius: 99px;
    margin-right: 6px;
}
.pill-blue  { background: rgba(59,130,246,0.15); color: #93c5fd; }
.pill-gold  { background: var(--gold-dim); color: var(--gold); }
.pill-teal  { background: var(--teal-dim); color: var(--teal); }
.pill-red   { background: var(--red-dim);  color: var(--red);  }
.pill-green { background: var(--green-dim); color: var(--green); }

/* Progress stat card */
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 22px 24px;
    text-align: center;
}
.stat-card .stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--gold);
    line-height: 1;
}
.stat-card .stat-label {
    font-size: 0.8rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 6px;
}

/* Home feature cards */
.feature-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 28px 24px;
    text-align: center;
    transition: all 0.25s ease;
    height: 100%;
}
.feature-card:hover {
    border-color: rgba(232,184,75,0.35);
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
}
.feature-icon {
    font-size: 2.2rem;
    margin-bottom: 14px;
}
.feature-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: var(--text-primary);
    margin-bottom: 8px;
}
.feature-desc {
    font-size: 0.87rem;
    color: var(--text-secondary);
    line-height: 1.55;
}

/* SHARP letter highlight (home) */
.sharp-letters {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    display: flex;
    justify-content: center;
    gap: 4px;
    margin: 24px 0;
}
.sharp-letters span {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 52px;
    height: 52px;
    border-radius: 10px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    transition: all 0.2s;
    color: var(--gold);
}

/* Page header */
.page-header {
    margin-bottom: 32px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
}
.page-header h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2rem !important;
    letter-spacing: -0.02em !important;
    color: var(--text-primary) !important;
    margin: 0 0 4px 0 !important;
}
.page-header .subtitle {
    color: var(--text-muted);
    font-size: 0.88rem;
}

/* Lesson block */
.lesson-block {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 22px 26px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}
.lesson-block:hover { border-color: var(--border-bright); }
</style>
"""


def inject_theme():
    """Call this at the top of every page to inject the global theme."""
    import streamlit as st
    st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    """Render a consistent page header."""
    import streamlit as st
    subtitle_html = f'<div class="subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="page-header">
            <h1>{icon} {title}</h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_label(text: str):
    """Render a section divider label."""
    import streamlit as st
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)
