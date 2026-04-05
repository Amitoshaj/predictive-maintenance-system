import streamlit as st
import joblib
import pandas as pd
import os
import datetime

# =========================
# LOAD MODEL (ROBUST PATH)
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "model", "model.pkl")

model = joblib.load(model_path)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Industrial AI Dashboard", layout="wide")

# =========================
# HEADER
# =========================
st.markdown("""
# 🏭 Industrial Predictive Maintenance System
### 👨‍💻 Operator: Amitosh Junghare
#### Real-time AI Monitoring & Failure Prediction
""")

st.info("This system monitors machine health and predicts failures using AI.")
st.caption(f"Last Updated: {datetime.datetime.now().strftime('%H:%M:%S')}")

st.markdown("---")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Control Panel")

temp = st.sidebar.slider("🌡️ Temperature (°C)", 50, 120, 70)
pressure = st.sidebar.slider("⚙️ Pressure (Pa)", 20, 80, 30)
vibration = st.sidebar.slider("📉 Vibration", 0.0, 0.1, 0.02)

run = st.sidebar.button("▶️ Run System Check")

# =========================
# SENSOR MONITORING
# =========================
st.markdown("## 📊 Sensor Monitoring")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Temperature", f"{temp} °C")

with col2:
    st.metric("Pressure", f"{pressure} Pa")

with col3:
    st.metric("Vibration", f"{vibration}")

st.markdown("---")

# =========================
# AI DECISION ENGINE
# =========================
st.markdown("## 🧠 AI Decision Engine")

alerts = []
logs = []
history = []

if run:
    # =========================
    # MODEL PREDICTION
    # =========================
    result = model.predict([[temp, pressure, vibration]])
    proba = model.predict_proba([[temp, pressure, vibration]])

    confidence = round(max(proba[0]) * 100, 2)

    # =========================
    # ALERT LOGIC
    # =========================
    if temp > 85:
        alerts.append("⚠️ High Temperature")

    if vibration > 0.04:
        alerts.append("⚠️ Vibration Issue")

    if temp > 95 and vibration > 0.05:
        alerts.append("🚨 Critical Condition")

    if result[0] == 1:
        alerts.append("🔴 AI Failure Risk")

    # =========================
    # SYSTEM STATUS
    # =========================
    st.markdown("---")

    if result[0] == 1:
        st.markdown("## 🔴 SYSTEM STATUS: CRITICAL")
        st.error("System Failure Likely - Immediate Action Required")
    else:
        st.markdown("## 🟢 SYSTEM STATUS: NORMAL")
        st.success("System Operating Normally")

    # =========================
    # ALERT PANEL
    # =========================
    st.markdown("### 🚨 Active Alerts")

    if alerts:
        for alert in alerts:
            st.warning(alert)
            logs.append(f"[ALERT] {alert}")
    else:
        st.success("✅ No active alerts")

    # =========================
    # CONFIDENCE
    # =========================
    st.info(f"🎯 Model Confidence: {confidence}%")

    # =========================
    # HISTORY (SINGLE ENTRY)
    # =========================
    history.append({
        "Temperature": temp,
        "Pressure": pressure,
        "Vibration": vibration
    })

# =========================
# EVENT LOGS
# =========================
st.markdown("---")
st.markdown("## 📜 Event Logs")

for log in logs:
    st.write(log)

# =========================
# SENSOR TREND
# =========================
if history:
    st.markdown("---")
    st.markdown("## 📈 Sensor Trend Analysis")

    df = pd.DataFrame(history)
    st.line_chart(df)

# =========================
# MODEL INSIGHTS
# =========================
st.markdown("---")
st.markdown("## 📊 Model Insights")

try:
    st.image(model_path.replace("model.pkl", "feature_importance.png"),
             caption="Feature Importance Analysis")
except:
    st.warning("Feature importance graph not found. Please train model again.")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("🔧 AI-Based Industrial Monitoring System")
st.markdown("👨‍💻 Developed by Amitosh Junghare")