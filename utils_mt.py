# utils_mt.py
"""
Utility layer for EduApp:
- OpenAI translation (lazy import so Admin doesn't crash if 'openai' isn't installed yet)
- Sample pairs dataset helpers
- Ticket (assignment) helpers
- Results logging for research exports

Place this file at the REPO ROOT (same level as Home.py).
"""

from __future__ import annotations
import os, time
from typing import Tuple, Optional, Dict, Any
import pandas as pd

# ------------- Config / Secrets -------------
def _get_secret(name: str, default: str = "") -> str:
    """
    Read secrets from Streamlit (preferred) or environment.
    Works both on Streamlit Cloud and locally.
    """
    try:
        import streamlit as st  # optional; only used to read secrets
        val = st.secrets.get(name, None)
        if isinstance(val, str) and val.strip():
            return val.strip()
    except Exception:
        pass
    return os.getenv(name, default).strip()

OPENAI_API_KEY = _get_secret("OPENAI_API_KEY", "")

# ------------- OpenAI (lazy import) -------------
def _get_openai_client() -> Tuple[Optional[Any], Optional[str]]:
    """
    Lazy-import OpenAI so pages like Admin can load even if the lib isn't installed yet.
    Returns (client, error_message).
    """
    try:
        from openai import OpenAI  # type: ignore
    except Exception as e:
        return None, (
            "[OpenAI library missing: add 'openai>=1.52.0' to requirements.txt "
            "and reboot the app. Details: %s]" % e
        )
    try:
        if not OPENAI_API_KEY:
            return None, "[OpenAI key missing: add OPENAI_API_KEY in Streamlit Secrets]"
        client = OpenAI(api_key=OPENAI_API_KEY)
        return client, None
    except Exception as e:
        return None, f"[OpenAI init error: {e}]"

def mt_openai(
    text: str,
    system_prompt: str = "You are a professional Arabic↔English translator. Preserve meaning and tone.",
    terms: str = "",
    model: str = "gpt-4o-mini",
) -> str:
    """
    Deterministic translation via OpenAI Chat Completions.
    - terms: comma-separated "source=target" glossary hints (optional)
    """
    # Build glossary hint
    gloss = ""
    if terms:
        kv = [t.strip() for t in terms.split(",") if "=" in t]
        if kv:
            gloss = "\nUse these terminology mappings: " + "; ".join(kv)

    client, err = _get_openai_client()
    if err:
        return err

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt + gloss},
                {"role": "user", "content": text},
            ],
            temperature=0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[OpenAI error: {e}]"

# ------------- Pairs dataset (for MT Lab) -------------
SAMPLE_PAIRS_PATH = "data/sample_pairs.csv"

def ensure_sample_pairs():
    """Create a small demo dataset if it doesn't exist."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(SAMPLE_PAIRS_PATH):
        df = pd.DataFrame([
            {"id":1,"source":"Please submit your application before the deadline.",
             "reference":"يرجى تقديم طلبك قبل الموعد النهائي.","src_lang":"en","tgt_lang":"ar"},
            {"id":2,"source":"Health authorities recommend drinking water regularly.",
             "reference":"تنصح السلطات الصحية بشرب الماء بانتظام.","src_lang":"en","tgt_lang":"ar"},
            {"id":3,"source":"The museum will extend its opening hours during the festival.",
             "reference":"سيُمدد المتحف ساعات عمله خلال المهرجان.","src_lang":"en","tgt_lang":"ar"},
        ])
        df.to_csv(SAMPLE_PAIRS_PATH, index=False)

def load_pairs(csv_path: str = SAMPLE_PAIRS_PATH) -> pd.DataFrame:
    """Load pairs CSV with safe fallback columns."""
    try:
        return pd.read_csv(csv_path)
    except Exception:
        return pd.DataFrame(columns=["id","source","reference","src_lang","tgt_lang"])

# ------------- Tickets (assignments) -------------
TIX_PATH = "data/tickets.csv"

def ensure_tickets_file():
    """Ensure tickets.csv exists with proper header."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(TIX_PATH):
        pd.DataFrame(columns=[
            "ticket_id","source","reference","src_lang","tgt_lang",
            "assigned_to","due_date","status","points"
        ]).to_csv(TIX_PATH, index=False)

def load_tickets() -> pd.DataFrame:
    """Load tickets with safe fallback."""
    ensure_tickets_file()
    try:
        return pd.read_csv(TIX_PATH)
    except Exception:
        return pd.DataFrame(columns=[
            "ticket_id","source","reference","src_lang","tgt_lang",
            "assigned_to","due_date","status","points"
        ])

def save_tickets(df: pd.DataFrame):
    """Persist current tickets table."""
    os.makedirs("data", exist_ok=True)
    df.to_csv(TIX_PATH, index=False)

def add_ticket(
    ticket_id: str,
    source: str,
    reference: str = "",
    src_lang: str = "en",
    tgt_lang: str = "ar",
    assigned_to: str = "",
    due_date: str = "",
    status: str = "open",
    points: int = 5,
):
    """
    Append a single ticket (used by Admin 'paste ticket' form).
    """
    df = load_tickets()
    new = {
        "ticket_id": ticket_id,
        "source": source,
        "reference": reference,
        "src_lang": src_lang,
        "tgt_lang": tgt_lang,
        "assigned_to": assigned_to,
        "due_date": due_date,
        "status": status,
        "points": points,
    }
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    save_tickets(df)

# ------------- Results logging (research exports) -------------
RESULTS_PATH = "data/results.csv"

def append_result(row: Dict[str, Any]):
    """
    Append a submission row to results.csv.
    Expected keys (flexible): timestamp, student, mode, item_id/ticket_id, source, reference,
    mt_output, post_edit, terms, system_prompt, metric_*.
    """
    os.makedirs("data", exist_ok=True)
    r = dict(row)
    r.setdefault("timestamp", int(time.time()))
    try:
        df = pd.read_csv(RESULTS_PATH)
    except Exception:
        df = pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([r])], ignore_index=True)
    df.to_csv(RESULTS_PATH, index=False)
