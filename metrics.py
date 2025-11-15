# metrics.py
from typing import Dict, List
import re

def _tok(s: str) -> List[str]:
    return re.findall(r"\w+|\S", s.strip(), flags=re.UNICODE)

def _ngram_precision(cand: str, ref: str, n:int=2) -> float:
    c = _tok(cand); r = _tok(ref)
    if len(c) < n or len(r) < n: return 0.0
    def ngrams(seq, n): return [" ".join(seq[i:i+n]) for i in range(len(seq)-n+1)]
    c_ngrams = ngrams(c, n); r_ngrams = set(ngrams(r, n))
    if not c_ngrams: return 0.0
    match = sum(1 for g in c_ngrams if g in r_ngrams)
    return match / len(c_ngrams)

def _len_ratio(cand: str, ref: str) -> float:
    return (len(_tok(cand)) + 1e-9) / (len(_tok(ref)) + 1e-9)

def score_all(candidate: str, reference: str) -> Dict[str, float]:
    return {
        "p1": _ngram_precision(candidate, reference, 1),
        "p2": _ngram_precision(candidate, reference, 2),
        "len_ratio": _len_ratio(candidate, reference),
    }
