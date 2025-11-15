import streamlit as st
import pandas as pd

st.title("MQM Annotation — Simplified")
st.caption("Label errors for a candidate vs reference.")

source = st.text_area("Source", "The ministry will publish the annual report tomorrow.")
reference = st.text_area("Reference (Human)", "ستصدر الوزارة التقرير السنوي غدًا.")
candidate = st.text_area("Candidate (Your translation)", "")

cats = ["Accuracy:Mistranslation","Accuracy:Omission","Accuracy:Addition",
        "Fluency:Grammar","Fluency:Punctuation","Fluency:Spelling",
        "Style:Terminology","Style:Register","Style:Consistency"]

st.markdown("#### Add error")
col1, col2 = st.columns([2,1])
with col1:
    sel = st.selectbox("Category", cats)
with col2:
    span = st.text_input("Span (optional)", "")

if "errs" not in st.session_state:
    st.session_state["errs"] = []

if st.button("Add"):
    st.session_state["errs"].append({"category": sel, "span": span})

if st.session_state["errs"]:
    st.markdown("#### Current errors")
    st.dataframe(pd.DataFrame(st.session_state["errs"]))
