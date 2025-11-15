import streamlit as st
from utils_mt import mt_openai

st.title("Prompt Lab — Design & Test Prompts")

text = st.text_area("Enter source text", "The city will launch new community programs next month.")
terms = st.text_input("Terminology mapping (optional)", "programs=برامج, community=مجتمعية")
system = st.text_area("System prompt", "You are a professional Arabic↔English translator. Preserve meaning and tone.")
style = st.text_input("Style/constraints (optional)", "Formal MSA, concise, no ambiguity.")

if st.button("Generate with OpenAI"):
    prompt = f"{text}\n\nConstraints: {style}"
    out = mt_openai(prompt, system_prompt=system, terms=terms)
    st.text_area("Model Output", out, height=200)
