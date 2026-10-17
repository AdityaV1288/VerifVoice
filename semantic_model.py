"""VerifVoice — Person 2: Speech & coercion detection.

Public interface (final — see PERSON2_ARCHITECTURE.md §3):

    transcribe(audio_path, lang) -> str      # audio -> text (Phase 3)
    analyze_transcript(text, lang) -> dict   # text -> coercion signal
    analyze(source, input_type, lang) -> dict# dispatcher (audio | text)

P3's backend calls ONLY the dispatcher `analyze()`. The scripted-transcript path
(input_type="text") is a first-class supported path, so the rule engine is never
blocked by ASR availability.

Status: Phase 2 — real rule engine (7 regex detectors + weighted score + reason codes).
"""

import re

import semantic_config as config

# Compile the keyword patterns once at import time.
_COMPILED = {
    key: [re.compile(p, re.IGNORECASE) for p in patterns]
    for key, patterns in config.KEYWORDS.items()
}


def _normalize(text: str) -> str:
    """Lowercase, fix curly apostrophes, expand common contractions, collapse
    whitespace. Contracting "do not" -> "dont" lets patterns match either form.
    """
    t = text.lower()
    t = t.replace("\u2019", "'").replace("\u2018", "'")
    t = re.sub(r"\bdo not\b", "dont", t)
    t = re.sub(r"\bdoes not\b", "doesnt", t)
    t = re.sub(r"\bcannot\b", "cant", t)
    t = re.sub(r"\bcan not\b", "cant", t)
    t = re.sub(r"\bwill not\b", "wont", t)
    t = re.sub(r"\bshould not\b", "shouldnt", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _detect_unsupported(text: str) -> bool:
    """Heuristic: significant Devanagari content is unsupported until Phase 8
    adds Hindi/Hinglish keyword lists. Returns True -> abstain, never guess.
    """
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    devanagari = sum(1 for c in letters if "\u0900" <= c <= "\u097f")
    return (devanagari / len(letters)) > 0.2


def _result(score: float, codes: list, status: str, lang: str) -> dict:
    """Build a schema-conformant result (§3.1)."""
    return {
        "coercion_score": score,
        "reason_codes": codes,
        "signals": {key: 0.0 for key in config.SIGNAL_KEYS},
        "status": status,
        "lang": lang,
    }


def transcribe(audio_path: str, lang: str = "en") -> str:
    """Transcribe audio to text via faster-whisper (Phase 3).

    Returns "" on failure or unsupported input, so callers degrade gracefully.
    """
    # Phase 3: integrate faster-whisper here. Until then the dispatcher uses text.
    return ""


def analyze_transcript(text: str, lang: str = "en") -> dict:
    """Analyze transcript text and return the coercion signal (§3.1 schema).

    Pipeline: normalize -> length/language gate -> 7 detectors -> weighted score
    -> reason codes.
    """
    if not isinstance(text, str):
        text = str(text)

    normalized = _normalize(text)

    # Gate 1: too little text -> abstain (weak signal, never "fraud").
    if len(normalized.split()) < config.MIN_TOKENS:
        return _result(0.0, [], "insufficient_text", lang)

    # Gate 2: unsupported language -> abstain.
    if lang not in config.SUPPORTED_LANGS or _detect_unsupported(normalized):
        return _result(0.0, [], "unsupported_language", lang)

    # Detectors: presence-capped 0/1 per category.
    signals = {}
    for key in config.SIGNAL_KEYS:
        patterns = _COMPILED.get(key, [])
        signals[key] = 1.0 if any(p.search(normalized) for p in patterns) else 0.0

    # Weighted score (emergency_narrative is deliberately absent from WEIGHTS).
    coercion_score = round(
        sum(config.WEIGHTS[k] * signals[k] for k in config.WEIGHTS), 4
    )

    # Reason codes: every category that fired, in SIGNAL_KEYS order.
    reason_codes = [
        config.REASON_CODES[k]
        for k in config.SIGNAL_KEYS
        if signals.get(k, 0.0) >= 1.0
    ]

    return {
        "coercion_score": coercion_score,
        "reason_codes": reason_codes,
        "signals": signals,
        "status": "analyzed",
        "lang": lang,
    }


def analyze(source: str, input_type: str = "text", lang: str = "en") -> dict:
    """Dispatcher: route audio through transcription, else treat as text.

    This is the ONLY entry point P3 should call.
    """
    if input_type == "audio":
        text = transcribe(source, lang=lang)
        if not text:
            # No transcript -> abstain (weak signal, never "fraud").
            return _result(0.0, [], "insufficient_text", lang)
        return analyze_transcript(text, lang=lang)

    return analyze_transcript(source, lang=lang)
