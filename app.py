"""
SHARP Prompt Evaluator
Built on the SHARP Framework by Loveleen Gaur
Powered by Groq
"""

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
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp { font-family: 'Space Grotesk', sans-serif; }

    .hero-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border: 1px solid #FF6B35;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(255,107,53,0.08) 0%, transparent 50%);
        pointer-events: none;
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.8rem; font-weight: 700;
        background: linear-gradient(135deg, #FF6B35, #FFB347);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem; letter-spacing: -1px;
    }
    .hero-subtitle { color: #8892a4; font-size: 1.1rem; margin-bottom: 1rem; }
    .hero-author { color: #FFB347; font-size: 0.95rem; font-weight: 500; }

    .sharp-bar {
        display: flex; justify-content: center; gap: 0.5rem;
        margin: 1.2rem 0 0.5rem; flex-wrap: wrap;
    }
    .sharp-letter {
        background: rgba(255,107,53,0.12);
        border: 1px solid rgba(255,107,53,0.3);
        border-radius: 10px; padding: 0.5rem 1rem;
        text-align: center; min-width: 140px;
    }
    .sharp-letter-char { font-size: 1.5rem; font-weight: 700; color: #FF6B35; }
    .sharp-letter-word { font-size: 0.75rem; color: #8892a4; margin-top: 2px; }

    .score-container {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 16px; padding: 2rem; text-align: center;
        border: 1px solid #2a2a4a; margin: 1rem 0;
    }
    .score-big {
        font-size: 4rem; font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .score-label { font-size: 1.3rem; font-weight: 600; margin-top: 0.5rem; }

    .rating-blunt { color: #ff4444; }
    .rating-getting { color: #ffaa00; }
    .rating-sharp { color: #44bb44; }
    .rating-razor { color: #00ffaa; }

    .dim-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid #2a2a4a;
        border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.8rem;
    }
    .dim-header {
        display: flex; justify-content: space-between;
        align-items: center; margin-bottom: 0.4rem;
    }
    .dim-name { font-weight: 600; font-size: 1rem; color: #FFB347; }
    .dim-score {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700; font-size: 1.1rem;
        padding: 2px 10px; border-radius: 6px;
    }
    .dim-score-0 { background: rgba(255,68,68,0.2); color: #ff4444; }
    .dim-score-1 { background: rgba(255,170,0,0.2); color: #ffaa00; }
    .dim-score-2 { background: rgba(68,187,68,0.2); color: #44bb44; }
    .dim-explanation { color: #8892a4; font-size: 0.9rem; line-height: 1.5; }

    .improved-box {
        background: linear-gradient(135deg, rgba(0,255,170,0.05), rgba(68,187,68,0.05));
        border: 1px solid rgba(0,255,170,0.3);
        border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
        font-size: 0.95rem; line-height: 1.6; color: #e0e0e0;
    }

    .sidebar-info {
        background: rgba(255,107,53,0.08);
        border: 1px solid rgba(255,107,53,0.2);
        border-radius: 10px; padding: 1rem; margin-bottom: 1rem;
        font-size: 0.85rem; color: #b0b8c8; line-height: 1.6;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stTextArea textarea {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.95rem !important;
        border-color: #2a2a4a !important;
        background-color: #0E1117 !important;
    }
    .stTextArea textarea:focus {
        border-color: #FF6B35 !important;
        box-shadow: 0 0 0 1px #FF6B35 !important;
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
        st.success("Groq API key loaded securely from app secrets.")

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
        <strong>💡 How it works:</strong><br><br>
        1. Paste your prompt<br>
        2. Select the task type<br>
        3. Click Evaluate<br>
        4. Get your SHARP score + improved prompt<br><br>
        <strong>Scoring:</strong><br>
        🔴 0-3: Blunt<br>
        🟡 4-6: Getting There<br>
        🟢 7-8: Sharp<br>
        ⚡ 9-10: Razor Sharp
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#666; font-size:0.8rem;">
        Built on the <strong style="color:#FF6B35;">SHARP Framework</strong><br>
        by <strong style="color:#FFB347;">Loveleen Gaur</strong><br><br>
        <span style="color:#444;">Powered by Groq</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# HERO HEADER
# ============================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🔪 SHARP Prompt Evaluator</div>
    <div class="hero-subtitle">Evaluate, Score & Improve Your AI Prompts Instantly</div>
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
user_prompt = st.text_area(
    "📝 Paste your prompt here:",
    height=180,
    placeholder="Example: Write something about AI...\n\nPaste the prompt you want evaluated and click 'Evaluate My Prompt' below."
)

col1, col2, col3 = st.columns([1, 2, 1])
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
                        <div class="score-label {rating_class}">{emoji} {rating_text}</div>
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
                                        <span class="dim-name">{dim_key}</span>
                                        <span class="dim-score dim-score-{d_score}">{d_score}/2</span>
                                    </div>
                                    <div class="dim-explanation">{d_explain}</div>
                                </div>
                                """, unsafe_allow_html=True)

                    elif "WHAT'S MISSING" in section:
                        st.markdown("### 🔍 What's Missing")
                        content = section.replace("WHAT'S MISSING", "").strip()
                        st.markdown(content)

                    elif "IMPROVED SHARP PROMPT" in section:
                        st.markdown("### ✨ Improved SHARP Prompt")
                        content = section.replace("IMPROVED SHARP PROMPT", "").strip()
                        st.markdown(f"""
                        <div class="improved-box">{content}</div>
                        """, unsafe_allow_html=True)
                        st.code(content, language=None)

                    elif "3 TIPS TO REMEMBER" in section:
                        st.markdown("### 💡 3 Tips to Remember")
                        content = section.replace("3 TIPS TO REMEMBER", "").strip()
                        st.markdown(content)

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
