import streamlit as st
from transformers import pipeline
import plotly.graph_objects as go
import json
import os

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(page_title="GenerAI Influence Sentinel", layout="wide")

st.title("🧠 GenerAI Influence Sentinel")
st.subheader("Real-Time Psychological Manipulation Detection System")

# -----------------------------------
# LOAD AI MODEL
# -----------------------------------

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

sentiment_model = load_model()

# -----------------------------------
# KEYWORD LISTS
# -----------------------------------

fear_words = ["regret", "danger", "loss", "fear", "risk", "lose", "threat"]
urgency_words = ["now", "immediately", "limited", "hurry", "today", "urgent", "last chance"]

HISTORY_FILE = "history.json"

# -----------------------------------
# CORE SCORING FUNCTION
# -----------------------------------

def calculate_scores(text):
    sentiment = sentiment_model(text)[0]
    
    fear_score = sum(word in text.lower() for word in fear_words)
    urgency_score = sum(word in text.lower() for word in urgency_words)
    sentiment_score = 1 if sentiment['label'] == "NEGATIVE" else 0
    
    total_score = (fear_score * 2) + (urgency_score * 1.5) + (sentiment_score * 2)
    
    return fear_score, urgency_score, sentiment_score, total_score

# -----------------------------------
# INFLUENCE DNA
# -----------------------------------

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

# -----------------------------------
# MANIPULATION CLASSIFIER
# -----------------------------------

def classify_manipulation(fear, urgency):
    if fear > 0 and urgency > 0:
        return "Fear + Urgency Manipulation"
    elif fear > 0:
        return "Fear-Based Manipulation"
    elif urgency > 0:
        return "Urgency Pressure Manipulation"
    else:
        return "Low Manipulation"

# -----------------------------------
# EXPLANATION ENGINE
# -----------------------------------

def generate_explanation(fear, urgency, sentiment):
    reasons = []

    if fear > 0:
        reasons.append("Fear-based psychological trigger detected.")

    if urgency > 0:
        reasons.append("Urgency pressure language detected.")

    if sentiment > 0:
        reasons.append("Negative emotional tone identified.")

    if not reasons:
        return "No strong psychological manipulation patterns detected."

    return " | ".join(reasons)

# -----------------------------------
# SAFE REWRITE SUGGESTION
# -----------------------------------

def safe_rewrite(text):
    return "Suggested Neutral Rewrite: Please review the information carefully before making any decisions."

# -----------------------------------
# HISTORY FUNCTIONS
# -----------------------------------

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

# -----------------------------------
# UI INPUT
# -----------------------------------

text_input = st.text_area("Enter text to analyze")

threshold = st.slider("Set Manipulation Alert Threshold", 0, 15, 5)

# -----------------------------------
# ANALYSIS BUTTON
# -----------------------------------

if st.button("Analyze"):

    if text_input.strip() == "":
        st.warning("Please enter some text first.")
        st.stop()

    # Calculate Scores
    fear, urgency, sentiment_val, total = calculate_scores(text_input)

    # Save History
    save_history(total)

    # Calculate DNA
    dna_score, dna_level = calculate_influence_dna(fear, urgency, sentiment_val)

    # Classify
    category = classify_manipulation(fear, urgency)

    # Explanation
    explanation = generate_explanation(fear, urgency, sentiment_val)

    # -----------------------------------
    # METRICS
    # -----------------------------------

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fear Score", fear)
    col2.metric("Urgency Score", urgency)
    col3.metric("Negative Emotion", sentiment_val)
    col4.metric("Total Score", total)

    st.metric("🧬 Influence DNA Score", dna_score)
    st.write(f"### Risk Level: {dna_level}")

    # -----------------------------------
    # HEAT BAR
    # -----------------------------------

    st.write("### 🔥 Influence Intensity")
    st.progress(min(int(total), 15) / 15)

    # -----------------------------------
    # RADAR CHART
    # -----------------------------------

    st.write("### 🧠 Psychological Fingerprint")

    categories = ["Fear", "Urgency", "Negative Emotion"]
    values = [fear, urgency, sentiment_val]

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
    ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False
    )

    st.plotly_chart(fig_radar, use_container_width=True)

    # -----------------------------------
    # CLASSIFICATION & EXPLANATION
    # -----------------------------------

    st.write("### 🎯 Manipulation Type")
    st.warning(category)

    st.write("### 🔍 AI Explanation")
    st.info(explanation)

    # -----------------------------------
    # SAFE REWRITE
    # -----------------------------------

    st.write("### ✨ Safe Rewrite Suggestion")
    st.success(safe_rewrite(text_input))

    # -----------------------------------
    # ALERT SYSTEM
    # -----------------------------------

    if total > threshold:
        st.error("🚨 Manipulation Alert Triggered!")
    else:
        st.success("Content within safe limits.")

    # -----------------------------------
    # DOWNLOAD REPORT
    # -----------------------------------

    report = f"""
GenerAI Influence Sentinel Report

Fear Score: {fear}
Urgency Score: {urgency}
Negative Emotion: {sentiment_val}
Total Score: {total}
DNA Score: {dna_score}
Risk Level: {dna_level}
Manipulation Type: {category}
Explanation: {explanation}
"""

    st.download_button(
        label="📥 Download Analysis Report",
        data=report,
        file_name="analysis_report.txt"
    )

# -----------------------------------
# DRIFT SECTION
# -----------------------------------

st.write("### 📊 Psychological Drift Over Time")

history = load_history()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=list(range(1, len(history)+1)),
    y=history,
    mode='lines+markers',
    name="Manipulation Score"
))

fig.update_layout(
    xaxis_title="Analysis Number",
    yaxis_title="Manipulation Score"
)

st.plotly_chart(fig, use_container_width=True)

drift = calculate_drift()
st.metric("Psychological Drift Score", drift)