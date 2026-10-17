"""Person 2 smoke tests (Phase 2.4).

Run:  python semantic_tests.py

Covers the core behaviours the rule engine must exhibit:
  * coercive transcript -> high score + reason codes
  * benign transcript -> low score, no codes
  * genuine emergency -> low score, EMERGENCY_NARRATIVE only (context, not coercion)
  * AAC/benign synthetic -> low score
  * too-short text -> insufficient_text (abstain)
  * unsupported language -> unsupported_language (abstain)
"""

import semantic_model as sm
import semantic_config as cfg

CASES = [
    {
        "name": "T01 golden scam (son in hospital)",
        "text": (
            "Hello, is this Meera? This is Dr. Sharma calling from City Hospital. "
            "Your son Rahul has been in a serious accident and needs emergency surgery "
            "right now. We need you to transfer Rs 50,000 immediately to book the "
            "operation theatre. Please do not tell anyone about this, it is very "
            "delicate. And do not try to call the hospital to verify - the lines are "
            "down. If we do not operate in the next hour, he may not survive."
        ),
        "min_score": 0.70,
        "must_have": ["COERCIVE_URGENCY", "FINANCIAL_INSTRUCTION", "SECRECY_PRESSURE",
                      "VERIFICATION_REFUSAL", "AUTHORITY_CLAIM", "EMERGENCY_NARRATIVE"],
    },
    {
        "name": "T09 benign family call",
        "text": "Hi beta, how are you? How was school today? Did you have lunch? "
                "We were just thinking about you and wanted to say hello.",
        "max_score": 0.30,
        "must_not_have": ["COERCIVE_URGENCY", "FINANCIAL_INSTRUCTION", "THREAT"],
    },
    {
        "name": "T10 genuine emergency (no money)",
        "text": "Hello? Uncle, dad had a small accident and we are at the hospital. "
                "The doctors say he is stable. Can you please come to the hospital? "
                "We are waiting near the emergency ward.",
        "max_score": 0.30,
        "must_have": ["EMERGENCY_NARRATIVE"],
        "must_not_have": ["FINANCIAL_INSTRUCTION"],
    },
    {
        "name": "T11 AAC/TTS benign pharmacy payment",
        "text": "Hello, this is my regular order. Please pay my usual amount to the "
                "pharmacy for this month's medicine as always. Thank you.",
        "max_score": 0.30,
        "must_not_have": ["THREAT", "SECRECY_PRESSURE"],
    },
    {
        "name": "T16 insufficient text",
        "text": "Hello?",
        "expect_status": "insufficient_text",
        "max_score": 0.05,
    },
    {
        "name": "T17 unsupported language (Tamil)",
        "text": "இது உங்கள் வங்கி. உங்கள் OTP ஐ பகிரவும் மற்றும் பணத்தை மாற்றவும். சீக்கிரம் செய்யுங்கள்.",
        "expect_status": "unsupported_language",
        "max_score": 0.05,
    },
]

def run():
    passed = 0
    failed = 0
    for case in CASES:
        r = sm.analyze(case["text"])
        ok = True
        msgs = []

        if "expect_status" in case and r["status"] != case["expect_status"]:
            ok = False
            msgs.append(f"status {r['status']!r} != {case['expect_status']!r}")

        if "min_score" in case and r["coercion_score"] < case["min_score"]:
            ok = False
            msgs.append(f"score {r['coercion_score']} < {case['min_score']}")

        if "max_score" in case and r["coercion_score"] > case["max_score"]:
            ok = False
            msgs.append(f"score {r['coercion_score']} > {case['max_score']}")

        for code in case.get("must_have", []):
            if code not in r["reason_codes"]:
                ok = False
                msgs.append(f"missing code {code}")

        for code in case.get("must_not_have", []):
            if code in r["reason_codes"]:
                ok = False
                msgs.append(f"unexpected code {code}")

        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {case['name']}")
        print(f"       score={r['coercion_score']} status={r['status']} "
              f"codes={r['reason_codes']}")
        if msgs:
            for m in msgs:
                print(f"         - {m}")
        print()
        if ok:
            passed += 1
        else:
            failed += 1

    print(f"=== {passed} passed, {failed} failed ===")
    return failed == 0


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
