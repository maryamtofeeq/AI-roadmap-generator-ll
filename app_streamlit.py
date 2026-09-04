import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Roadmap Generator", page_icon="🗺️", layout="wide")

# Streamlit Cloud: add GROQ_API_KEY in Settings > Secrets.
# Local: set GROQ_API_KEY as an environment variable.
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

if not api_key:
    st.error("GROQ_API_KEY is not configured. Add it to Streamlit Cloud Secrets or set it as an environment variable.")
    st.stop()

client = Groq(api_key=api_key)


def create_prompt(domain, level, learning_time):
    return f"""
You are an expert learning-roadmap designer.

Create a personalized, practical learning roadmap for:

Domain / Field: {domain}
Current skill level: {level}
Available learning time: {learning_time}

Requirements:
1. Start from the user's current skill level.
2. Arrange topics from easier to harder.
3. Divide the roadmap into clear phases.
4. Adapt the amount of content to the available learning time.
5. Include the learning goal.
6. Include prerequisites.
7. Include important topics and subtopics in the correct order.
8. Include practical exercises.
9. Include a project for each major phase where appropriate.
10. Include a realistic timeline.
11. Include milestones/checkpoints.
12. Include a final capstone project.
13. Include recommended next steps after completing the roadmap.
14. Avoid unnecessary topics and information overload.
15. Use clear Markdown headings, bullets, and tables where useful.

Return only the roadmap.
"""


def generate_roadmap(domain, level, learning_time):
    domain = (domain or "").strip()
    level = (level or "").strip()
    learning_time = (learning_time or "").strip()

    if not domain:
        return "⚠️ Please enter a domain or field."
    if not level:
        return "⚠️ Please select your skill level."
    if not learning_time:
        return "⚠️ Please enter your available learning time."

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert educational roadmap generator. Create realistic, structured, practical learning plans.",
                },
                {"role": "user", "content": create_prompt(domain, level, learning_time)},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Something went wrong while generating the roadmap.\n\nError: `{str(e)}`"


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🗺️ AI Roadmap Generator")
st.write("Create a personalized learning roadmap for any domain or skill using AI.")
st.divider()

left, right = st.columns([1, 1.5])

with left:
    st.subheader("📋 Your Learning Details")

    domain = st.text_input(
        "Domain / Field",
        placeholder="e.g. Python, Data Science, Cybersecurity",
    )

    level = st.selectbox(
        "Skill Level",
        ["Beginner", "Intermediate", "Advanced"],
    )

    learning_time = st.text_input(
        "Time Available",
        placeholder="e.g. 3 months, 6 months, 10 hours/week",
    )

    st.caption("Tip: Be specific, e.g. `3 months, 8 hours per week`.")

    generate = st.button("🚀 Generate Roadmap", type="primary", use_container_width=True)

    if st.button("🎯 Use Demo: Python Beginner", use_container_width=True):
        st.session_state["demo_domain"] = "Python"
        st.session_state["demo_level"] = "Beginner"
        st.session_state["demo_time"] = "3 months, 8 hours per week"
        st.rerun()

with right:
    st.subheader("📚 Generated Roadmap")

    if "demo_domain" in st.session_state:
        domain = st.session_state["demo_domain"]
        level = st.session_state["demo_level"]
        learning_time = st.session_state["demo_time"]

    if generate:
        with st.spinner("🤖 Creating your personalized roadmap..."):
            roadmap = generate_roadmap(domain, level, learning_time)

        st.markdown(roadmap)
        st.download_button(
            "⬇️ Download Roadmap",
            data=roadmap,
            file_name="learning_roadmap.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.info("Enter your learning details on the left and click **Generate Roadmap**.")

st.divider()
st.caption("Built with Streamlit + Groq")
