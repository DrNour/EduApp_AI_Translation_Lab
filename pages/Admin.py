import streamlit as st

# Robust import: support root utils_mt.py or utils/utils_mt.py
try:
    from utils_mt import ensure_sample_pairs
except ModuleNotFoundError:
    try:
        from utils.utils_mt import ensure_sample_pairs  # if you put it under utils/
    except ModuleNotFoundError as e:
        st.error("Could not import utils_mt. Make sure utils_mt.py exists at repo root (same level as Home.py).")
        st.exception(e)
        st.stop()

st.title("Admin")
st.caption("Create or upload the dataset used in MT Lab.")

if st.button("Create/Reset sample_pairs.csv"):
    ensure_sample_pairs()
    st.success("Created data/sample_pairs.csv ✅")
