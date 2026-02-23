import streamlit as st
import plotly.graph_objects as go
import json
import os
import re

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="GenerAI Influence Sentinel",
    page_icon="🧠",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align: center; color: #00BFFF;'>🧠 GenerAI Influence Sentinel</h1>",
    unsafe_allow_html=True
)
st.caption("Real-Time Psychological Manipulation Detection System")

st.markdown("---")

# ---------------------------------------------------
# KEYWORDS
# ---------------------------------------------------

fear_words = ["regret", "danger", "loss", "fear", "risk", "lose", "threat"]
urgency_words = ["now", "immediately", "limited", "hurry", "today", "urgent", "last chance"]
negative_words = ["bad", "worst", "collapse", "fail", "blocked", "destroy"]

HISTORY_FILE = "history.json"

# ---------------------------------------------------
# SCORE CALCULATION
# ---------------------------------------------------

def calculate_scores(text):
    text_lower = text.lower()

    detected_fear = [word for word in fear_words if word in text_lower]
    detected_urgency = [word for word in urgency_words if word in text_lower]
    detected_negative = [word for word in negative_words if word in text_lower]

    fear_score = len(detected_fear)
    urgency_score = len(detected_urgency)
    sentiment_score = len(detected_negative)

    total_score = (fear_score * 2) + (urgency_score * 1.5) + (sentiment_score * 1.5)

    return fear_score, urgency_score, sentiment_score, total_score, detected_fear, detected_urgency

# ---------------------------------------------------
# INFLUENCE DNA
# ---------------------------------------------------

def calculate_influence_dna(fear, urgency, sentiment):
    dna_score = (fear * 2) + (urgency * 1.5) + (sentiment * 1.5)

    if dna_score >= 8:
        level = "CRITICAL"
    elif dna_score >= 5:
        level = "HIGH"
    elif dna_score >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"

    confidence = min(int((dna_score / 10) * 100), 100)

    return dna_score, level, confidence

# ---------------------------------------------------
# NEUTRAL REWRITE (GenAI Concept)
# ---------------------------------------------------

def generate_neutral_version(text):
    return re.sub(
        r"\b(urgent|immediately|act now|last chance|hurry|before it's too late)\b",
        "consider calmly",
        text,
        flags=re.IGNORECASE
    )

# ---------------------------------------------------
# HISTORY
# ---------------------------------------------------

def save_history(score):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(score)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def calculate_drift():
    history = load_history()
    if len(history) < 2:
        return 0
    recent = history[-5:]
    return max(recent) - min(recent)

# ---------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------

st.write("## 📩 Input Content")

input_mode = st.radio("Choose Input Type:", ["Text", "Image", "Audio"])

text_input = ""

if input_mode == "Text":
    text_input = st.text_area("Enter text to analyze")

elif input_mode == "Image":
    image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if image:
        st.image(image, caption="Uploaded Image")
        text_input = "Image content analysis simulated"

elif input_mode == "Audio":
    audio = st.file_uploader("Upload audio file", type=["wav", "mp3"])
    if audio:
        st.audio(audio)
        text_input = "Audio transcription simulated"

threshold = st.slider("Set Manipulation Alert Threshold", 0, 15, 5)

# ---------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------

if st.button("🔍 Analyze"):

    if text_input.strip() == "":
        st.warning("Please provide input first.")
        st.stop()

    with st.spinner("Analyzing psychological influence patterns..."):

        fear, urgency, sentiment_val, total, detected_fear, detected_urgency = calculate_scores(text_input)
        dna_score, dna_level, confidence = calculate_influence_dna(fear, urgency, sentiment_val)
        save_history(total)

    st.markdown("---")
    st.write("## 🔎 Analysis Results")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fear Score", fear)
    col2.metric("Urgency Score", urgency)
    col3.metric("Negative Tone", sentiment_val)
    col4.metric("Total Score", total)

    st.metric("🧬 Influence DNA Score", dna_score)
    st.metric("📊 Confidence Level", f"{confidence}%")
    st.write(f"### Risk Level: {dna_level}")

    if dna_level == "CRITICAL":
        st.error("🚨 CRITICAL Psychological Manipulation Detected")
    elif dna_level == "HIGH":
        st.warning("⚠️ High Manipulation Risk")
    elif dna_level == "MEDIUM":
        st.info("Moderate Influence Risk")
    else:
        st.success("Low Influence Risk")

    st.write("### 🔥 Influence Intensity")
    st.progress(min(int(total), 15) / 15)

    st.write("### ✏️ Suggested Neutral Rewrite")
    st.info(generate_neutral_version(text_input))

# ---------------------------------------------------
# DRIFT SECTION
# ---------------------------------------------------

st.write("## 📊 Psychological Drift Over Time")

history = load_history()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=list(range(1, len(history) + 1)),
    y=history,
    mode='lines+markers',
    name="Manipulation Score"
))

fig.update_layout(xaxis_title="Analysis Number", yaxis_title="Manipulation Score")

st.plotly_chart(fig, use_container_width=True)

drift = calculate_drift()
st.metric("Psychological Drift Score", drift)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")
st.caption("GenerAI Influence Sentinel | Ethical AI Detection Framework | Hackathon Edition")
