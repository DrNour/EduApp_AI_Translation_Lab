import streamlit as st
import pandas as pd
import os

st.title("Dashboard — Class Overview")
st.caption("Upload results.csv to visualize cohort metrics.")

path = "data/results.csv"
if os.path.exists(path):
    df = pd.read_csv(path)
    st.dataframe(df.head(50))
else:
    st.info("No data/results.csv yet. (You can extend MT_Lab to append results here.)")
