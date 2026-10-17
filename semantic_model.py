"""VerifVoice — Person 2: Speech & coercion detection.

Public interface (final — see PERSON2_ARCHITECTURE.md §3):

    transcribe(audio_path, lang) -> str      # audio -> text (Phase 3)
    analyze_transcript(text, lang) -> dict   # text -> coercion signal
    analyze(source, input_type, lang) -> dict# dispatcher (audio | text)

P3's backend calls ONLY the dispatcher `analyze()`. The scripted-transcript path
(input_type="text") is a first-class supported path, so the rule engine is never
blocked by ASR availability.

Status: Phase 1 skeleton — interface is final, values are hard-coded placeholders.
"""

import semantic_config as config


def transcribe(audio_path: str, lang: str = "en") -> str:
    """Transcribe audio to text via faster-whisper (Phase 3).

    Returns "" on failure or unsupported input, so callers degrade gracefully.
    """
    # Phase 3: integrate faster-whisper here. Until then the dispatcher uses text.
    return ""


def analyze_transcript(text: str, lang: str = "en") -> dict:
    """Analyze transcript text and return the coercion signal (§3.1 schema).

    Phase 1: returns a schema-correct placeholder (coercion_score hard-coded).
    Phase 2 will replace the placeholder with the real rule engine.
    """
    signals = {key: 0.0 for key in config.SIGNAL_KEYS}
    return {
        "coercion_score": 0.5,          # TODO(Phase 2): real weighted score
        "reason_codes": [],
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
            return {
                "coercion_score": 0.0,
                "reason_codes": [],
                "signals": {key: 0.0 for key in config.SIGNAL_KEYS},
                "status": "insufficient_text",
                "lang": lang,
            }
        return analyze_transcript(text, lang=lang)

    return analyze_transcript(source, lang=lang)
