# PERSON 2 — Speech & Coercion Detection · `semantic_model.py`

> **Your job:** build the transcript-analysis pipeline that detects coercion. Detect **urgency, secrecy,
> authority claims, verification refusal, and financial instructions**. Start with transparent rules; add a
> compact classifier only if time permits. **Deliverable file:** `semantic_model.py` returning **scores +
> reason codes**.
>
> **This is the PRIMARY signal** in the fusion formula `R = 0.5·C + 0.3·S + 0.2·N` — so your module carries
> the most weight. Get the rule layer rock-solid first; the model is a bonus.

---

## 0. Your exact interface (lock with Person 3)

```python
# semantic_model.py
def analyze_transcript(text: str, *, lang: str = "en") -> dict:
    """
    Returns:
      {
        "coercion_score": float 0..1,     # 1 = strongly coercive
        "reason_codes":   [str, ...],     # subset of the vocabulary below
        "signals": {                      # per-category 0..1 (for explainability + dashboard)
            "urgency": float,
            "authority_claim": float,
            "secrecy_pressure": float,
            "verification_refusal": float,
            "financial_instruction": float,
            "threat": float
        },
        "status": "analyzed" | "insufficient_text" | "unsupported_language",
        "lang": str
      }
    """
```

**Rules:**
- Too little text (e.g. < 5 tokens) → `status: "insufficient_text"`, score low → fusion treats as weak signal.
- Unsupported language → `status: "unsupported_language"` and **warn/abstain**, never auto-restrict.
- Every reason code must be **human-readable** and traceable to the matched cue (this is your explainability
  gift to the demo).

---

## 1. Reason-code vocabulary (freeze this with the team)

| Reason code | Meaning |
|---|---|
| `COERCIVE_URGENCY` | Immediate action demanded ("act now", "urgent", "within 5 minutes") |
| `AUTHORITY_CLAIM` | Claimed to be police/bank/hospital/govt/official |
| `SECRECY_PRESSURE` | "Don't tell anyone", "keep this private", "don't hang up" |
| `VERIFICATION_REFUSAL` | Discourages checking / verifying ("don't verify", "trust me") |
| `FINANCIAL_INSTRUCTION` | Directs transfer/UPI/OTP/PIN/payment |
| `THREAT` | Fear/arrest/account-blocked/legal consequences |
| `EMERGENCY_NARRATIVE` | Accident/hospital/relative-in-trouble story |

---

## 2. Transparent rule layer (build this FIRST — it's the whole deliverable)

```python
import re

# High-precision concept lists (extend for Hindi/Hinglish — see §5)
URGENCY = [r"\bact now\b", r"\burgent", r"\bimmediately\b", r"\bright now\b", r"\bwithin \d+ minutes\b",
           r"\bdon'?t delay\b", r"\bquick\b", r"\bhurry\b"]
AUTHORITY = [r"\bpolice\b", r"\bbank\b", r"\brbi\b", r"\bhospital\b", r"\bdoctor\b", r"\bofficer\b",
             r"\bgovernment\b", r"\bcustoms\b", r"\btax department\b", r"\bcbi\b", r"\bed\b"]
SECRECY = [r"\bdon'?t tell\b", r"\bkeep (it|this) (private|secret|confidential)\b", r"\bno one (else )?should know\b",
           r"\bdon'?t hang up\b", r"\bstay on the line\b"]
VERIF_REFUSAL = [r"\bdon'?t verify\b", r"\btrust me\b", r"\bno need to (check|confirm|call back)\b",
                 r"\bdon'?t call (the )?back\b", r"\bdon'?t (contact|ask)\b"]
FINANCIAL = [r"\btransfer\b", r"\bupi\b", r"\botp\b", r"\bpin\b", r"\bbank account\b", r"\bsend money\b",
             r"\bpay\b", r"\bnetbanking\b", r"\bqr code\b", r"\bpayment\b"]
THREAT = [r"\barrest\b", r"\baccount (will be |is )?(blocked|frozen|closed)\b", r"\blegal action\b",
          r"\bfine\b", r"\bgo to jail\b", r"\byour money will be\b"]
EMERGENCY = [r"\baccident\b", r"\binjured\b", r"\bhospital\b", r"\bsurgery\b", r"\bemergency\b",
             r"\bson\b", r"\bdaughter\b", r"\bhusband\b", r"\bwife\b", r"\bkidnapped\b"]

def _count(text, patterns):
    return float(sum(1 for p in patterns if re.search(p, text, re.IGNORECASE)))

def analyze_transcript(text, lang="en"):
    if not text or len(text.split()) < 5:
        return {"coercion_score": 0.0, "reason_codes": [], "signals": {},
                "status": "insufficient_text", "lang": lang}
    t = text.lower()
    signals = {
        "urgency":               _count(t, URGENCY),
        "authority_claim":       _count(t, AUTHORITY),
        "secrecy_pressure":      _count(t, SECRECY),
        "verification_refusal":  _count(t, VERIF_REFUSAL),
        "financial_instruction": _count(t, FINANCIAL),
        "threat":                _count(t, THREAT),
        "emergency_narrative":   _count(t, EMERGENCY),
    }
    # presence → capped per-category score (1 hit = strong; more hits saturate)
    cat_score = {k: min(1.0, v) for k, v in signals.items()}
    # coercion = weighted combination of the coercive categories
    coercion_score = min(1.0,
        0.25*cat_score["urgency"] +
        0.20*cat_score["financial_instruction"] +
        0.20*cat_score["threat"] +
        0.15*cat_score["verification_refusal"] +
        0.10*cat_score["authority_claim"] +
        0.10*cat_score["secrecy_pressure"])
    # reason codes: order by the strongest signals
    code_map = {
        "urgency": "COERCIVE_URGENCY", "authority_claim": "AUTHORITY_CLAIM",
        "secrecy_pressure": "SECRECY_PRESSURE", "verification_refusal": "VERIFICATION_REFUSAL",
        "financial_instruction": "FINANCIAL_INSTRUCTION", "threat": "THREAT",
        "emergency_narrative": "EMERGENCY_NARRATIVE",
    }
    reason_codes = [code_map[k] for k, v in cat_score.items() if v >= 1.0]
    return {"coercion_score": round(coercion_score, 3), "reason_codes": reason_codes,
            "signals": {k: round(v, 3) for k, v in cat_score.items()},
            "status": "analyzed", "lang": lang}
```

- **Why rules first:** transparent, deterministic, explainable, and it works with a *scripted transcript*
  even if ASR is flaky. Judges can inspect exactly why `COERCIVE_URGENCY` fired.
- **Keep weights configurable** (a small `config.py` or top-of-file dict) so you can tune thresholds on the fly.

---

## 3. Optional compact classifier (only if time remains)

- **Step 1 — ASR → text.** If Whisper-tiny installs and meets latency, use it. Otherwise use a lightweight
  recognizer, or (recommended for the demo) a **scripted-transcript adapter**: the demo passes pre-transcribed
  text for each sample. This removes ASR as a single point of failure.
- **Step 2 — features.** TF-IDF (or the rule-layer signal vector above) over the transcript.
- **Step 3 — classifier.** `LogisticRegression` (or small MLP) trained on a tiny labelled set of coercive vs
  benign transcripts you write during the event (10–20 examples each). Combine: `final = 0.7*rule_score +
  0.3*clf_score`, or use the classifier only to *boost* confidence.
- **Do NOT** put a large LLM in the critical path. Generative text (nice warnings) is post-hoc only.

---

## 4. How your score feeds the rest of the team
- Your `coercion_score` (0–1) is the **C** in `R = 0.5·C + 0.3·S + 0.2·N`.
- Your `reason_codes` merge into the risk token's `reason_codes` array (e.g. `COERCIVE_URGENCY`,
  `FINANCIAL_INSTRUCTION`) that the bank policy simulator displays.
- `signals` dict powers the dashboard's "why" breakdown.

---

## 5. Hindi / Hinglish code-switching (stretch, high judge value)
- Add transliterated + Devanagari keywords to each list, e.g.:
  - urgency: `जल्दी`, `तुरंत`, `abhi`, `jaldi`, `turant`
  - financial: `पैसे`, `paisa`, `paise bhejo`, `UPI`, `OTP`, `PIN`
  - authority: `पुलिस`, `police`, `bank wale`
  - secrecy: `kisi ko mat batana`, `किसी को मत बताना`
- Keep `lang` param so unsupported input returns `unsupported_language` rather than guessing.
- Normalize text (lowercase, strip diacritics for transliteration) before matching.

---

## 6. Test plan (you supply numbers; Person 6 formalizes)

| # | Transcript | Expect | What you record |
|---|---|---|---|
| A | Normal chat, no coercion, known payee | low `coercion_score`, no codes | score, codes |
| B | "Your son is in hospital, transfer ₹50,000 NOW, don't tell anyone, don't verify" | high score + `COERCIVE_URGENCY`+`FINANCIAL_INSTRUCTION`+`SECRECY_PRESSURE` | score, codes |
| C | Synthetic voice, benign text ("Hi, this is my pharmacy, pay my usual bill") | low coercion, no codes | score, codes |
| D | Genuine emergency ("Dad had an accident, please come") | elevated `EMERGENCY_NARRATIVE` but **no financial instruction** → moderate, override preserved | score, codes |

Also measure **semantic update latency** and log which rule fired for every code.

---

## 7. What to prepare BEFORE the event (allowed, no submission code)
- [ ] Freeze the reason-code vocabulary + interface above; share with Person 3.
- [ ] Draft the rule keyword lists (EN + Hindi/Hinglish) — this is design, not submission code.
- [ ] Prepare the labelled transcript set (coercive vs benign) for the optional classifier.
- [ ] Decide ASR path: Whisper-tiny (test s390x) vs scripted-transcript adapter (default).
- [ ] Write limitations: language coverage is declared + measured; unknown language → abstain.

## 8. What to write DURING the event
`semantic_model.py` (rule layer + `analyze_transcript`) · optional `train_semantic_clf.py` · a `data/` folder
with your labelled transcript examples (no real victim data) · a `config.py` for weights/thresholds.

---

## 9. Limitations to document
- Rule layer catches *high-precision* cues; it can miss paraphrased coercion (that's why the fusion + other
  signals exist, and why we don't claim perfect recall).
- Language coverage is explicit; unsupported → abstain/warn, never auto-restrict.
- No large LLM in the critical path (latency + honesty).
- `coercion_score` is a demo heuristic, not a calibrated probability.
