
import streamlit as st

st.set_page_config(
    page_title="Prompt Engineering Lab",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #081225 0%, #0b1730 100%);
    color: #f8fafc;
}
[data-testid="stSidebar"] {
    background: #0d1730;
}
.hero {
    background: linear-gradient(135deg, #102040 0%, #16345f 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 32px 28px;
    margin-bottom: 24px;
}
.hero h1 {
    font-size: 2.8rem;
    margin: 0 0 8px 0;
    color: white;
}
.hero p {
    color: #b8c7dc;
    font-size: 1.05rem;
    margin: 0;
}
.card-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(180px, 1fr));
    gap: 16px;
    margin-top: 18px;
}
.feature-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 18px;
}
.feature-card h3 {
    color: #ffb36b;
    margin-bottom: 8px;
}
.section-box {
    background: rgba(17,28,54,0.92);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 20px;
    margin-top: 18px;
}
.footer-note {
    color: #8ea3c2;
    text-align: center;
    font-size: 0.92rem;
    margin-top: 24px;
}
@media (max-width: 900px) {
    .card-grid {
        grid-template-columns: 1fr;
    }
    .hero h1 {
        font-size: 2rem;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🧠 Prompt Engineering Lab</h1>
    <p>Learn, practice, evaluate, and improve AI prompts in one place.</p>
    <p style="margin-top:10px;"><strong>Led by Dr. Loveleen Gaur</strong></p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card-grid">
    <div class="feature-card">
        <h3>📚 Learn</h3>
        <div>Understand core prompt engineering concepts, examples, and frameworks.</div>
    </div>
    <div class="feature-card">
        <h3>🧪 Practice</h3>
        <div>Work on guided prompt tasks across research, business, teaching, and coding.</div>
    </div>
    <div class="feature-card">
        <h3>📊 Evaluate</h3>
        <div>Score prompts using the SHARP Framework developed by Dr. Loveleen Gaur.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-box">
    <h2 style="margin-top:0;">What this platform does</h2>
    <p>
        Prompt Engineering Lab is a structured platform for learning prompt engineering, practicing with real tasks,
        and improving prompts through guided evaluation.
    </p>
    <p>
        The evaluation engine is powered by the <strong>SHARP Framework</strong>, a prompt evaluation methodology
        developed by Dr. Loveleen Gaur.
    </p>
    <p style="margin-bottom:0;">
        Use the left navigation to open the learning module, evaluator, practice lab, templates, and progress dashboard.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.info("Start with **Learn Prompt Engineering** to introduce students to the platform.")
with col2:
    st.success("Then move to **Evaluate Prompt** and **Practice Lab** for hands-on work.")

st.markdown(
    '<div class="footer-note">SHARP Framework is a prompt evaluation methodology developed by Dr. Loveleen Gaur.</div>',
    unsafe_allow_html=True,
)
