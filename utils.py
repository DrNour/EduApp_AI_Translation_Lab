import os
import requests
import pandas as pd

def _get_secret(name, default=""):
    """Read from Streamlit secrets if available; else environment."""
    try:
        import streamlit as st
        return st.secrets.get(name, default)
    except Exception:
        return os.environ.get(name, default)

OPENAI_API_KEY = _get_secret("OPENAI_API_KEY", "")
GOOGLE_TRANSLATE_API_KEY = _get_secret("GOOGLE_TRANSLATE_API_KEY", "")

# --------- Engines ---------

def mt_openai(text: str,
              system_prompt: str = "You are a professional Arabic↔English translator. Preserve meaning and tone.",
              terms: str = "",
              model: str = "gpt-4o-mini") -> str:
    """Translate using OpenAI Chat Completions. Deterministic (temperature=0)."""
    if not OPENAI_API_KEY:
        return "[OpenAI key missing: add OPENAI_API_KEY in Secrets]"
    # Build terminology hint
    gloss = ""
    if terms:
        kv = [t.strip() for t in terms.split(",") if "=" in t]
        if kv:
            gloss = "\nUse these terminology mappings: " + "; ".join(kv)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt + gloss},
                {"role": "user", "content": text}
            ],
            temperature=0
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[OpenAI error: {e}]"

def mt_google_translate(text: str, target_lang: str = "ar", source_lang: str = "") -> str:
    """Google Translate API v2 via REST (optional)."""
    if not GOOGLE_TRANSLATE_API_KEY:
        return "[Google Translate key missing: add GOOGLE_TRANSLATE_API_KEY in Secrets]"
    try:
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {"q": text, "target": target_lang.lower(), "key": GOOGLE_TRANSLATE_API_KEY}
        if source_lang:
            params["source"] = source_lang.lower()
        r = requests.post(url, data=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data["data"]["translations"][0]["translatedText"]
    except Exception as e:
        return f"[Google Translate error: {e}]"

def fake_mt(text: str, src_lang="en", tgt_lang="ar") -> str:
    """Demo-only fallback if no keys: reverse tokens just to prove UI works."""
    toks = text.split()
    rev = " ".join(toks[::-1])
    return f"{rev} [{'AR' if tgt_lang.lower().startswith('ar') else 'MT'}]"

# --------- Data helpers ---------

def ensure_sample_pairs():
    """Create minimal dataset if not present."""
    os.makedirs("data", exist_ok=True)
    path = "data/sample_pairs.csv"
    if not os.path.exists(path):
        df = pd.DataFrame([
            {"id":1,"source":"Please submit your application before the deadline.",
             "reference":"يرجى تقديم طلبك قبل الموعد النهائي.","src_lang":"en","tgt_lang":"ar"},
            {"id":2,"source":"Health authorities recommend drinking water regularly.",
             "reference":"تنصح السلطات الصحية بشرب الماء بانتظام.","src_lang":"en","tgt_lang":"ar"},
            {"id":3,"source":"The museum will extend its opening hours during the festival.",
             "reference":"سيُمدد المتحف ساعات عمله خلال المهرجان.","src_lang":"en","tgt_lang":"ar"}
        ])
        df.to_csv(path, index=False)

def load_pairs(csv_path="data/sample_pairs.csv") -> pd.DataFrame:
    try:
        return pd.read_csv(csv_path)
    except Exception:
        return pd.DataFrame(columns=["id","source","reference","src_lang","tgt_lang"])
