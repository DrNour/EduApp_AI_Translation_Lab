import os, pandas as pd, streamlit as st
from utils_mt import ensure_sample_pairs

st.title("Admin")
st.caption("Create or upload the dataset used in MT Lab.")

if st.button("Create/Reset sample_pairs.csv"):
    ensure_sample_pairs()
    st.success("Created data/sample_pairs.csv ✅")

uploaded = st.file_uploader("Or upload your own pairs CSV", type=["csv"])
if uploaded:
    os.makedirs("data", exist_ok=True)
    with open("data/sample_pairs.csv","wb") as w:
        w.write(uploaded.getvalue())
    st.success("Uploaded to data/sample_pairs.csv")
