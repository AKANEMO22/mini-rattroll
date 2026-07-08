import streamlit as st

st.set_page_config(
    page_title="Adaptive Recommender Platform",
    page_icon="🚀",
    layout="wide",
)

st.title("Adaptive Hybrid Recommender System")
st.markdown("""
Welcome to the Platform-Level MLOps System.
Please select a page from the sidebar to begin:
- **Recommendation**: End-user view
- **Drift Monitoring**: Real-time MLOps sensors
- **Model Management**: Admin Registry
- **Simulation**: Inject manual data drift
""")
