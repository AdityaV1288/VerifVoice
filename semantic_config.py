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
