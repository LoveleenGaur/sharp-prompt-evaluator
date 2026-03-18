import streamlit as st
from utils.theme import inject_theme, page_header, section_label


def show():
    inject_theme()
    page_header("📚", "Learn Prompt Engineering",
                "A structured guide to designing high-quality AI prompts using the SHARP Framework.")

    # ── Nav tabs ────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "What is Prompt Engineering",
        "The SHARP Framework",
        "Weak vs Strong Prompts",
        "Common Mistakes",
        "Practice Exercise",
    ])

    # ── Tab 1 ────────────────────────────────────────────────────────────────
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        section_label("OVERVIEW")
        st.markdown(
            """
            <div class="lesson-block">
                <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.05rem;
                            color:#f1f5f9;margin-bottom:10px;">
                    What is Prompt Engineering?
                </div>
                <p style="color:#94a3b8;line-height:1.7;margin:0;">
                    Prompt engineering is the process of designing inputs that guide AI systems to produce
                    accurate, structured, and useful outputs. A well-crafted prompt reduces ambiguity and
                    gives you precise control over the AI's response — its quality, structure, tone, and relevance.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        section_label("WHY IT MATTERS")
        col1, col2, col3 = st.columns(3)
        benefits = [
            ("🎯", "Precision", "Specify exactly what you need — no more guesswork."),
            ("🏗️", "Structure", "Get outputs in tables, lists, or any format you define."),
            ("⚡", "Efficiency", "Fewer back-and-forths; better first-draft quality."),
        ]
        for col, (icon, title, desc) in zip([col1, col2, col3], benefits):
            with col:
                st.markdown(
                    f"""
                    <div class="sharp-card" style="text-align:center;">
                        <div style="font-size:1.8rem;margin-bottom:10px;">{icon}</div>
                        <div style="font-family:'Syne',sans-serif;font-weight:700;
                                    color:#f1f5f9;margin-bottom:6px;">{title}</div>
                        <div style="font-size:0.87rem;color:#94a3b8;">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        section_label("WHY PROMPTS FAIL")
        failures = [
            ("Too vague", "\"Write about marketing\" — the AI has no idea what you need."),
            ("Missing role", "Without a persona, the AI picks a generic default perspective."),
            ("No output structure", "Responses become long walls of unformatted text."),
            ("No constraints", "Outputs run too long, go off-topic, or miss the point."),
        ]
        for label, detail in failures:
            st.markdown(
                f"""
                <div style="display:flex;gap:14px;align-items:flex-start;
                            background:rgba(248,113,113,0.04);border:1px solid rgba(248,113,113,0.12);
                            border-radius:10px;padding:14px 18px;margin-bottom:10px;">
                    <span style="color:#f87171;font-size:1rem;margin-top:1px;">✕</span>
                    <div>
                        <div style="font-weight:600;color:#f1f5f9;font-size:0.92rem;">{label}</div>
                        <div style="color:#94a3b8;font-size:0.87rem;margin-top:3px;">{detail}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Tab 2 ────────────────────────────────────────────────────────────────
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        section_label("THE FRAMEWORK")
        st.markdown(
            """
            <div style="background:linear-gradient(135deg,rgba(232,184,75,0.06),rgba(232,184,75,0.02));
                        border:1px solid rgba(232,184,75,0.2);border-radius:16px;
                        padding:24px 28px;margin-bottom:28px;">
                <p style="color:#94a3b8;margin:0;line-height:1.7;">
                    The <strong style="color:#e8b84b;">SHARP Framework</strong>, developed by
                    <strong style="color:#f1f5f9;">Dr. Loveleen Gaur</strong>, provides a five-dimension
                    structure for writing prompts that consistently produce high-quality AI outputs.
                    Missing even two dimensions significantly degrades response quality.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        dimensions = [
            ("S", "Situation", "Context & Background",
             "Tells the AI where it is, what is happening, and why this is needed. Without context, the AI makes assumptions that may be completely wrong.",
             "We are launching a new organic skincare serum for women aged 25–35 in urban markets."),
            ("H", "Hat", "Role / Persona",
             "Assigns the AI an expert identity. A well-defined role activates relevant knowledge and calibrates tone, depth, and perspective automatically.",
             "You are a digital marketing strategist with 10 years of brand-building experience."),
            ("A", "Ask", "Clear Task / Action",
             "States exactly what needs to be done. Ambiguous asks produce generic answers. Specific asks produce targeted, actionable outputs.",
             "Create a 2-week product launch campaign plan."),
            ("R", "Rules", "Constraints & Boundaries",
             "Defines what to include, what to exclude, tone, word limits, and style. Rules prevent over-generation and keep the output focused.",
             "Include social media, email, and influencer activities. Keep tone modern. No jargon."),
            ("P", "Product", "Expected Output Format",
             "Specifies what the final output should look like — table, bullet points, memo, numbered list, etc. This is the most commonly forgotten dimension.",
             "Present as a table with columns: Channel | Activity | Objective | Timeline."),
        ]

        for letter, name, subtitle, explanation, example in dimensions:
            st.markdown(
                f"""
                <div class="dim-row" style="margin-bottom:14px;">
                    <div class="dim-letter">{letter}</div>
                    <div class="dim-body">
                        <div class="dim-name">{name}
                            <span style="font-size:0.78rem;color:#4b5563;font-weight:400;margin-left:8px;">{subtitle}</span>
                        </div>
                        <div class="dim-desc" style="margin-bottom:10px;">{explanation}</div>
                        <div style="background:#080f1a;border:1px solid rgba(255,255,255,0.06);
                                    border-radius:8px;padding:10px 14px;
                                    font-family:'JetBrains Mono',monospace;font-size:0.82rem;
                                    color:#c8e6ff;line-height:1.5;">
                            <span style="color:#4b5563;margin-right:8px;">Example →</span>{example}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div style="background:rgba(74,222,128,0.06);border:1px solid rgba(74,222,128,0.2);
                        border-radius:12px;padding:16px 20px;margin-top:8px;">
                <span style="color:#4ade80;font-size:0.9rem;">
                    💡 <strong>Key insight:</strong> A prompt missing 2–3 dimensions will produce generic,
                    unfocused output. All 5 dimensions together unlock consistently excellent results.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Tab 3 ────────────────────────────────────────────────────────────────
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        section_label("SIDE-BY-SIDE COMPARISON")

        examples = [
            ("Marketing", "Write about marketing",
             "You are a digital marketing strategist. [S] A D2C skincare brand is launching on Instagram targeting women aged 22–35. [A] Create a 4-week content strategy. [R] Focus on organic reach, use storytelling, avoid hard selling. Max 300 words. [P] Present as a weekly plan table with: Week | Theme | Content Type | Goal."),
            ("Human Resources", "Write HR policy",
             "You are an HR policy specialist. [S] A 200-person tech company is formalizing remote work after 2 years of informal practice. [A] Draft a remote work policy covering eligibility, attendance, communication norms, and compliance. [R] Keep tone professional. Include headings. Under 500 words. [P] Present as a structured policy document with labeled sections."),
            ("Finance", "Explain budgeting",
             "You are a finance professor teaching MBA students. [S] Students have basic accounting knowledge but no exposure to advanced budgeting. [A] Explain zero-based budgeting with a real company example. [R] Cover definition, advantages, disadvantages. Max 350 words. Avoid excessive jargon. [P] Use four labeled sections: Definition | Advantages | Disadvantages | Example."),
            ("Strategy", "Help with business strategy",
             "You are a business strategy consultant. [S] A SaaS company with $2M ARR wants to expand from North America into Southeast Asia within 18 months. [A] Create a market entry strategy. [R] Address customer segment, go-to-market model, top 3 risks, and 2 competitive threats. [P] Format as a strategic framework with short sections and bullet points. Max 400 words."),
        ]

        for domain, weak, strong in examples:
            with st.expander(f"📌 {domain}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        f"""
                        <div style="background:rgba(248,113,113,0.06);border:1px solid rgba(248,113,113,0.2);
                                    border-radius:12px;padding:16px 18px;height:100%;">
                            <div style="font-size:0.72rem;font-family:'Syne',sans-serif;font-weight:700;
                                        letter-spacing:0.1em;color:#f87171;margin-bottom:10px;">
                                ✕ WEAK PROMPT
                            </div>
                            <div style="color:#94a3b8;font-size:0.9rem;line-height:1.6;">{weak}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col2:
                    st.markdown(
                        f"""
                        <div style="background:rgba(74,222,128,0.05);border:1px solid rgba(74,222,128,0.2);
                                    border-radius:12px;padding:16px 18px;height:100%;">
                            <div style="font-size:0.72rem;font-family:'Syne',sans-serif;font-weight:700;
                                        letter-spacing:0.1em;color:#4ade80;margin-bottom:10px;">
                                ✓ STRONG SHARP PROMPT
                            </div>
                            <div style="color:#c8e6ff;font-size:0.88rem;font-family:'JetBrains Mono',monospace;
                                        line-height:1.6;">{strong}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # ── Tab 4 ────────────────────────────────────────────────────────────────
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        section_label("AVOID THESE MISTAKES")

        mistakes = [
            ("No role assigned",
             "\"Explain AI\" — the AI responds as a generic assistant, not as an expert.",
             "Add: You are a [specific expert role]."),
            ("No output structure",
             "Responses become unstructured walls of text that are hard to use.",
             "Add: Present as [bullet points / table / numbered list / memo]."),
            ("No constraints",
             "Outputs become too long, too broad, or completely off-topic.",
             "Add: Max [X] words. Avoid [Y]. Include only [Z]."),
            ("No context",
             "The AI guesses the scenario, often incorrectly.",
             "Add: A brief situation sentence before your ask."),
            ("Vague ask",
             "\"Help with marketing\" → the AI doesn't know what kind of help you need.",
             "Be specific: \"Create a 4-week Instagram content calendar.\""),
            ("Everything in one sentence",
             "Dense, unpunctuated prompts confuse the model and reduce output quality.",
             "Use SHARP tags like [S], [H], [A], [R], [P] to visually separate dimensions."),
        ]

        for i, (mistake, why, fix) in enumerate(mistakes):
            st.markdown(
                f"""
                <div class="sharp-card-accent" style="margin-bottom:12px;">
                    <div style="font-weight:700;color:#f1f5f9;margin-bottom:6px;font-size:0.95rem;">
                        {i+1}. {mistake}
                    </div>
                    <div style="color:#94a3b8;font-size:0.87rem;margin-bottom:8px;">{why}</div>
                    <div style="color:#4ade80;font-size:0.85rem;">
                        <span style="opacity:0.5;">Fix: </span>{fix}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Tab 5 ────────────────────────────────────────────────────────────────
    with tab5:
        st.markdown("<br>", unsafe_allow_html=True)
        section_label("REWRITE EXERCISE")
        st.markdown(
            """
            <div style="color:#94a3b8;margin-bottom:20px;line-height:1.7;">
                Below is a weak prompt. Rewrite it using all 5 SHARP dimensions.
                When you're done, click <strong style="color:#f1f5f9;">Show model answer</strong> to compare.
            </div>
            """,
            unsafe_allow_html=True,
        )

        weak_prompts = {
            "Write a business email": (
                "Write a business email",
                "[S] A consulting firm has just signed a new corporate client. [H] You are a business communication expert. [A] Write a professional client onboarding email. [R] Keep tone warm yet professional. Mention next steps and expected timeline. Under 200 words. [P] Present as a polished email with a subject line, greeting, body, and sign-off."
            ),
            "Explain machine learning": (
                "Explain machine learning",
                "[S] I am preparing a 10-minute presentation for non-technical executives at a bank. [H] You are a data science educator. [A] Explain machine learning in plain language with 2 real banking examples. [R] Avoid jargon. Keep it under 300 words. Focus on business value, not algorithms. [P] Structure as: Definition (2 sentences) | How it works (3 sentences) | Examples (2 bullet points) | Business benefit (1 sentence)."
            ),
            "Create a marketing plan": (
                "Create a marketing plan",
                "[S] A DTC pet food brand is launching a subscription service for premium dog food targeting millennial pet owners. [H] You are a growth marketing strategist. [A] Create a 90-day marketing plan for the subscription launch. [R] Focus on digital channels. Include budget allocation percentages. Avoid paid TV/radio. [P] Present as a table: Month | Channel | Activity | Goal | Budget %."
            ),
        }

        selected_weak = st.selectbox("Choose a prompt to rewrite:", list(weak_prompts.keys()))
        weak_text, model_answer = weak_prompts[selected_weak]

        st.markdown(
            f"""
            <div style="background:rgba(248,113,113,0.06);border:1px solid rgba(248,113,113,0.18);
                        border-radius:10px;padding:14px 18px;margin-bottom:20px;">
                <div style="font-size:0.72rem;color:#f87171;font-family:'Syne',sans-serif;
                            font-weight:700;letter-spacing:0.1em;margin-bottom:6px;">WEAK PROMPT TO REWRITE</div>
                <div style="color:#94a3b8;font-size:0.95rem;">{weak_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        student_answer = st.text_area(
            "Your SHARP rewrite:",
            height=160,
            placeholder="Include all 5 dimensions: [S] Situation · [H] Hat · [A] Ask · [R] Rules · [P] Product",
            key=f"learn_rewrite_{selected_weak}",
        )

        if st.button("Show model answer", key="show_model_answer"):
            st.markdown(
                f"""
                <div style="background:rgba(74,222,128,0.05);border:1px solid rgba(74,222,128,0.2);
                            border-radius:12px;padding:18px 20px;margin-top:8px;">
                    <div style="font-size:0.72rem;color:#4ade80;font-family:'Syne',sans-serif;
                                font-weight:700;letter-spacing:0.1em;margin-bottom:10px;">MODEL ANSWER</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.87rem;
                                color:#c8e6ff;line-height:1.7;">{model_answer}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div style="margin-top:28px;padding:16px 20px;
                        background:rgba(232,184,75,0.05);border:1px solid rgba(232,184,75,0.15);
                        border-radius:10px;">
                <span style="color:#e8b84b;font-size:0.9rem;">
                    ▶ Next step: Head to the <strong>Practice Lab</strong> to write prompts for real business scenarios,
                    then use <strong>Evaluate Prompt</strong> to get your SHARP score.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
