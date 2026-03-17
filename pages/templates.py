
import json
import streamlit as st

st.set_page_config(page_title="Prompt Templates", page_icon="📁", layout="wide")

st.title("📁 Prompt Templates")
st.caption("Prompt Engineering Lab · Reusable starter prompts")

with open("data/templates.json", "r", encoding="utf-8") as f:
    templates = json.load(f)

categories = sorted(set(item["category"] for item in templates))
selected_category = st.selectbox("Filter by category", ["All"] + categories)

filtered = templates if selected_category == "All" else [t for t in templates if t["category"] == selected_category]

for item in filtered:
    with st.expander(f"{item['title']} · {item['category']}"):
        st.write(item["description"])
        st.code(item["template"], language=None)
