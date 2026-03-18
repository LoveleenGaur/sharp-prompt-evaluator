import html
import re
import streamlit as st
from groq import Groq
from sharp_engine import SHARP_SYSTEM_PROMPT, build_evaluation_message
from utils.theme import inject_theme, page_header, section_label


# ── Helpers ──────────────────────────────────────────────────────────────────

def safe_html(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")


def extract_section(full_text: str, title: str) -> str:
    pattern = rf"###\s*{re.escape(title)}\s*(.*?)(?=\n###|\Z)"
    match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def extract_score(text: str):
    match = re.search(r"SHARP SCORE:\s*(\d+)\s*/\s*10\s*-\s*(.+)", text, re.IGNORECASE)
    if not match:
        return None, None
    return int(match.group(1)), match.group(2).strip()


def score_color(score: int) -> str:
    if score <= 3:  return "#f87171"
    if score <= 6:  return "#fbbf24"
    if score <= 8:  return "#4ade80"
    return "#2dd4bf"


def score_label(score: int) -> tuple:
    if score <= 3:  return "🔴", "BLUNT"
    if score <= 6:  return "🟡", "GETTING THERE"
    if score <= 8:  return "🟢", "SHARP"
    return "⚡", "RAZOR SHARP"


def badge_class(s: int) -> str:
    return {0: "badge-0", 1: "badge-1", 2: "badge-2"}.get(s, "badge-0")


def extract_dimension(section: str, key: str):
    pattern = rf"\*\*{re.escape(key)}:\s*\[?(\d)\]?\*\*\s*(.*?)(?=\n\*\*[SHARP]|\Z)"
    match = re.search(pattern, section, re.DOTALL)
    if not match:
        return None, ""
    return int(match.group(1)), match.group(2).strip()


def parse_tips(tips_text: str) -> list:
    lines = [l.strip() for l in tips_text.splitlines() if l.strip()]
    tips = []
    for line in lines:
        cleaned = re.sub(r"^\d+[\.\)]\s*", "", line).strip()
        if cleaned:
            tips.append(cleaned)
    return tips[:3]


# ── Main ─────────────────────────────────────────────────────────────────────

def show():
    inject_theme()
    page_header("🔪", "Evaluate Prompt",
                "Score any prompt 0–10 across all 5 SHARP dimensions and get an improved version instantly.")

    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.markdown(
            """
            <div style="background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.25);
                        border-radius:12px;padding:18px 22px;margin-bottom:24px;">
                <strong style="color:#f87171;">⚠ API key not configured</strong><br>
                <span style="color:#94a3b8;font-size:0.88rem;">
                    Add <code>GROQ_API_KEY = "your_key"</code> to your Streamlit secrets to enable evaluation.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Input area ────────────────────────────────────────────────────────────
    col_left, col_right = st.columns([3, 1])
    with col_left:
        default_prompt = st.session_state.pop("selected_prompt", "")
        user_prompt = st.text_area(
            "Paste your prompt here",
            value=default_prompt,
            height=200,
            placeholder=(
                "Example: You are a marketing strategist. Write a product launch email "
                "for a skincare brand targeting young professionals. Keep it under 200 words "
                "and use a warm but professional tone."
            ),
        )
    with col_right:
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
        st.markdown("<br>", unsafe_allow_html=True)
        evaluate_btn = st.button("🔪  Evaluate with SHARP", use_container_width=True)

    with st.expander("📖 SHARP quick reference"):
        dims = [
            ("S", "Situation", "Context & background for the task"),
            ("H", "Hat", "Role or persona for the AI to adopt"),
            ("A", "Ask", "The exact task or action required"),
            ("R", "Rules", "Constraints, tone, exclusions, limits"),
            ("P", "Product", "Expected output format or structure"),
        ]
        for letter, name, desc in dims:
            st.markdown(
                f"""
                <div style="display:flex;gap:12px;align-items:center;padding:8px 4px;
                            border-bottom:1px solid rgba(255,255,255,0.05);">
                    <span style="font-family:'Syne',sans-serif;font-weight:800;color:#e8b84b;
                                 min-width:18px;font-size:1rem;">{letter}</span>
                    <span style="font-weight:600;color:#f1f5f9;min-width:90px;font-size:0.9rem;">{name}</span>
                    <span style="color:#94a3b8;font-size:0.87rem;">{desc}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Evaluation ────────────────────────────────────────────────────────────
    if evaluate_btn:
        if not user_prompt.strip():
            st.warning("Please paste a prompt to evaluate.")
            return
        if not api_key:
            st.error("Groq API key not found. Add it to Streamlit secrets.")
            return

        with st.spinner("Evaluating with SHARP…"):
            try:
                client = Groq(api_key=api_key)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=0.2,
                    messages=[
                        {"role": "system", "content": SHARP_SYSTEM_PROMPT},
                        {"role": "user", "content": build_evaluation_message(user_prompt, task_type)},
                    ],
                )
                response_text = completion.choices[0].message.content
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")
                return

        if not response_text:
            st.error("Empty response from the model.")
            return

        score_num, rating_text = extract_score(response_text)
        if score_num is None:
            st.error("Could not parse SHARP score from the response.")
            with st.expander("Raw model output"):
                st.code(response_text)
            return

        # ── Save to progress ──────────────────────────────────────────────────
        evals = st.session_state.get("eval_history", [])
        evals.append({"score": score_num, "rating": rating_text, "prompt": user_prompt[:120]})
        st.session_state["eval_history"] = evals

        color = score_color(score_num)
        emoji, label = score_label(score_num)
        pct = score_num / 10 * 100

        # ── Score hero card ────────────────────────────────────────────────────
        st.markdown(
            f"""
            <div class="score-hero">
                <div class="score-number" style="color:{color};">{score_num}<span style="font-size:2.5rem;opacity:0.5;">/10</span></div>
                <div class="score-rating" style="color:{color};">{emoji} {label}</div>
                <div class="score-bar-track">
                    <div class="score-bar-fill" style="width:{pct}%;background:{color};"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Dimension breakdown ───────────────────────────────────────────────
        dim_section  = extract_section(response_text, "DIMENSION BREAKDOWN")
        miss_section = extract_section(response_text, "WHAT'S MISSING")
        impr_section = extract_section(response_text, "IMPROVED SHARP PROMPT")
        tips_section = extract_section(response_text, "3 TIPS TO REMEMBER")

        section_label("DIMENSION BREAKDOWN")

        dim_meta = [
            ("S - Situation", "S", "Situation"),
            ("H - Hat",       "H", "Hat"),
            ("A - Ask",       "A", "Ask"),
            ("R - Rules",     "R", "Rules"),
            ("P - Product",   "P", "Product"),
        ]

        for key, letter, name in dim_meta:
            d_score, d_explain = extract_dimension(dim_section, key)
            if d_score is not None:
                bc = badge_class(d_score)
                st.markdown(
                    f"""
                    <div class="dim-row">
                        <div class="dim-letter">{letter}</div>
                        <div class="dim-body">
                            <div class="dim-name">{name}</div>
                            <div class="dim-desc">{safe_html(d_explain)}</div>
                        </div>
                        <div class="dim-badge {bc}">{d_score}/2</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # ── What's missing ────────────────────────────────────────────────────
        if miss_section:
            section_label("WHAT'S MISSING")
            st.markdown(
                f"""
                <div class="sharp-card" style="background:rgba(248,113,113,0.04);
                     border-color:rgba(248,113,113,0.15);">
                    <div style="color:#94a3b8;font-size:0.92rem;line-height:1.7;">
                        {safe_html(miss_section)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ── Improved prompt ───────────────────────────────────────────────────
        if impr_section:
            section_label("IMPROVED SHARP PROMPT")
            st.markdown(
                f'<div class="improved-prompt-box">{safe_html(impr_section)}</div>',
                unsafe_allow_html=True,
            )
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("📋  Copy to clipboard"):
                    st.session_state["clipboard"] = impr_section
                    st.success("Copied to session clipboard.")
            with col2:
                if st.button("🧪  Send to Practice Lab"):
                    st.session_state["selected_prompt"] = impr_section
                    st.info("Improved prompt loaded into Practice Lab — head there to continue.")

        # ── Tips ──────────────────────────────────────────────────────────────
        if tips_section:
            section_label("3 TIPS TO REMEMBER")
            tips = parse_tips(tips_section)
            if not tips:
                # fallback: show raw
                st.markdown(
                    f'<div class="sharp-card"><div style="color:#94a3b8;">{safe_html(tips_section)}</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                for i, tip in enumerate(tips, 1):
                    st.markdown(
                        f"""
                        <div class="tip-item">
                            <div class="tip-num">{i}</div>
                            <div class="tip-text">{safe_html(tip)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
