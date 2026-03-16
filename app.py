"""
SHARP Prompt Evaluator
Built on the SHARP Framework by Loveleen Gaur
Powered by Groq
"""

import html
import re
import streamlit as st
from groq import Groq
from sharp_engine import SHARP_SYSTEM_PROMPT, build_evaluation_message


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="SHARP Prompt Evaluator",
    page_icon="🔪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# HELPERS
# ============================================================
def get_groq_client(api_key: str) -> Groq:
    return Groq(api_key=api_key)


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
    error_text = str(exc)
    lowered = error_text.lower()

    if "rate limit" in lowered or "429" in lowered:
        st.error(
            "Groq rate limit reached. Wait a minute and try again, or switch to another Groq key."
        )
    elif "authentication" in lowered or "api key" in lowered or "401" in lowered:
        st.error(
            "Your Groq API key looks invalid. Copy it again from the Groq console and paste it into the sidebar."
        )
    else:
        st.error(f"Something went wrong: {error_text}")


def safe_html(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")


# ============================================================
# LOAD API KEY
# ============================================================
secret_api_key = st.secrets.get("GROQ_API_KEY", "")
api_key = secret_api_key


# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

    :root {
        --bg: #0b1020;
        --sidebar: #0f172a;
        --surface: #121a2b;
        --surface-2: #172033;
        --border: #24324a;
        --text: #f8fafc;
        --muted: #aab4c3;
        --accent: #ff7a1a;
        --accent-hover: #ff933d;
        --accent-soft: rgba(255, 122, 26, 0.10);
        --good: #22c55e;
        --warn: #f59e0b;
        --bad: #ef4444;
        --radius: 16px;
    }

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top left, rgba(255,122,26,0.08), transparent 26%), var(--bg);
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #0c1324 100%);
        border-right: 1px solid rgba(255,255,255,0.04);
    }

    [data-testid="stSidebar"] * {
        color: var(--text);
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .hero-container {
        background: linear-gradient(135deg, #121a2b 0%, #13213f 55%, #10294e 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 2.5rem 2.25rem 2rem;
        margin-bottom: 1.75rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.24);
    }

    .hero-container::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 20% 20%, rgba(255,122,26,0.14), transparent 28%);
        pointer-events: none;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        line-height: 1.05;
        color: #fff7ed;
        margin-bottom: 0.55rem;
        letter-spacing: -1.4px;
    }

    .hero-title .blade {
        color: var(--accent);
        margin-right: 0.4rem;
    }

    .hero-subtitle {
        color: var(--muted);
        font-size: 1.06rem;
        margin-bottom: 0.85rem;
    }

    .hero-author {
        display: inline-block;
        color: #ffd7b0;
        font-size: 0.92rem;
        background: rgba(255,122,26,0.10);
        border: 1px solid rgba(255,122,26,0.18);
        padding: 0.45rem 0.85rem;
        border-radius: 999px;
        margin-bottom: 1rem;
    }

    .sharp-bar {
        display: grid;
        grid-template-columns: repeat(5, minmax(110px, 1fr));
        gap: 0.8rem;
        margin-top: 1rem;
    }

    .sharp-letter {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 0.85rem 0.75rem;
        text-align: center;
        backdrop-filter: blur(8px);
    }

    .sharp-letter-char {
        font-size: 1.55rem;
        font-weight: 700;
        color: var(--accent);
        line-height: 1.1;
    }

    .sharp-letter-word {
        font-size: 0.78rem;
        color: var(--muted);
        margin-top: 0.25rem;
    }

    .section-title {
        color: var(--text);
        font-size: 1.85rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }

    .section-subtitle {
        color: var(--muted);
        margin-bottom: 1.1rem;
        font-size: 0.97rem;
    }

    .sidebar-chip {
        background: rgba(34, 197, 94, 0.10);
        border: 1px solid rgba(34, 197, 94, 0.22);
        color: #b8f5ca;
        border-radius: 12px;
        padding: 0.85rem 0.95rem;
        font-size: 0.92rem;
        margin-bottom: 1rem;
    }

    .sidebar-info {
        background: var(--surface);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1rem 1rem 0.95rem;
        margin-bottom: 1rem;
        color: var(--muted);
        font-size: 0.88rem;
        line-height: 1.75;
    }

    .sidebar-info strong {
        color: var(--text);
    }

    .stTextArea label, .stSelectbox label, .stTextInput label {
        color: var(--text) !important;
        font-weight: 600 !important;
    }

    .stTextArea textarea {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.98rem !important;
        border-radius: 18px !important;
        border: 1px solid var(--border) !important;
        background: #0f172a !important;
        color: #eef2ff !important;
        min-height: 210px !important;
    }

    .stTextArea textarea:focus {
        border-color: rgba(255,122,26,0.65) !important;
        box-shadow: 0 0 0 1px rgba(255,122,26,0.4) !important;
    }

    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background: #0f172a !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 12px !important;
    }

    .stButton button {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%) !important;
        color: white !important;
        border: 0 !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.85rem 1rem !important;
        box-shadow: 0 10px 24px rgba(255,122,26,0.22) !important;
    }

    .stButton button:hover {
        filter: brightness(1.03);
        transform: translateY(-1px);
    }

    .stMarkdown h3 {
        color: var(--text);
        letter-spacing: -0.4px;
    }

    .score-container {
        background: linear-gradient(135deg, #111827 0%, #16213a 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin: 1rem 0 1.5rem;
        box-shadow: 0 18px 45px rgba(0,0,0,0.20);
    }

    .score-big {
        font-size: 4rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1;
    }

    .score-label {
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 0.65rem;
        letter-spacing: 0.2px;
    }

    .rating-blunt { color: var(--bad); }
    .rating-getting { color: var(--warn); }
    .rating-sharp { color: var(--good); }
    .rating-razor { color: #38bdf8; }

    .dim-card {
        background: var(--surface);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1rem 1.15rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.10);
    }

    .dim-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 0.5rem;
    }

    .dim-name {
        font-weight: 700;
        font-size: 1rem;
        color: #ffd7b0;
    }

    .dim-score {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.95rem;
        padding: 0.3rem 0.65rem;
        border-radius: 999px;
        min-width: 60px;
        text-align: center;
    }

    .dim-score-0 { background: rgba(239,68,68,0.12); color: #ff8f8f; }
    .dim-score-1 { background: rgba(245,158,11,0.14); color: #ffd27c; }
    .dim-score-2 { background: rgba(34,197,94,0.14); color: #9ce7b4; }

    .dim-explanation {
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.65;
    }

    .result-card {
        background: var(--surface);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 1.2rem 1.25rem;
        margin: 0.85rem 0 1rem;
        color: var(--muted);
        line-height: 1.7;
    }

    .improved-box {
        background: linear-gradient(135deg, rgba(255,122,26,0.07), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,122,26,0.22);
        border-radius: 18px;
        padding: 1.2rem 1.25rem;
        margin: 0.75rem 0 0.9rem;
        font-size: 0.98rem;
        line-height: 1.75;
        color: #fff5eb;
    }

    .tips-card {
        background: var(--surface);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 1.1rem 1.2rem;
        margin-top: 0.5rem;
        color: var(--muted);
        line-height: 1.75;
    }

    .tips-card ol {
        margin: 0;
        padding-left: 1.1rem;
    }

    .tips-card li {
        margin-bottom: 0.55rem;
    }

    .tips-card strong {
        color: var(--text);
    }

    .stCodeBlock {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }

    .stAlert {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
    }

    .stExpander {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        background: var(--surface) !important;
    }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        background: var(--surface);
        overflow: hidden;
    }

    @media (max-width: 900px) {
        .sharp-bar {
            grid-template-columns: repeat(2, minmax(120px, 1fr));
        }

        .hero-title {
            font-size: 2.3rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ Settings")

    if not secret_api_key:
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Get a key from console.groq.com/keys"
        )
    else:
        st.markdown(
            '<div class="sidebar-chip">Groq API key loaded securely from app secrets.</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    task_type = st.selectbox(
        "What type of prompt is this?",
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

    st.markdown("---")

    st.markdown("""
    <div class="sidebar-info">
        <strong>How it works</strong><br><br>
        1. Paste your prompt<br>
        2. Select the task type<br>
        3. Click Evaluate<br>
        4. Get your SHARP score and an improved prompt<br><br>
        <strong>Scoring</strong><br>
        0-3: Blunt<br>
        4-6: Getting There<br>
        7-8: Sharp<br>
        9-10: Razor Sharp
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#94a3b8; font-size:0.84rem; line-height:1.7;">
        Built on the <strong style="color:#FF7A1A;">SHARP Framework</strong><br>
        by <strong style="color:#FFD7B0;">Loveleen Gaur</strong><br><br>
        <span style="color:#64748b;">Powered by Groq</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# HERO HEADER
# ============================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title"><span class="blade">🔪</span>SHARP Prompt Evaluator</div>
    <div class="hero-subtitle">Evaluate, score, and improve your AI prompts with a sharper visual and analytical experience.</div>
    <div class="hero-author">Built on the SHARP Framework by Loveleen Gaur</div>
    <div class="sharp-bar">
        <div class="sharp-letter">
            <div class="sharp-letter-char">S</div>
            <div class="sharp-letter-word">Situation</div>
        </div>
        <div class="sharp-letter">
            <div class="sharp-letter-char">H</div>
            <div class="sharp-letter-word">Hat</div>
        </div>
        <div class="sharp-letter">
            <div class="sharp-letter-char">A</div>
            <div class="sharp-letter-word">Ask</div>
        </div>
        <div class="sharp-letter">
            <div class="sharp-letter-char">R</div>
            <div class="sharp-letter-word">Rules</div>
        </div>
        <div class="sharp-letter">
            <div class="sharp-letter-char">P</div>
            <div class="sharp-letter-word">Product</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# MAIN INPUT
# ============================================================
st.markdown('<div class="section-title">Evaluate your prompt</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Paste a draft below. The evaluator will score it across all five SHARP dimensions and rewrite it into a stronger prompt.</div>', unsafe_allow_html=True)

user_prompt = st.text_area(
    "📝 Paste your prompt here:",
    height=210,
    placeholder="Example: Explain neuroplasticity for undergraduate psychology students in 250 words using a formal tone and 3 recent examples."
)

col1, col2, col3 = st.columns([1, 1.8, 1])
with col2:
    evaluate_btn = st.button(
        "🔪 Evaluate My Prompt",
        use_container_width=True,
        type="primary"
    )


# ============================================================
# EVALUATION LOGIC
# ============================================================
if evaluate_btn:
    if not api_key:
        st.error("Groq API key not found. Please add it in Streamlit app secrets.")
    elif not user_prompt.strip():
        st.warning("Please paste a prompt to evaluate.")
    else:
        with st.spinner("Analyzing your prompt with SHARP..."):
            try:
                client = get_groq_client(api_key)
                response_text = evaluate_with_groq(client, user_prompt, task_type)

                st.markdown("---")

                score_match = re.search(r'SHARP SCORE:\s*(\d+)/10\s*-\s*(.+)', response_text)

                if score_match:
                    score_num = int(score_match.group(1))
                    rating_text = score_match.group(2).strip()

                    if score_num <= 3:
                        rating_class = "rating-blunt"
                        emoji = "🔴"
                    elif score_num <= 6:
                        rating_class = "rating-getting"
                        emoji = "🟡"
                    elif score_num <= 8:
                        rating_class = "rating-sharp"
                        emoji = "🟢"
                    else:
                        rating_class = "rating-razor"
                        emoji = "⚡"

                    st.markdown(f"""
                    <div class="score-container">
                        <div class="score-big {rating_class}">{score_num}/10</div>
                        <div class="score-label {rating_class}">{emoji} {html.escape(rating_text)}</div>
                    </div>
                    """, unsafe_allow_html=True)

                sections = response_text.split("###")

                for section in sections:
                    section = section.strip()
                    if not section:
                        continue

                    if "DIMENSION BREAKDOWN" in section:
                        st.markdown("### 📊 Dimension Breakdown")
                        dims = {
                            "S - Situation": ("Situation", "Does the AI know the context?"),
                            "H - Hat": ("Hat / Role", "Does the AI know who to be?"),
                            "A - Ask": ("Ask / Task", "Is the task clear and specific?"),
                            "R - Rules": ("Rules", "Are constraints and boundaries set?"),
                            "P - Product": ("Product / Output", "Is the expected format defined?")
                        }

                        for dim_key, (_dim_name, _dim_desc) in dims.items():
                            dim_match = re.search(
                                rf'\*\*{re.escape(dim_key)}:\s*\[?(\d)\]?\*\*\s*(.*?)(?=\*\*[SHARP]|$)',
                                section,
                                re.DOTALL
                            )
                            if dim_match:
                                d_score = int(dim_match.group(1))
                                d_explain = dim_match.group(2).strip()
                                st.markdown(f"""
                                <div class="dim-card">
                                    <div class="dim-header">
                                        <span class="dim-name">{html.escape(dim_key)}</span>
                                        <span class="dim-score dim-score-{d_score}">{d_score}/2</span>
                                    </div>
                                    <div class="dim-explanation">{safe_html(d_explain)}</div>
                                </div>
                                """, unsafe_allow_html=True)

                    elif "WHAT'S MISSING" in section:
                        st.markdown("### 🔍 What's Missing")
                        content = section.replace("WHAT'S MISSING", "").strip()
                        st.markdown(
                            f'<div class="result-card">{safe_html(content)}</div>',
                            unsafe_allow_html=True
                        )

                    elif "IMPROVED SHARP PROMPT" in section:
                        st.markdown("### ✨ Improved SHARP Prompt")
                        content = section.replace("IMPROVED SHARP PROMPT", "").strip()
                        st.markdown(
                            f'<div class="improved-box">{safe_html(content)}</div>',
                            unsafe_allow_html=True
                        )
                        st.code(content, language=None)

                    elif "3 TIPS TO REMEMBER" in section:
                        st.markdown("### 💡 3 Tips to Remember")
                        content = section.replace("3 TIPS TO REMEMBER", "").strip()
                        tips = [line.strip("-• ").strip() for line in content.splitlines() if line.strip()]
                        if tips:
                            tips_html = "".join([f"<li>{safe_html(tip)}</li>" for tip in tips])
                            st.markdown(
                                f'<div class="tips-card"><ol>{tips_html}</ol></div>',
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                f'<div class="tips-card">{safe_html(content)}</div>',
                                unsafe_allow_html=True
                            )

                    elif "SHARP SCORE" in section:
                        pass

            except Exception as exc:
                show_api_error(exc)


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")

with st.expander("📖 Learn the SHARP Framework"):
    st.markdown("""
    ## The SHARP Framework — by Loveleen Gaur

    **SHARP** is a 5-dimension framework for writing effective AI prompts.
    Every great prompt needs all 5 elements:

    | Dimension | What It Means | Question to Ask Yourself |
    |-----------|--------------|------------------------|
    | **S — Situation** | Context & background | *Did I tell the AI what's happening and why?* |
    | **H — Hat** | Role / persona for the AI | *Did I tell the AI who to become?* |
    | **A — Ask** | Clear, specific task | *Did I clearly state what I want done?* |
    | **R — Rules** | Constraints & boundaries | *Did I set limits on what to include/exclude?* |
    | **P — Product** | Expected output format | *Did I define what the output should look like?* |

    ### Scoring Scale
    - **0-3: 🔴 BLUNT** — Needs major rework
    - **4-6: 🟡 GETTING THERE** — Needs sharpening
    - **7-8: 🟢 SHARP** — Good prompt, minor tweaks
    - **9-10: ⚡ RAZOR SHARP** — Excellent prompt!

    ### Example

    **Blunt Prompt (Score: 2/10):**
    > "Write about marketing"

    **SHARP Prompt (Score: 9/10):**
    > **[S]** I run a small organic skincare brand in India targeting women aged 25-35.
    > We just launched a new vitamin C serum.
    > **[H]** You are a social media marketing expert specializing in D2C beauty brands.
    > **[A]** Write 5 Instagram captions announcing our new product launch.
    > **[R]** Keep each caption under 150 characters. Use a friendly, aspirational tone. Include 3 relevant hashtags per caption. Don't use cliches like "game-changer" or "must-have".
    > **[P]** Present in a numbered list with the caption text followed by hashtags.
    """)
