import streamlit as st
from transformers import pipeline
import plotly.graph_objects as go
import json
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(page_title="GenerAI Influence Sentinel", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #00BFFF;'>🧠 GenerAI Influence Sentinel</h1>",
    unsafe_allow_html=True
)
st.subheader("Real-Time Psychological Manipulation Detection System")

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

sentiment_model = load_model()

# ---------------------------------------------------
# KEYWORDS
# ---------------------------------------------------

fear_words = ["regret", "danger", "loss", "fear", "risk", "lose", "threat"]
urgency_words = ["now", "immediately", "limited", "hurry", "today", "urgent", "last chance"]

HISTORY_FILE = "history.json"

# ---------------------------------------------------
# SCORE CALCULATION
# ---------------------------------------------------

def calculate_scores(text):
    sentiment = sentiment_model(text)[0]

    detected_fear = [word for word in fear_words if word in text.lower()]
    detected_urgency = [word for word in urgency_words if word in text.lower()]

    fear_score = len(detected_fear)
    urgency_score = len(detected_urgency)
    sentiment_score = 1 if sentiment['label'] == "NEGATIVE" else 0

    total_score = (fear_score * 2) + (urgency_score * 1.5) + (sentiment_score * 2)

    return fear_score, urgency_score, sentiment_score, total_score, detected_fear, detected_urgency

# ---------------------------------------------------
# INFLUENCE DNA
# ---------------------------------------------------

def calculate_influence_dna(fear, urgency, sentiment):
    dna_score = (fear * 2) + (urgency * 1.5) + (sentiment * 2)

    if dna_score >= 8:
        level = "CRITICAL"
    elif dna_score >= 5:
        level = "HIGH"
    elif dna_score >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return dna_score, level

# ---------------------------------------------------
# HISTORY FUNCTIONS
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
# DEMO BUTTONS
# ---------------------------------------------------

st.write("### 🔎 Try Demo Examples")

col_demo1, col_demo2, col_demo3 = st.columns(3)

if col_demo1.button("Political Pressure Example"):
    st.session_state.demo_text = "If you don't act now, the country will collapse and you will regret it."

if col_demo2.button("Scam Urgency Example"):
    st.session_state.demo_text = "Act immediately or your account will be permanently blocked."

if col_demo3.button("Marketing Pressure Example"):
    st.session_state.demo_text = "Limited offer today! Hurry before you lose this opportunity."

default_text = st.session_state.get("demo_text", "")

text_input = st.text_area("Enter text to analyze", value=default_text)

threshold = st.slider("Set Manipulation Alert Threshold", 0, 15, 5)

# ---------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------

if st.button("Analyze"):

    if text_input.strip() == "":
        st.warning("Please enter some text first.")
        st.stop()

    fear, urgency, sentiment_val, total, detected_fear, detected_urgency = calculate_scores(text_input)

    save_history(total)

    dna_score, dna_level = calculate_influence_dna(fear, urgency, sentiment_val)

    # ---------------------------------------------------
    # METRICS
    # ---------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fear Score", fear)
    col2.metric("Urgency Score", urgency)
    col3.metric("Negative Emotion", sentiment_val)
    col4.metric("Total Score", total)

    st.metric("🧬 Influence DNA Score", dna_score)
    st.write(f"### Risk Level: {dna_level}")

    # ---------------------------------------------------
    # RISK COLOR CODING
    # ---------------------------------------------------

    if dna_level == "CRITICAL":
        st.error("🚨 CRITICAL Psychological Manipulation Detected")
    elif dna_level == "HIGH":
        st.warning("⚠️ High Manipulation Risk")
    elif dna_level == "MEDIUM":
        st.info("Moderate Influence Risk")
    else:
        st.success("Low Influence Risk")

    # ---------------------------------------------------
    # HEAT BAR
    # ---------------------------------------------------

    st.write("### 🔥 Influence Intensity")
    st.progress(min(int(total), 15) / 15)

    # ---------------------------------------------------
    # RADAR CHART
    # ---------------------------------------------------

    st.write("### 🧠 Psychological Fingerprint")

    categories = ["Fear", "Urgency", "Negative Emotion"]
    values = [fear, urgency, sentiment_val]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False)

    st.plotly_chart(fig_radar, use_container_width=True)

    # ---------------------------------------------------
    # EXPLAINABILITY
    # ---------------------------------------------------

    st.write("### 🧠 Why Was This Flagged?")

    if detected_fear:
        st.write("⚠️ Fear Triggers Detected:", ", ".join(detected_fear))

    if detected_urgency:
        st.write("⏳ Urgency Triggers Detected:", ", ".join(detected_urgency))

    if sentiment_val:
        st.write("💬 Negative Emotional Tone Detected")

    # ---------------------------------------------------
    # ALERT SYSTEM
    # ---------------------------------------------------

    if total > threshold:
        st.error("🚨 Manipulation Alert Triggered!")
    else:
        st.success("Content within safe limits.")

    # ---------------------------------------------------
    # DOWNLOAD REPORT
    # ---------------------------------------------------

    report = f"""
GenerAI Influence Sentinel Report

Fear Score: {fear}
Urgency Score: {urgency}
Negative Emotion: {sentiment_val}
Total Score: {total}
DNA Score: {dna_score}
Risk Level: {dna_level}
Fear Triggers: {', '.join(detected_fear)}
Urgency Triggers: {', '.join(detected_urgency)}
"""

    st.download_button(
        label="📥 Download Analysis Report",
        data=report,
        file_name="analysis_report.txt"
    )

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

st.plotly_chart(fig,use_container_width="always")

drift = calculate_drift()
st.metric("Psychological Drift Score", drift)

# ---------------------------------------------------
# ARCHITECTURE SECTION
# ---------------------------------------------------

st.write("## 🏗 System Architecture")

st.markdown("""
1. User Input Text  
2. NLP Sentiment Analysis (Transformers)  
3. Psychological Trigger Detection  
4. Influence DNA Scoring Engine  
5. Risk Classification Layer  
6. Visualization & Drift Tracking  
""")
