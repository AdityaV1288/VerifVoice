"""pipeline.py — combined VerifVoice analysis (Person 1 + Person 2).

This is the INTEGRATION layer that connects the two signal modules:

  * Person 2 `semantic_model`      -> coercion_score + reason_codes (C)
  * Person 1 `audio_authenticity`  -> authenticity_score / spoof (S)

The combined result is what Person 3's `/analyze` endpoint returns, and what
Person 4's fusion consumes:  R = 0.5*C + 0.3*S + 0.2*N.

P4's fusion + payment policy live in `risk_engine.py` / `bank_simulator.py`
(not here). This module only guarantees the two signals arrive together,
correctly labelled, and that a missing spoof model never breaks the demo.
"""

import uuid

import semantic_model
from audio_authenticity import analyze_audio


def analyze_call(source: str, input_type: str = "text", lang: str = "en") -> dict:
    """Run BOTH signal modules and return a unified, JSON-ready result.

    * input_type == "text"  -> coercion only (no audio for the spoof model).
    * input_type == "audio" -> coercion (transcribes via faster-whisper) AND
      audio authenticity (WAV).

    The spoof side is allowed to be `model_unavailable` (Person 1's honest
    default) — that is surfaced as status, not as a crash.
    """
    result = {
        "request_id": str(uuid.uuid4()),
        "input_type": input_type,
        "lang": lang,
        # --- Person 2: coercion (always available) ---
        "coercion_score": None,
        "coercion_status": None,
        "reason_codes": [],
        "signals": {},
        # --- Person 1: audio authenticity (audio only) ---
        "spoof_score": None,
        "spoof_status": None,
        "spoof_classification": None,
        "quality_score": None,
        "model_name": None,
        "spoof_reasons": [],
        "spoof_warnings": [],
    }

    # Person 2 — coercion (transcribes internally when input_type == "audio").
    coercion = semantic_model.analyze(source, input_type=input_type, lang=lang)
    result["coercion_score"] = coercion["coercion_score"]
    result["coercion_status"] = coercion["status"]
    result["reason_codes"] = coercion["reason_codes"]
    result["signals"] = coercion["signals"]

    # Person 1 — audio authenticity (only meaningful for a real audio file).
    if input_type == "audio":
        try:
            audio = analyze_audio(source)
            d = audio.to_dict()
            result["spoof_score"] = d["authenticity_score"]
            result["spoof_status"] = d["status"]
            result["spoof_classification"] = d["classification"]
            result["quality_score"] = d["quality_score"]
            result["model_name"] = d["model_name"]
            result["spoof_reasons"] = list(d["reasons"])
            result["spoof_warnings"] = list(d["warnings"])
        except Exception as exc:  # never let P1 break the coercion path
            result["spoof_status"] = "error"
            result["spoof_warnings"] = [str(exc)]

    return result


# --------------------------------------------------------------------------- #
# Reference only — Person 4 owns fusion + policy. Kept here so the combined
# output is self-documenting about where the risk score comes from.
#
#   R = 0.5 * coercion_score + 0.3 * spoof_score + 0.2 * new_beneficiary
#
# When spoof_score is None (model unavailable), P4 should degrade gracefully
# (e.g. renormalize onto the coercion signal, or treat S as unknown) rather than
# fabricate a number.
# --------------------------------------------------------------------------- #
