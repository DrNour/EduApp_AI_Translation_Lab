import streamlit as st
import pandas as pd
from utils_mt import ensure_sample_pairs, load_pairs, mt_openai, mt_google_translate, fake_mt
from metrics import score_all

st.title("MT Lab — Human vs MT vs Post-edit")
st.caption("Generate MT (OpenAI if configured; optional Google), post-edit, and score vs reference.")

ensure_sample_pairs()
pairs = load_pairs()
if pairs.empty:
    st.info("Go to **Admin** to create or upload data.")
    st.stop()

row = st.selectbox("Choose a sentence", pairs.to_dict("records"),
                   format_func=lambda r: f"{r['id']}: {r['source'][:80]}")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Source")
    st.write(row["source"])
with c2:
    st.subheader("Reference (Human)")
    st.write(row["reference"])

st.markdown("### Choose Engine")
engine = st.radio("Engine", ["OpenAI", "Google Translate", "Demo (fake)"], horizontal=True)
terms = st.text_input("Terminology (comma-separated e.g., policy=سياسة, ministry=الوزارة)", "")
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

mt_text = st.text_area("MT Output", value=st.session_state.get("mt_out",""), height=150)
pe_text = st.text_area("Your Post-edit", value="", height=150,
                       placeholder="Improve the MT output here...")

if st.button("Score vs Reference"):
    cand = pe_text.strip() or mt_text.strip()
    if not cand:
        st.warning("Nothing to score yet — generate MT or paste your text.")
    else:
        s = score_all(cand, row["reference"])
        st.success("Scores")
        st.write({k: (round(v,3) if isinstance(v,float) else v) for k,v in s.items()})
