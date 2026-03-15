from typing import Dict, List, Union
from sacrebleu.metrics import BLEU, TER
from bert_score import score as bertscore_score


bleu_metric = BLEU()
ter_metric = TER()


def score_all(candidate: str, reference: str, lang: str = "en") -> Dict[str, Union[float, str]]:
    """
    Compute BLEU, TER, and BERTScore for a candidate translation against a reference.

    Args:
        candidate: MT output or post-edited text
        reference: Gold/reference translation
        lang: Language code for BERTScore model selection (default: 'en')

    Returns:
        Dict of metric scores.
    """
    candidate = (candidate or "").strip()
    reference = (reference or "").strip()

    if not candidate or not reference:
        return {
            "bleu": 0.0,
            "ter": 100.0,
            "bertscore_precision": 0.0,
            "bertscore_recall": 0.0,
            "bertscore_f1": 0.0,
        }

    # sacrebleu expects: sys_stream, [ref_streams]
    bleu = bleu_metric.sentence_score(candidate, [reference]).score
    ter = ter_metric.sentence_score(candidate, [reference]).score

    # BERTScore returns tensors
    P, R, F1 = bertscore_score(
        [candidate],
        [reference],
        lang=lang,
        verbose=False
    )

    return {
        "bleu": round(float(bleu), 4),
        "ter": round(float(ter), 4),
        "bertscore_precision": round(float(P[0]), 4),
        "bertscore_recall": round(float(R[0]), 4),
        "bertscore_f1": round(float(F1[0]), 4),
    }
