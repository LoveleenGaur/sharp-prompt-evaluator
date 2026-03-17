import streamlit as st

def show():
    st.title("📚 Learn Prompt Engineering")

    st.markdown("""
    Prompt engineering is the art of designing instructions that guide AI to produce accurate, structured, and useful outputs.
    """)

    st.markdown("---")

    st.header("🔹 The SHARP Framework")

    st.markdown("""
    - **S — Situation** → Context  
    - **H — Hat** → Role  
    - **A — Ask** → Task  
    - **R — Rules** → Constraints  
    - **P — Product** → Output format  
    """)

    st.markdown("---")

    st.header("❌ Weak vs ✅ Strong Prompt")

    st.markdown("""
    **Weak Prompt:**
    > Write about marketing.

    **Strong Prompt:**
    > You are a marketing strategist. Write a 300-word explanation of digital marketing strategies for startups. Include 3 examples and present output in bullet points.
    """)

    st.markdown("---")

    st.header("📊 Real Examples (Management Domains)")

    examples = [
        ("Marketing", "Write a product launch plan", 
         "You are a marketing strategist. Create a product launch plan for a skincare brand targeting Gen Z. Include channels, budget allocation, and timeline."),

        ("HR", "Write HR policy", 
         "You are an HR manager. Create a remote work policy for a tech company. Include eligibility, expectations, and compliance rules."),

        ("Finance", "Explain budgeting", 
         "You are a finance expert. Explain zero-based budgeting with a real-world example and pros/cons."),

        ("Operations", "Improve supply chain", 
         "You are an operations consultant. Suggest 5 ways to optimize supply chain efficiency for a manufacturing firm."),

        ("Strategy", "Business strategy", 
         "You are a business strategist. Create a growth strategy for a SaaS startup entering the US market."),

        ("Leadership", "Leadership advice", 
         "You are a leadership coach. Provide 5 actionable strategies to improve team motivation."),

        ("Analytics", "Analyze data", 
         "You are a data analyst. Analyze customer churn factors and suggest actionable insights."),

        ("Entrepreneurship", "Startup idea", 
         "You are a startup mentor. Evaluate a fintech idea for scalability and risks."),

        ("Project Management", "Project plan", 
         "You are a project manager. Create a project plan with milestones and risk mitigation."),

        ("Communication", "Write email", 
         "You are a business communication expert. Write a professional email for client onboarding."),

        ("Sales", "Sales pitch", 
         "You are a sales expert. Write a persuasive pitch for B2B SaaS product."),

        ("Customer Experience", "Improve CX", 
         "You are a CX strategist. Suggest improvements for customer retention."),

        ("Risk Management", "Risk analysis", 
         "You are a risk analyst. Identify risks in digital transformation projects."),

        ("Consulting", "Consulting advice", 
         "You are a consultant. Provide recommendations to improve operational efficiency."),

        ("Innovation", "Innovation strategy", 
         "You are an innovation strategist. Suggest disruptive ideas for retail industry.")
    ]

    for domain, weak, strong in examples:
        with st.expander(f"📌 {domain} Example"):
            st.markdown(f"**Weak Prompt:** {weak}")
            st.markdown(f"**Improved Prompt:** {strong}")

    st.markdown("---")

    st.success("Next → Go to Evaluate Prompt to test your prompts.")
