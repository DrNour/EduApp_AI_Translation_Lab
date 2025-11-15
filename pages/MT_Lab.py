import streamlit as st
import pandas as pd

# Robust imports
utils_err = None
try:
    from utils_mt import ensure_sample_pairs, load_pairs, mt_openai, mt_google_translate, fake_mt
except ModuleNotFoundError as e:
    utils_err = e

st.title("MT Lab — Human vs MT vs Post-edit")
if utils_err:
    st.error("Could not import utils_mt. Ensure utils_mt.py is at repo root (same level as Home.py).")
    st.exception(utils_err)
    st.stop()

ensure_sample_pairs()
pairs = load_pairs()
if pairs.empty:
    st.info("Go to **Admin** to create or upload data.")
    st.stop()

row = st.selectbox("Choose a sentence", pairs.to_dict("records"),
                   format_func=lambda r: f"{r['id']}: {r['source'][:80]}")

c1, c2 = st.columns(2)
with c1: st.subheader("Source"); st.write(row["source"])
with c2: st.subheader("Reference"); st.write(row["reference"])

engine = st.radio("Engine", ["OpenAI", "Google Translate", "Demo (fake)"], horizontal=True)
terms = st.text_input("Terminology (e.g., policy=سياسة, ministry=الوزارة)", "")
system_prompt = st.text_area("System prompt (OpenAI only)",
    "You are a professional Arabic↔English translator. Preserve meaning and tone.")

if st.button("Translate"):
    if engine == "OpenAI":
        out = mt_openai(row["source"], system_prompt=system_prompt, terms=terms)
    elif engine == "Google Translate":
        tgt = "ar" if row["tgt_lang"].lower().startswith("ar") else "en"
        src = "en" if row["src_lang"].lower().startswith("en") else "ar"
        out = mt_google_translate(row["source"], target_lang=tgt, source_lang=src)
    else:
        out = fake_mt(row["source"], src_lang=row["src_lang"], tgt_lang=row["tgt_lang"])
    st.session_state["mt_out"] = out

st.text_area("MT Output", value=st.session_state.get("mt_out",""), height=150)
st.text_area("Your Post-edit", value="", height=150, placeholder="Improve the MT output...")
