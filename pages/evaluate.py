import html
import re
import streamlit as st
from groq import Groq
from sharp_engine import SHARP_SYSTEM_PROMPT, build_evaluation_message


def show():
    st.markdown("""
    <style>
    .score-card {
        background: linear-gradient(135deg, #112347 0%, #1b315d 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 28px;
        text-align: center;
        margin-bottom: 20px;
    }
    .score-number {
        font-size: 4rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 10px;
    }
    .score-label {
        font-size: 1.15rem;
        font-weight: 700;
    }
    .section-card {
        background: rgba(17, 28, 54, 0.92);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
    }
    .dim-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .dim-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .dim-title {
        font-weight: 700;
        color: #ffbe73;
    }
    .dim-badge {
        padding: 4px 10px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .badge-red {
        background: rgba(239,68,68,0.15);
        color: #ef4444;
    }
    .badge-yellow {
        background: rgba(245,158,11,0.15);
        color: #f59e0b;
    }
    .badge-green {
        background: rgba(34,197,94,0.15);
        color: #22c55e;
    }
    .improved-box {
        background: #0f1a33;
        border: 1px solid rgba(34,197,94,0.45);
        border-radius: 16px;
        padding: 18px;
        color: #f8fafc;
        line-height: 1.75;
        font-size: 1rem;
        white-space: pre-wrap;
    }
    .small-note {
        color: #c9d5e8;
        font-size: 0.96rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("📊 Evaluate Prompt")
    st.caption("Prompt Engineering Lab · Powered by the SHARP Framework developed by Dr. Loveleen Gaur")

    api_key = st.secrets.get("GROQ_API_KEY", "")

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
            "Management / Leadership",
            "Other",
        ],
    )

    user_prompt = st.text_area(
        "Paste your prompt here",
        height=220,
        placeholder="Example: You are a marketing strategist. Write a product launch email for a skincare brand targeting young professionals. Keep it under 200 words and use a warm but professional tone.",
    )

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        evaluate_btn = st.button("🔪 Evaluate with SHARP", use_container_width=True)

    with st.expander("📖 Quick reminder: What SHARP means"):
        st.markdown("""
        - **S — Situation**: Context and background  
        - **H — Hat**: Role or persona for the AI  
        - **A — Ask**: The exact task  
        - **R — Rules**: Constraints, boundaries, tone, or exclusions  
        - **P — Product**: Output format or deliverable  
        """)

    if evaluate_btn:
        if not user_prompt.strip():
            st.warning("Please paste a prompt to evaluate.")
            return

        if not api_key:
            st.error("Groq API key was not found in Streamlit secrets.")
            return

        with st.spinner("Evaluating your prompt with SHARP..."):
            try:
                client = Groq(api_key=api_key)
                user_message = build_evaluation_message(user_prompt, task_type)

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=0.2,
                    messages=[
                        {"role": "system", "content": SHARP_SYSTEM_PROMPT},
                        {"role": "user", "content": user_message},
                    ],
                )

                response_text = completion.choices[0].message.content
                if not response_text:
                    st.error("Empty response returned from Groq.")
                    return

                score_num, rating_text = extract_score(response_text)
                if score_num is None:
                    st.error("Could not extract SHARP score from the model response.")
                    st.code(response_text)
                    return

                emoji, label, color = score_style(score_num)

                st.markdown(
                    f"""
                    <div class="score-card">
                        <div class="score-number" style="color:{color};">{score_num}/10</div>
                        <div class="score-label" style="color:{color};">{emoji} {label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                dim_section = extract_section(response_text, "DIMENSION BREAKDOWN")
                missing_section = extract_section(response_text, "WHAT'S MISSING")
                improved_section = extract_section(response_text, "IMPROVED SHARP PROMPT")
                tips_section = extract_section(response_text, "3 TIPS TO REMEMBER")

                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📊 Dimension Breakdown")

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
                        badge_class = score_badge_class(d_score)
                        st.markdown(
                            f"""
                            <div class="dim-card">
                                <div class="dim-header">
                                    <div class="dim-title">{html.escape(dim_key)}</div>
                                    <div class="dim-badge {badge_class}">{d_score}/2</div>
                                </div>
                                <div>{safe_html(d_explain)}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                st.markdown("</div>", unsafe_allow_html=True)

                if missing_section:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.subheader("🔎 What's Missing")
                    st.markdown(f"<div class='small-note'>{safe_html(missing_section)}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                if improved_section:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.subheader("✨ Improved SHARP Prompt")
                    st.markdown(
                        f"<div class='improved-box'>{safe_html(improved_section)}</div>",
                        unsafe_allow_html=True,
                    )
                    st.code(improved_section, language=None)
                    st.markdown("</div>", unsafe_allow_html=True)

                if tips_section:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.subheader("💡 3 Tips to Remember")
                    st.markdown(f"<div class='small-note'>{safe_html(tips_section)}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            except Exception as exc:
                st.error(f"Something went wrong: {exc}")


def safe_html(text: str) -> str:
    return html.escape(text).replace("\\n", "<br>")


def extract_section(full_text: str, title: str) -> str:
    pattern = rf"###\\s*{re.escape(title)}\\s*(.*?)(?=\\n###|\\Z)"
    match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def extract_score(text: str):
    match = re.search(r"SHARP SCORE:\\s*(\\d+)\\s*/\\s*10\\s*-\\s*(.+)", text, re.IGNORECASE)
    if not match:
        return None, None
    return int(match.group(1)), match.group(2).strip()


def score_style(score: int):
    if score <= 3:
        return "🔴", "BLUNT", "#ef4444"
    if score <= 6:
        return "🟡", "GETTING THERE", "#f59e0b"
    if score <= 8:
        return "🟢", "SHARP", "#22c55e"
    return "⚡", "RAZOR SHARP", "#06b6d4"


def score_badge_class(score: int):
    if score == 0:
        return "badge-red"
    if score == 1:
        return "badge-yellow"
    return "badge-green"


def extract_dimension_explanation(section_text: str, dim_key: str):
    pattern = rf"\\*\\*{re.escape(dim_key)}:\\s*\\[?(\\d)\\]?\\*\\*\\s*(.*?)(?=\\n\\*\\*[SHARP]|\\Z)"
    match = re.search(pattern, section_text, re.DOTALL)
    if not match:
        return None, ""
    return int(match.group(1)), match.group(2).strip()
