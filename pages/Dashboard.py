# pages/Dashboard.py
import os, io
import pandas as pd
import streamlit as st

st.title("Dashboard — Class Overview & Exports")

def downloadable(path, label, fname):
    if os.path.exists(path):
        buf = io.BytesIO(open(path,"rb").read())
        st.download_button(f"⬇️ {label}", buf, file_name=fname, mime="text/csv")
    else:
        st.info(f"{path} not found yet.")

st.subheader("Datasets")
downloadable("data/sample_pairs.csv", "Download sample_pairs.csv", "sample_pairs.csv")
downloadable("data/tickets.csv", "Download tickets.csv", "tickets.csv")

st.subheader("Research data")
downloadable("data/results.csv", "Download results.csv (submissions + metrics)", "results.csv")

# (optional) quick preview
for p in ["data/results.csv","data/tickets.csv","data/sample_pairs.csv"]:
    if os.path.exists(p):
        st.markdown(f"#### Preview: {p}")
        st.dataframe(pd.read_csv(p).head(50), use_container_width=True)
