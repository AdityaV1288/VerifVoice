"""VerifVoice — Person 2: Speech & coercion detection.

Public interface (final — see PERSON2_ARCHITECTURE.md §3):

    transcribe(audio_path, lang) -> str      # audio -> text (Phase 3)
    analyze_transcript(text, lang) -> dict   # text -> coercion signal
    analyze(source, input_type, lang) -> dict# dispatcher (audio | text)

P3's backend calls ONLY the dispatcher `analyze()`. The scripted-transcript path
(input_type="text") is a first-class supported path, so the rule engine is never
blocked by ASR availability.

Status: Phase 3 — rule engine + faster-whisper transcription.
"""

import re

import semantic_config as config

# Compile the keyword patterns once at import time.
_COMPILED = {
    key: [re.compile(p, re.IGNORECASE) for p in patterns]
    for key, patterns in config.KEYWORDS.items()
}

# Mask negated credential requests ("we will NEVER ask for your OTP/PIN") so a
# bank's own safety warning isn't read as a financial instruction.
_MASK_NEGATED = re.compile(
    r"\b(?:never|do not|dont|will not|wont|should not|shouldnt|not) "
    r"(?:ask|share|give|reveal|disclose|provide|request) "
    r"(?:you )?(?:for )?(?:your )?"
    r"(?:otp|pin|password|cvv|credentials)"
    r"(?:\s*(?:or|and)\s*(?:otp|pin|password|cvv|credentials))*",
    re.IGNORECASE,
)


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
    """Heuristic: flag significant content in scripts we DON'T support (any
    non-Latin, non-Devanagari letters). English (Latin) and Hindi (Devanagari)
    are supported; Tamil/Telugu/Bengali/CJK/etc. -> abstain, never guess.
    """
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    other = sum(
        1 for c in letters
        if not c.isascii() and not ("\u0900" <= c <= "\u097f")
    )
    return (other / len(letters)) > 0.2


def _result(score: float, codes: list, status: str, lang: str) -> dict:
    """Build a schema-conformant result (§3.1)."""
    return {
        "coercion_score": score,
        "reason_codes": codes,
        "signals": {key: 0.0 for key in config.SIGNAL_KEYS},
        "status": status,
        "lang": lang,
    }


_model = None  # cached faster-whisper model (lazy-loaded)


def _get_model():
    """Lazily load the faster-whisper model. The import is deferred so the rule
    engine still works on hosts where faster-whisper is unavailable."""
    global _model
    if _model is None:
        import os
        # huggingface.co is unreachable from some networks; fall back to a mirror.
        # setdefault() respects any HF_ENDPOINT the caller already set explicitly.
        os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
        from faster_whisper import WhisperModel  # local import (optional dep)

        # Prefer the locally-downloaded model (models/faster-whisper-base) so the
        # demo works offline; otherwise download by name via the mirror.
        local = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "models", "faster-whisper-base",
        )
        model_name = (
            local if os.path.isfile(os.path.join(local, "model.bin"))
            else config.TRANSCRIBE_MODEL
        )

        _model = WhisperModel(
            model_name,
            device=config.TRANSCRIBE_DEVICE,
            compute_type=config.TRANSCRIBE_COMPUTE,
        )
    return _model


def transcribe(audio_path: str, lang: str = "auto") -> str:
    """Transcribe audio to text via faster-whisper.

    lang: "auto" -> whisper auto-detects the language; or a 2-letter code
    ("en", "hi"). Returns "" on ANY failure so callers degrade to the
    scripted-transcript path instead of crashing.

    Note: audio is decoded with librosa and passed to faster-whisper as a numpy
    array, because faster-whisper's built-in av.decode_audio() is incompatible
    with PyAV >= 15 (removed the `metadata_errors` kwarg).
    """
    try:
        import numpy as np
        import librosa
        model = _get_model()
        # 16 kHz mono float32 — exactly what Whisper expects.
        audio, _sr = librosa.load(audio_path, sr=16000, mono=True)
        audio = np.asarray(audio, dtype=np.float32)
        language = None if lang in (None, "", "auto") else lang
        segments, _info = model.transcribe(audio, beam_size=1, language=language)
        return " ".join(seg.text.strip() for seg in segments).strip()
    except Exception:
        return ""


def transcription_ready() -> bool:
    """True if the ASR model is usable (already loaded, or present locally).

    Does NOT trigger a download — safe to call from a /health endpoint. If
    False, the rule engine still works; only audio->text is unavailable.
    """
    import os
    if _model is not None:
        return True
    local = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "models", "faster-whisper-base",
    )
    return os.path.isfile(os.path.join(local, "model.bin"))


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
        subject = (
            _MASK_NEGATED.sub(" ", normalized)
            if key == "financial_instruction"
            else normalized
        )
        signals[key] = 1.0 if any(p.search(subject) for p in patterns) else 0.0

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
        text = transcribe(source)  # auto-detect language for ASR
        if not text:
            # No transcript -> abstain (weak signal, never "fraud").
            return _result(0.0, [], "insufficient_text", lang)
        return analyze_transcript(text, lang=lang)

    return analyze_transcript(source, lang=lang)
