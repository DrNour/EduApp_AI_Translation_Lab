# utils_mt.py
from openai import OpenAI
import os, pandas as pd, time

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or ""

# -------------------- OpenAI MT --------------------
def mt_openai(
    text: str,
    system_prompt: str = "You are a professional Arabic↔English translator. Preserve meaning and tone.",
    terms: str = "",
    model: str = "gpt-4o-mini",
) -> str:
    if not OPENAI_API_KEY:
        return "[OpenAI key missing: add OPENAI_API_KEY in Streamlit Secrets]"
    gloss = ""
    if terms:
        kv = [t.strip() for t in terms.split(",") if "=" in t]
        if kv:
            gloss = "\nUse these terminology mappings: " + "; ".join(kv)
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
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

# -------------------- Sample pairs --------------------
def ensure_sample_pairs():
    os.makedirs("data", exist_ok=True)
    path = "data/sample_pairs.csv"
    if not os.path.exists(path):
        df = pd.DataFrame([
            {"id":1,"source":"Please submit your application before the deadline.",
             "reference":"يرجى تقديم طلبك قبل الموعد النهائي.","src_lang":"en","tgt_lang":"ar"},
            {"id":2,"source":"Health authorities recommend drinking water regularly.",
             "reference":"تنصح السلطات الصحية بشرب الماء بانتظام.","src_lang":"en","tgt_lang":"ar"},
            {"id":3,"source":"The museum will extend its opening hours during the festival.",
             "reference":"سيُمدد المتحف ساعات عمله خلال المهرجان.","src_lang":"en","tgt_lang":"ar"},
        ])
        df.to_csv(path, index=False)

def load_pairs(csv_path="data/sample_pairs.csv"):
    try:
        return pd.read_csv(csv_path)
    except Exception:
        return pd.DataFrame(columns=["id","source","reference","src_lang","tgt_lang"])

# -------------------- Tickets (assignments) --------------------
TIX_PATH = "data/tickets.csv"

def ensure_tickets_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(TIX_PATH):
        pd.DataFrame(columns=[
            "ticket_id","source","reference","src_lang","tgt_lang","assigned_to","due_date","status","points"
        ]).to_csv(TIX_PATH, index=False)

def load_tickets() -> pd.DataFrame:
    ensure_tickets_file()
    try:
        return pd.read_csv(TIX_PATH)
    except Exception:
        return pd.DataFrame(columns=[
            "ticket_id","source","reference","src_lang","tgt_lang","assigned_to","due_date","status","points"
        ])

def save_tickets(df: pd.DataFrame):
    os.makedirs("data", exist_ok=True)
    df.to_csv(TIX_PATH, index=False)

def add_ticket(ticket_id: str, source: str, reference: str = "", src_lang="en", tgt_lang="ar",
               assigned_to: str = "", due_date: str = "", status: str = "open", points: int = 5):
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

# -------------------- Results logging (for research) --------------------
RESULTS_PATH = "data/results.csv"

def append_result(row: dict):
    os.makedirs("data", exist_ok=True)
    row = dict(row)
    row.setdefault("timestamp", int(time.time()))
    try:
        df = pd.read_csv(RESULTS_PATH)
    except Exception:
        df = pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(RESULTS_PATH, index=False)
