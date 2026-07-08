import streamlit as st

st.title("🧠 Model Registry Management")

st.markdown("### Active Models")
st.success("v2.1 - Current Active Model (Deployed 2 hours ago)")

st.markdown("### Version History")
versions = [
    {"version": "v2.1", "status": "Active", "metrics": {"ndcg": 0.85}},
    {"version": "v2.0", "status": "Archived", "metrics": {"ndcg": 0.82}},
    {"version": "v1.0", "status": "Archived", "metrics": {"ndcg": 0.78}},
]

for v in versions:
    with st.expander(f"Model {v['version']} - Status: {v['status']}"):
        st.write(f"Metrics: NDCG = {v['metrics']['ndcg']}")
        if v['status'] != "Active":
            if st.button(f"Rollback to {v['version']}"):
                st.toast(f"Rolling back to {v['version']}...")
