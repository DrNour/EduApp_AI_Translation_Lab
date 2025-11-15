"""
Lightweight scoring utils:
- If sacrebleu / pyter3 available, use them.
- Else fall back to simple n-gram precision + length ratio.
"""
from typing import Dict, List
import re

try:
    import sacrebleu  # type: ignore
except Exception:
    sacrebleu = None

try:
    from pyter3 import ter  # type: ignore
except Exception:
    ter = None

def _tokenise(s: str) -> List[str]:
    return re.findall(r"\w+|\S", s.strip(), flags=re.UNICODE)

def _ngram_precision(cand: str, ref: str, n:int=2) -> float:
    c = _tokenise(cand)
    r = _tokenise(ref)
    if len(c) < n or len(r) < n:
        return 0.0
    def ngrams(seq, n):
        return [" ".join(seq[i:i+n]) for i in range(len(seq)-n+1)]
    c_ngrams = ngrams(c, n)
    r_ngrams = set(ngrams(r, n))
    if not c_ngrams:
        return 0.0
    match = sum(1 for g in c_ngrams if g in r_ngrams)
    return match / len(c_ngrams)

def _len_ratio(cand: str, ref: str) -> float:
    return (len(_tokenise(cand)) + 1e-9) / (len(_tokenise(ref)) + 1e-9)

def score_all(candidate: str, reference: str) -> Dict[str, float]:
    out = {}
    # BLEU
    if sacrebleu:
        try:
            bleu = sacrebleu.corpus_bleu([candidate], [[reference]]).score / 100.0  # normalize 0-1
            out["BLEU"] = bleu
        except Exception:
            pass
    # TER
    if ter:
        try:
            out["TER"] = float(ter(reference.split(), candidate.split()))
        except Exception:
            pass
    # Fallbacks
    out.setdefault("p1", _ngram_precision(candidate, reference, 1))
    out.setdefault("p2", _ngram_precision(candidate, reference, 2))
    out.setdefault("len_ratio", _len_ratio(candidate, reference))
    return out
