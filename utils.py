
import json, time, hashlib
from typing import List, Dict
import pandas as pd

# ---------- Minimal metrics (dependency-free) ----------
def tokenise(text: str) -> List[str]:
    return text.strip().split()

def simple_ngram_precision(candidate: str, reference: str, n:int=2) -> float:
    c = tokenise(candidate)
    r = tokenise(reference)
    if len(c) < n or len(r) < n:
        return 0.0 if len(c) < n else float(len(set(c)&set(r)))/max(1,len(c))
    def ngrams(seq, n):
        return [" ".join(seq[i:i+n]) for i in range(len(seq)-n+1)]
    c_ngrams = ngrams(c,n)
    r_ngrams = set(ngrams(r,n))
    if not c_ngrams:
        return 0.0
    match = sum(1 for g in c_ngrams if g in r_ngrams)
    return match/len(c_ngrams)

def length_ratio(candidate: str, reference: str) -> float:
    rc = len(tokenise(candidate))
    rr = len(tokenise(reference))
    return (rc/(rr+1e-9))

def naive_score(candidate: str, reference: str) -> Dict[str, float]:
    return {
        "p1": simple_ngram_precision(candidate, reference, n=1),
        "p2": simple_ngram_precision(candidate, reference, n=2),
        "len_ratio": length_ratio(candidate, reference)
    }

# ---------- Placeholders for MT engines ----------
def fake_mt(text: str, src_lang="en", tgt_lang="ar") -> str:
    # Simple reversible toy "mt": reverse words, not real MT!
    toks = text.split()
    rev = " ".join(toks[::-1])
    if tgt_lang.lower().startswith("ar"):
        return rev + " [AR]"
    return rev + " [MT]"

def hash_id(*args) -> str:
    return hashlib.md5(("||".join([str(a) for a in args])).encode()).hexdigest()[:10]

# ---------- Minimal storage (CSV-based) ----------
def load_pairs(csv_path="data/sample_pairs.csv") -> pd.DataFrame:
    try:
        return pd.read_csv(csv_path)
    except Exception:
        return pd.DataFrame(columns=["id","source","reference","src_lang","tgt_lang"])

def append_result(row: Dict, out_csv="data/results.csv"):
    df = None
    try:
        df = pd.read_csv(out_csv)
    except Exception:
        df = pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(out_csv, index=False)

# ---------- MQM Schema (simplified) ----------
MQM_SCHEMA = [
    {"category":"Accuracy","sub":["Mistranslation","Omission","Addition"]},
    {"category":"Fluency","sub":["Grammar","Punctuation","Spelling"]},
    {"category":"Style","sub":["Terminology","Register","Consistency"]}
]
