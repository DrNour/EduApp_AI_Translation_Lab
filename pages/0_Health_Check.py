# pages/0_Health_Check.py
import os, glob, importlib, streamlit as st

st.title("Health Check")

st.subheader("Python & Env")
st.write("Python:", os.sys.version)
st.write("CWD:", os.getcwd())

st.subheader("Files present")
top = sorted([p for p in glob.glob("*") if not os.path.isdir(p)])
dirs = sorted([p for p in glob.glob("*/")])
st.write("Top-level files:", top)
st.write("Directories:", dirs)
st.write("Pages:", sorted(glob.glob("pages/*.py")))
st.write(".streamlit:", sorted(glob.glob(".streamlit/*")))

st.subheader("Imports")
def check(mod):
    try:
        importlib.import_module(mod)
        st.write(f"✅ {mod}")
    except Exception as e:
        st.write(f"❌ {mod} -> {e}")

for m in ["utils_mt", "metrics", "pandas", "openai", "requests", "sacrebleu", "pyter3"]:
    check(m)

st.subheader("Secrets")
ok_openai = "OPENAI_API_KEY" in st.secrets
st.write("OPENAI_API_KEY:", "✅ set" if ok_openai else "❌ missing")
ok_google = "GOOGLE_TRANSLATE_API_KEY" in st.secrets
st.write("GOOGLE_TRANSLATE_API_KEY:", "✅ set" if ok_google else "— (optional)")
