import streamlit as st
import requests

st.title("📈 Drift Monitoring")
st.write("Real-time behavioral and structural drift monitoring.")

try:
    resp = requests.get("http://localhost:8000/detect_status")
    if resp.status_code == 200:
        data = resp.json()
        st.metric(label="Drift Score (KS-Test)", value=f"{data['drift_score']:.4f}")
        st.metric(label="P-Value", value=f"{data['p_value']:.4f}")
        
        if data['is_drift']:
            st.error("🚨 DRIFT DETECTED!")
        else:
            st.success("✅ System Stable")
except Exception as e:
    st.error("Backend not reachable.")
