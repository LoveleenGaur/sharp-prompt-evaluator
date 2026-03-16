
"""
SHARP Prompt Evaluator
Responsive polished UI with full SHARP breakdown
Built on the SHARP Framework by Loveleen Gaur
Powered by Groq
"""

import html
import re
import streamlit as st
from groq import Groq
from sharp_engine import SHARP_SYSTEM_PROMPT, build_evaluation_message


# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="SHARP Prompt Evaluator",
    page_icon="🔪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

api_key = st.secrets.get("GROQ_API_KEY", "")


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def get_groq_client(key: str) -> Groq:
    return Groq(api_key=key)


def evaluate_with_groq(client: Groq, user_prompt: str, task_type: str) -> str:
    user_message = build_evaluation_message(user_prompt, task_type)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SHARP_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    content = completion.choices[0].message.content
    if not content:
        raise ValueError("Groq returned an empty response.")
    return content


def show_api_error(exc: Exception) -> None:
    lowered = str(exc).lower()
    if "rate limit" in lowered or "429" in lowered:
        st.error("Groq rate limit reached. Please wait a minute and try again.")
    elif "authentication" in lowered or "api key" in lowered or "401" in lowered:
        st.error("The Groq API key appears invalid. Please check your Streamlit secrets.")
    else:
        st.error(f"Something went wrong: {exc}")


def safe_html(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")


def extract_section(full_text: str, title: str) -> str:
    pattern = rf"###\s*{re.escape(title)}\s*(.*?)(?=\n###|\Z)"
    match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def extract_score_block(text: str):
    match = re.search(r"SHARP SCORE:\s*(\d+)\s*/\s*10\s*-\s*(.+)", text, re.IGNORECASE)
    if not match:
        return None, None
    return int(match.group(1)), match.group(2).strip()


def score_style(score: int):
    if score <= 3:
        return "🔴", "BLUNT", "#EF4444"
    if score <= 6:
        return "🟡", "GETTING THERE", "#F59E0B"
    if score <= 8:
        return "🟢", "SHARP", "#22C55E"
    return "⚡", "RAZOR SHARP", "#06B6D4"


def extract_dimension_explanation(section_text: str, dim_key: str) -> tuple[int | None, str]:
    pattern = rf"\*\*{re.escape(dim_key)}:\s*\[?(\d)\]?\*\*\s*(.*?)(?=\n\*\*[SHARP]|\Z)"
    match = re.search(pattern, section_text, re.DOTALL)
    if not match:
        return None, ""
    return int(match.group(1)), match.group(2).strip()


# ------------------------------------------------------------
# STYLES
# ------------------------------------------------------------
st.markdown("""
<style>
:root {
    --bg: #081225;
    --bg-soft: #0d1730;
    --surface: #111c36;
    --surface-2: #162445;
    --border: #243556;
    --text: #f8fafc;
    --muted: #9fb0c9;
    --accent: #ff7a1a;
    --accent-2: #ff9b4a;
    --green: #22c55e;
    --yellow: #f59e0b;
    --red: #ef4444;
    --cyan: #06b6d4;
}

html, body, [class*="css"] {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(255,122,26,0.08), transparent 28%),
        linear-gradient(180deg, #061022 0%, #081225 100%);
    color: var(--text);
}

[data-testid="stSidebar"] {
    display: none;
}

#MainMenu, header, footer {
    visibility: hidden;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1180px;
}

.hero {
    background: linear-gradient(135deg, #0f1a33 0%, #16284d 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 38px 28px;
    text-align: center;
    margin-bottom: 28px;
    box-shadow: 0 14px 40px rgba(0,0,0,0.20);
}

.hero h1 {
    margin: 0;
    font-size: 3rem;
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text);
}

.hero-sub {
    margin: 14px auto 0 auto;
    color: var(--muted);
    font-size: 1.08rem;
    max-width: 760px;
}

.hero-pill {
    margin-top: 16px;
    display: inline-block;
    padding: 9px 16px;
    border-radius: 999px;
    background: rgba(255,122,26,0.10);
    border: 1px solid rgba(255,122,26,0.22);
    color: #ffd5b1;
    font-size: 0.96rem;
    font-weight: 600;
}

.sharp-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(110px, 1fr));
    gap: 12px;
    margin-top: 24px;
}

.sharp-box {
    background: rgba(8,18,37,0.45);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 16px 10px;
    text-align: center;
}

.sharp-letter {
    color: var(--accent);
    font-size: 1.9rem;
    font-weight: 800;
    line-height: 1;
}

.sharp-word {
    color: var(--text);
    font-size: 0.98rem;
    font-weight: 600;
    margin-top: 8px;
}

.panel {
    background: linear-gradient(180deg, rgba(17,28,54,0.92), rgba(13,23,48,0.96));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 22px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.16);
}

.section-title {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0 0 8px 0;
    color: var(--text);
}

.section-sub {
    color: var(--muted);
    margin-bottom: 16px;
    font-size: 1rem;
}

.setup-grid {
    display: grid;
    grid-template-columns: 1.15fr 0.85fr;
    gap: 16px;
    align-items: start;
}

.info-card {
    background: rgba(8,18,37,0.55);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 16px;
}

.info-card h4 {
    margin: 0 0 10px 0;
    font-size: 1.06rem;
    color: var(--text);
}

.info-card ul {
    margin: 0;
    padding-left: 1.1rem;
    color: var(--muted);
    line-height: 1.7;
}

.score-legend {
    display: grid;
    grid-template-columns: 1fr;
    gap: 10px;
}

.legend-pill {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.07);
    background: rgba(255,255,255,0.02);
    color: var(--text);
    font-size: 0.95rem;
}

.stSelectbox label, .stTextArea label {
    color: var(--text) !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
}

.stSelectbox > div > div,
.stTextArea textarea {
    background: #0c1731 !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}

.stTextArea textarea {
    min-height: 190px !important;
    font-size: 1rem !important;
    line-height: 1.5 !important;
}

.stTextArea textarea::placeholder {
    color: #7c8fad !important;
}

.stButton > button {
    width: 100%;
    border-radius: 14px !important;
    padding: 0.92rem 1.2rem !important;
    font-size: 1.03rem !important;
    font-weight: 800 !important;
    border: none !important;
    color: white !important;
    background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
    box-shadow: 0 10px 28px rgba(255,122,26,0.20);
}

.stButton > button:hover {
    filter: brightness(1.05);
}

.result-shell {
    background: linear-gradient(180deg, rgba(17,28,54,0.95), rgba(13,23,48,0.98));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 24px;
    margin-top: 22px;
    box-shadow: 0 12px 32px rgba(0,0,0,0.18);
}

.score-card {
    background: linear-gradient(135deg, #101c36, #16284d);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    margin-bottom: 18px;
}

.score-number {
    font-size: 4rem;
    font-weight: 900;
    line-height: 1;
    margin: 0;
}

.score-badge {
    display: inline-block;
    margin-top: 12px;
    padding: 9px 16px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 1rem;
    background: rgba(255,255,255,0.06);
}

.subsection-title {
    margin: 10px 0 12px 0;
    font-size: 1.65rem;
    font-weight: 800;
    color: var(--text);
}

.dim-card {
    background: rgba(8,18,37,0.54);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
}

.dim-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}

.dim-name {
    color: #ffd5b1;
    font-size: 1rem;
    font-weight: 800;
}

.dim-score {
    border-radius: 999px;
    padding: 6px 12px;
    font-size: 0.93rem;
    font-weight: 800;
    min-width: 54px;
    text-align: center;
}

.dim-score-0 { background: rgba(239,68,68,0.12); color: var(--red); }
.dim-score-1 { background: rgba(245,158,11,0.12); color: var(--yellow); }
.dim-score-2 { background: rgba(34,197,94,0.12); color: var(--green); }

.dim-explanation, .plain-text {
    color: var(--muted);
    line-height: 1.7;
    font-size: 0.98rem;
}

.improved-box {
    background: rgba(12,23,49,0.92);
    border: 1px solid rgba(34,197,94,0.55);
    border-radius: 16px;
    padding: 18px;
    color: var(--text);
    line-height: 1.75;
    font-size: 1rem;
    white-space: pre-wrap;
}

.tip-card {
    background: rgba(8,18,37,0.55);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 16px;
    color: var(--muted);
    line-height: 1.7;
}

.framework-box {
    background: rgba(8,18,37,0.55);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 18px;
}

.framework-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

.framework-table th,
.framework-table td {
    border-bottom: 1px solid rgba(255,255,255,0.07);
    padding: 12px 10px;
    text-align: left;
    vertical-align: top;
}

.framework-table th {
    color: #ffd5b1;
    font-size: 0.95rem;
}

.framework-table td {
    color: var(--muted);
    font-size: 0.96rem;
    line-height: 1.6;
}

.divider-space {
    height: 8px;
}

@media (max-width: 900px) {
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .hero {
        padding: 24px 16px;
        border-radius: 18px;
    }
    .hero h1 {
        font-size: 2.2rem;
    }
    .hero-sub {
        font-size: 0.98rem;
    }
    .sharp-grid {
        grid-template-columns: repeat(2, minmax(100px, 1fr));
    }
    .setup-grid {
        grid-template-columns: 1fr;
    }
    .panel, .result-shell {
        padding: 18px;
        border-radius: 18px;
    }
    .section-title {
        font-size: 1.8rem;
    }
    .score-number {
        font-size: 3rem;
    }
    .subsection-title {
        font-size: 1.38rem;
    }
}

@media (max-width: 520px) {
    .hero h1 {
        font-size: 1.8rem;
    }
    .sharp-grid {
        grid-template-columns: repeat(2, minmax(90px, 1fr));
        gap: 10px;
    }
    .sharp-box {
        padding: 14px 8px;
        border-radius: 14px;
    }
    .sharp-letter {
        font-size: 1.5rem;
    }
    .sharp-word {
        font-size: 0.92rem;
    }
    .score-number {
        font-size: 2.6rem;
    }
    .hero-pill {
        font-size: 0.88rem;
    }
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>🔪 SHARP Prompt Evaluator</h1>
    <div class="hero-sub">
        Evaluate, score, and improve your AI prompts using the SHARP framework with a cleaner, sharper interface.
    </div>
    <div class="hero-pill">Built on the SHARP Framework by Loveleen Gaur</div>
    <div class="sharp-grid">
        <div class="sharp-box"><div class="sharp-letter">S</div><div class="sharp-word">Situation</div></div>
        <div class="sharp-box"><div class="sharp-letter">H</div><div class="sharp-word">Hat</div></div>
        <div class="sharp-box"><div class="sharp-letter">A</div><div class="sharp-word">Ask</div></div>
        <div class="sharp-box"><div class="sharp-letter">R</div><div class="sharp-word">Rules</div></div>
        <div class="sharp-box"><div class="sharp-letter">P</div><div class="sharp-word">Product</div></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# SETUP
# ------------------------------------------------------------
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Evaluate your prompt</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Paste a draft below. The evaluator will score it across all five SHARP dimensions and rewrite it into a stronger prompt.</div>',
    unsafe_allow_html=True
)

task_type = st.selectbox(
    "Prompt type",
    [
        "General",
        "Writing / Content",
        "Coding / Technical",
        "Marketing / Business",
        "Research / Academic",
        "Creative / Storytelling",
        "Data Analysis",
        "Email / Communication",
        "Education / Teaching",
        "Other"
    ]
)

user_prompt = st.text_area(
    "📝 Paste your prompt here:",
    height=200,
    placeholder="Example: Explain AI to a beginner..."
)

left, mid, right = st.columns([1, 1.2, 1])
with mid:
    evaluate_btn = st.button("🔪 Evaluate My Prompt")

st.markdown('<div class="divider-space"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="setup-grid">
    <div class="info-card">
        <h4>How it works</h4>
        <ul>
            <li>Paste your prompt</li>
            <li>Select the task type</li>
            <li>Click Evaluate</li>
            <li>Get your SHARP score and improved prompt</li>
        </ul>
    </div>
    <div class="info-card">
        <h4>Scoring</h4>
        <div class="score-legend">
            <div class="legend-pill"><span>🔴 0-3</span><span>Blunt</span></div>
            <div class="legend-pill"><span>🟡 4-6</span><span>Getting There</span></div>
            <div class="legend-pill"><span>🟢 7-8</span><span>Sharp</span></div>
            <div class="legend-pill"><span>⚡ 9-10</span><span>Razor Sharp</span></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------
if evaluate_btn:
    if not user_prompt.strip():
        st.warning("Please paste a prompt to evaluate.")
    elif not api_key:
        st.error("Groq API key was not found in Streamlit secrets.")
    else:
        with st.spinner("Analyzing your prompt with SHARP..."):
            try:
                client = get_groq_client(api_key)
                response_text = evaluate_with_groq(client, user_prompt, task_type)

                score_num, rating_text = extract_score_block(response_text)
                if score_num is None:
                    st.error("The evaluator response did not include a valid SHARP score.")
                else:
                    emoji, label, color = score_style(score_num)
                    dim_section = extract_section(response_text, "DIMENSION BREAKDOWN")
                    missing_section = extract_section(response_text, "WHAT'S MISSING")
                    improved_section = extract_section(response_text, "IMPROVED SHARP PROMPT")
                    tips_section = extract_section(response_text, "3 TIPS TO REMEMBER")

                    st.markdown('<div class="result-shell">', unsafe_allow_html=True)
                    st.markdown(
                        f"""
                        <div class="score-card">
                            <div class="score-number" style="color:{color};">{score_num}/10</div>
                            <div class="score-badge" style="color:{color};">{emoji} {label}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown('<div class="subsection-title">📊 Dimension Breakdown</div>', unsafe_allow_html=True)
                    dims = [
                        "S - Situation",
                        "H - Hat",
                        "A - Ask",
                        "R - Rules",
                        "P - Product",
                    ]
                    for dim_key in dims:
                        d_score, d_explain = extract_dimension_explanation(dim_section, dim_key)
                        if d_score is not None:
                            st.markdown(
                                f"""
                                <div class="dim-card">
                                    <div class="dim-header">
                                        <div class="dim-name">{html.escape(dim_key)}</div>
                                        <div class="dim-score dim-score-{d_score}">{d_score}/2</div>
                                    </div>
                                    <div class="dim-explanation">{safe_html(d_explain)}</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    if missing_section:
                        st.markdown('<div class="subsection-title">🔎 What\'s Missing</div>', unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="plain-text">{safe_html(missing_section)}</div>',
                            unsafe_allow_html=True
                        )

                    if improved_section:
                        st.markdown('<div class="subsection-title">✨ Improved SHARP Prompt</div>', unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="improved-box">{safe_html(improved_section)}</div>',
                            unsafe_allow_html=True
                        )
                        st.code(improved_section, language=None)

                    if tips_section:
                        st.markdown('<div class="subsection-title">💡 3 Tips to Remember</div>', unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="tip-card">{safe_html(tips_section)}</div>',
                            unsafe_allow_html=True
                        )

                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as exc:
                show_api_error(exc)


# ------------------------------------------------------------
# FRAMEWORK DETAILS
# ------------------------------------------------------------
with st.expander("📖 Learn the SHARP Framework"):
    st.markdown("""
    <div class="framework-box">
        <div class="subsection-title" style="margin-top:0;">The SHARP Framework — by Loveleen Gaur</div>
        <div class="plain-text">
            SHARP is a five-dimension framework for writing stronger AI prompts. It helps users move from vague requests to
            structured prompts that produce clearer, more useful, and more reliable results.
        </div>

        <table class="framework-table">
            <thead>
                <tr>
                    <th>Dimension</th>
                    <th>What It Means</th>
                    <th>Question to Ask Yourself</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>S — Situation</strong></td>
                    <td>Context, background, and why the task matters.</td>
                    <td>Did I tell the AI what is happening and why?</td>
                </tr>
                <tr>
                    <td><strong>H — Hat</strong></td>
                    <td>The role, persona, or professional lens the AI should adopt.</td>
                    <td>Did I tell the AI who to become?</td>
                </tr>
                <tr>
                    <td><strong>A — Ask</strong></td>
                    <td>The exact task the AI should perform.</td>
                    <td>Did I clearly state what I want done?</td>
                </tr>
                <tr>
                    <td><strong>R — Rules</strong></td>
                    <td>Constraints, boundaries, exclusions, tone, length, or style.</td>
                    <td>Did I define what to include, avoid, or limit?</td>
                </tr>
                <tr>
                    <td><strong>P — Product</strong></td>
                    <td>The expected output format or final deliverable.</td>
                    <td>Did I define what the output should look like?</td>
                </tr>
            </tbody>
        </table>

        <div class="subsection-title" style="font-size:1.25rem; margin-top:18px;">Scoring Scale</div>
        <div class="plain-text">
            🔴 <strong>0-3: BLUNT</strong> — Needs major rework<br>
            🟡 <strong>4-6: GETTING THERE</strong> — Has potential, but important pieces are missing<br>
            🟢 <strong>7-8: SHARP</strong> — Strong prompt with minor refinements needed<br>
            ⚡ <strong>9-10: RAZOR SHARP</strong> — Excellent prompt, highly structured and ready to use
        </div>

        <div class="subsection-title" style="font-size:1.25rem; margin-top:18px;">Example</div>
        <div class="plain-text">
            <strong>Blunt Prompt (2/10):</strong><br>
            Write about marketing.<br><br>

            <strong>SHARP Prompt (9/10):</strong><br>
            [S] I run a small organic skincare brand in India targeting women aged 25-35. We just launched a new vitamin C serum.<br>
            [H] You are a social media marketing expert specializing in D2C beauty brands.<br>
            [A] Write 5 Instagram captions announcing our new product launch.<br>
            [R] Keep each caption under 150 characters. Use a friendly, aspirational tone. Include 3 relevant hashtags. Avoid clichés.<br>
            [P] Present the output as a numbered list with the caption followed by hashtags.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    "<div style='text-align:center; color:#7d8ea9; font-size:0.92rem; margin-top:18px;'>Built on the SHARP Framework by Loveleen Gaur · Powered by Groq</div>",
    unsafe_allow_html=True
)
