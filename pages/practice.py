import json
import streamlit as st

def show():
    st.title("🧪 Practice Lab")
    st.caption("Practice writing prompts across real management and business scenarios.")

    with open("data/practice_tasks.json", "r", encoding="utf-8") as f:
        tasks = json.load(f)

    task_titles = [task["title"] for task in tasks]
    selected_title = st.selectbox("Choose a practice task", task_titles)
    task = next(t for t in tasks if t["title"] == selected_title)

    st.subheader("Task")
    st.write(task["task"])

    st.subheader("What success looks like")
    for item in task["success_criteria"]:
        st.write(f"- {item}")

    student_prompt = st.text_area("Write your prompt draft here", height=180)

    if st.button("Save practice attempt"):
        if student_prompt.strip():
            attempts = st.session_state.get("practice_attempts", [])
            attempts.append({
                "task": selected_title,
                "prompt": student_prompt,
            })
            st.session_state["practice_attempts"] = attempts
            st.success("Practice attempt saved. Now open Evaluate Prompt to score it.")
        else:
            st.warning("Please write a prompt first.")
