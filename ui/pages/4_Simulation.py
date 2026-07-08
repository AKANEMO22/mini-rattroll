import streamlit as st
import requests

st.title("🧪 Drift Simulation Lab")
st.write("Inject artificial drift to test the Adaptive Controller.")

drift_type = st.selectbox("Select Drift Type", ["Interaction Drop", "Preference Shift", "Context Seasonality", "Catalog Change"])
severity = st.slider("Severity", 0.1, 1.0, 0.5)

if st.button("Inject Drift"):
    try:
        resp = requests.post("http://localhost:8000/simulate", json={"type": drift_type, "severity": severity})
        if resp.status_code == 200:
            st.toast("Drift injected successfully!")
            st.success("Controller is now analyzing the data stream...")
    except Exception as e:
        st.error("Backend not reachable.")
