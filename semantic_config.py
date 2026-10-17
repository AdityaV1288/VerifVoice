"""VerifVoice — Person 2 configuration.

Every tunable lives here so P4 (risk fusion) can adjust weights/thresholds
without touching the rule-engine logic. See PERSON2_ARCHITECTURE.md §3.

Safety principle: emergency_narrative is CONTEXT, not coercion — it is reported
but never contributes to coercion_score.
"""

# The 7 signal categories the rule engine detects.
SIGNAL_KEYS = [
    "urgency",
    "authority_claim",
    "secrecy_pressure",
    "verification_refusal",
    "financial_instruction",
    "threat",
    "emergency_narrative",
]

# Weights for coercion_score (sum to 1.0). emergency_narrative is deliberately
# excluded: a genuine emergency ("Dad had an accident, please come") is not
# coercion by itself.
WEIGHTS = {
    "urgency": 0.25,
    "financial_instruction": 0.20,
    "threat": 0.20,
    "verification_refusal": 0.15,
    "authority_claim": 0.10,
    "secrecy_pressure": 0.10,
}

# Reason-code vocabulary — shared contract with P4's risk token.
REASON_CODES = {
    "urgency": "COERCIVE_URGENCY",
    "authority_claim": "AUTHORITY_CLAIM",
    "secrecy_pressure": "SECRECY_PRESSURE",
    "verification_refusal": "VERIFICATION_REFUSAL",
    "financial_instruction": "FINANCIAL_INSTRUCTION",
    "threat": "THREAT",
    "emergency_narrative": "EMERGENCY_NARRATIVE",
}

# Gates.
MIN_TOKENS = 5                     # below this -> "insufficient_text"
SUPPORTED_LANGS = {"en"}           # extend with "hi"/"hinglish" in Phase 8

# Coercion-score bands (informational; P4 owns the actual payment policy).
BAND_LOW = 0.30
BAND_HIGH = 0.70

# Keyword patterns per signal. High-precision regex, matched case-insensitively
# against a normalized transcript. presence-capped: 1 hit == 1.0 (no counting).
#
# Design notes:
#   * "hospital"/"doctor" are NOT authority claims here — they live in
#     emergency_narrative (a genuine emergency mentions them too). Authority
#     fires on explicit role claims ("this is Dr. ...", "calling from ...").
#   * emergency_narrative is reported but NOT scored (see WEIGHTS).
KEYWORDS = {
    "urgency": [
        r"\bact now\b",
        r"\burgent(?:ly)?\b",
        r"\bimmediately\b",
        r"\bright now\b",
        r"\bright away\b",
        r"\bwithin \d+ minutes\b",
        r"\bdon'?t delay\b",
        r"\bhurry\b",
        r"\basap\b",
        r"\bat once\b",
        r"\bquickly\b",
        r"\bas soon as possible\b",
        r"\bbefore (?:the|this) offer expires\b",
        r"\boffer expires\b",
        r"\blimited time\b",
        r"\blast chance\b",
        r"\btoday only\b",
        r"\bact fast\b",
    ],
    "authority_claim": [
        r"\bpolice\b",
        r"\bbank\b",
        r"\brbi\b",
        r"\bofficer\b",
        r"\bgovernment\b",
        r"\bcustoms\b",
        r"\btax department\b",
        r"\bincome tax\b",
        r"\bcbi\b",
        r"\bcyber ?crime\b",
        r"\belectricity\b",
        r"\bthis is (?:dr|doctor|professor|inspector|officer|sub-?inspector|senior|constable)\b",
        r"\bi'?m calling from (?:the )?(?:police|bank|hospital|government|tax|cyber ?crime|electricity)\b",
    ],
    "secrecy_pressure": [
        r"\bdon'?t tell\b",
        r"\bkeep (?:it|this) (?:private|secret|confidential)\b",
        r"\bno one (?:else )?should know\b",
        r"\bdon'?t hang up\b",
        r"\bstay on the line\b",
        r"\bbetween (?:just )?us\b",
    ],
    "verification_refusal": [
        r"\bdon'?t verify\b",
        r"\btrust me\b",
        r"\bno need to (?:check|confirm|verify|call)\b",
        r"\bdon'?t call (?:back|the bank|the police|the hospital|them|anyone)\b",
        r"\bdon'?t (?:contact|ask|check)\b",
        r"\blines? (?:are|is) down\b",
    ],
    # KNOWN LIMITATION (Phase 5): keyword matching cannot distinguish "share your
    # OTP" (scam) from "we will NEVER ask for your OTP" (legit). A negated mention
    # still fires this signal -> coercion_score +0.20 (LOW, harmless — never blocks
    # alone). Tracked in PERSON2_ARCHITECTURE.md §7 and PERSON2_TASKS.md Phase 5.
    "financial_instruction": [
        r"\btransfer(?:s|red|ring)?\b",
        r"\bupi\b",
        r"\botp\b",
        r"\bpin\b",
        r"\bbank account\b",
        r"\bsend money\b",
        r"\bsend me\b",
        r"\bsend (?:rs\.?|rupees|inr|₹)?\s*\d",
        r"\bnet ?banking\b",
        r"\bqr code\b",
        r"\bpa(?:y|id|ying|yment)\b",
    ],
    "threat": [
        r"\barrest(?:ed|s)?\b",
        r"\baccount (?:will be |is )?(?:blocked|frozen|closed|deactivated|seized|emptied)\b",
        r"\blegal action\b",
        r"\bjail\b",
        r"\bcase (?:will be )?filed\b",
        r"\bdisconnect(?:ed|ion)?\b",
        r"\bdeactivat(?:e|ed|ion)\b",
        r"\bpenalty\b",
        r"\b(?:may|might|will) not survive\b",
        r"\bnever see (?:her|him|them|you) again\b",
    ],
    "emergency_narrative": [
        r"\baccident\b",
        r"\binjur(?:ed|y|ies)\b",
        r"\bhospital\b",
        r"\bsurgery\b",
        r"\bemergency\b",
        r"\bambulance\b",
        r"\bkidnap(?:ped|ping)?\b",
        r"\brushed to\b",
    ],
}

# Transcription (ASR) settings — used by semantic_model.transcribe().
TRANSCRIBE_MODEL = "base"       # faster-whisper size: tiny | base | small | medium
TRANSCRIBE_DEVICE = "cpu"
TRANSCRIBE_COMPUTE = "int8"     # int8 = fast/low-memory on CPU
