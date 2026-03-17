import streamlit as st

st.set_page_config(page_title="Progress Dashboard", page_icon="📈", layout="wide")

st.title("📈 Progress Dashboard")
st.caption("Prompt Engineering Lab · Session-based progress")

attempts = st.session_state.get("practice_attempts", [])

if not attempts:
    st.info("No practice attempts saved in this session yet.")
else:
    st.metric("Practice attempts this session", len(attempts))
    st.subheader("Saved attempts")
    for i, item in enumerate(reversed(attempts), start=1):
        with st.expander(f"Attempt {i} · {item['task']}"):
            st.write(item["prompt"])
