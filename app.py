import streamlit as st
import re

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="GenerAI Influence Sentinel",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------
# Title Section
# -------------------------------
st.title("🧠 GenerAI Influence Sentinel")
st.caption("Real-Time Psychological Manipulation Detection System")

st.markdown("---")

# -------------------------------
# Input Section
# -------------------------------
st.subheader("📩 Enter a Message to Analyze")

user_input = st.text_area(
    "Paste the message below:",
    height=150,
    placeholder="Type or paste suspicious message here..."
)

# -------------------------------
# Detection Logic
# -------------------------------
def calculate_scores(text):
    manipulation_keywords = [
        "urgent", "immediately", "act now", "limited time",
        "exclusive", "don't miss", "only today", "secret",
        "guaranteed", "risk-free", "last chance",
        "you must", "hurry", "before it's too late"
    ]

    drift_keywords = [
        "everyone is doing it",
        "only smart people choose this",
        "prove yourself",
        "be part of elite group"
    ]

    text_lower = text.lower()

    dna_score = sum(keyword in text_lower for keyword in manipulation_keywords)
    drift_score = sum(keyword in text_lower for keyword in drift_keywords)

    total_score = dna_score + drift_score

    if total_score <= 1:
        level = "Low"
    elif total_score <= 3:
        level = "Moderate"
    else:
        level = "High"

    return dna_score, drift_score, level


def generate_neutral_version(text):
    neutral_text = re.sub(
        r"\b(urgent|immediately|act now|limited time|last chance|hurry|before it's too late)\b",
        "consider carefully",
        text,
        flags=re.IGNORECASE
    )
    return neutral_text


# -------------------------------
# Analyze Button
# -------------------------------
if st.button("🔍 Analyze Message"):

    if user_input.strip() == "":
        st.warning("Please enter a message to analyze.")
    else:
        with st.spinner("Analyzing psychological influence patterns..."):

            dna_score, drift_score, dna_level = calculate_scores(user_input)

        st.markdown("---")
        st.subheader("🔎 Analysis Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🧬 Influence DNA Score", dna_score)

        with col2:
            st.metric("⚠️ Risk Level", dna_level)

        with col3:
            st.metric("📊 Psychological Drift", drift_score)

        st.markdown("### 🧠 Interpretation")

        if dna_level == "Low":
            st.success(
                "This message shows minimal psychological manipulation patterns."
            )

        elif dna_level == "Moderate":
            st.warning(
                "This message contains noticeable persuasive or pressure-based elements."
            )

        else:
            st.error(
                "High psychological manipulation detected. Approach with caution."
            )

        st.markdown("### ✏️ Suggested Neutral Rewrite")

        neutral_version = generate_neutral_version(user_input)
        st.info(neutral_version)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("GenerAI Influence Sentinel | Built for Ethical AI Awareness & Hackathon Demo")
