import streamlit as st
import requests

st.title("🛍️ Product Recommendations")

user_id = st.text_input("Enter User ID", value="u_123")
top_k = st.slider("Number of recommendations", 1, 20, 10)

if st.button("Get Recommendations"):
    with st.spinner("Fetching predictions via FastAPI..."):
        try:
            response = requests.post("http://localhost:8000/recommend", json={"user_id": user_id, "top_k": top_k})
            if response.status_code == 200:
                data = response.json()
                st.success("Recommendations fetched successfully!")
                
                cols = st.columns(3)
                for idx, item in enumerate(data.get("recommendations", [])):
                    with cols[idx % 3]:
                        st.info(f"**{item['item_id']}**\n\nScore: {item['score']:.4f}")
            else:
                st.error("Error connecting to Backend Core")
        except Exception as e:
            st.error(f"API Error: {e}")
