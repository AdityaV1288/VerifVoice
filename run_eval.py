"""run_eval.py — Person 2 formal evaluation (Phase 5).

Runs every labelled fixture through semantic_model.analyze() and prints a results
table for Person 6, plus edge-case and no-persistence checks.

Run:  python run_eval.py
"""

import json
import os
import re

import semantic_model as sm

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "data", "transcripts", "fixtures.json")

BANDS = {"low": (0.0, 0.30), "moderate": (0.30, 0.70), "high": (0.70, 1.01)}


def classify(score: float) -> str:
    for band, (lo, hi) in BANDS.items():
        if lo <= score < hi:
            return band
    return "?"


def run_fixtures(fixtures):
    print("=" * 108)
    print(f"{'ID':<5}{'Label':<10}{'Score':<7}{'Band':<9}{'Exp':<9}{'Result':<7}Reason codes")
    print("-" * 108)
    passed = failed = deferred = 0
    rows = []
    for f in fixtures:
        r = sm.analyze(f["text"])
        score = r["coercion_score"]
        band = classify(score)
        exp = f["expected_band"]
        if exp == "deferred":
            res = "DEFER"
            deferred += 1
        else:
            ok = band == exp
            res = "PASS" if ok else "FAIL"
            passed += ok
            failed += (not ok)
        codes = ", ".join(r["reason_codes"]) or "-"
        print(f"{f['id']:<5}{f['label']:<10}{score:<7.2f}{band:<9}{exp:<9}{res:<7}{codes}")
        rows.append({"id": f["id"], "name": f["name"], "label": f["label"],
                     "score": score, "band": band, "expected": exp, "status": r["status"]})
    print("-" * 108)
    print(f"RESULT: {passed} passed, {failed} failed, {deferred} deferred (Phase 8)")
    return rows


def summarize(rows):
    coercive = [r for r in rows if r["label"] == "coercive"]
    benign = [r for r in rows if r["label"] == "benign"]

    # Safety metrics (the ones that matter for the README/slides).
    false_neg = [r for r in coercive if r["expected"] != "deferred" and r["score"] < 0.30]
    false_pos = [r for r in benign if r["score"] >= 0.30]
    print("\n--- Safety metrics ---")
    print(f"coercive caught (score >= 0.30): "
          f"{sum(1 for r in coercive if r['score'] >= 0.30)}/{len(coercive)}")
    print(f"benign left alone (score < 0.30):  "
          f"{sum(1 for r in benign if r['score'] < 0.30)}/{len(benign)}")
    if false_neg:
        print("false negatives (scam scored low):", [r["id"] for r in false_neg])
    if false_pos:
        print("false positives (benign scored >= 0.30):", [r["id"] for r in false_pos])
    else:
        print("false positives: none")


def run_edge_cases():
    print("\n--- Edge cases ---")
    cases = [
        ("empty string", ""),
        ("punctuation only", "!!! ??? ..."),
        ("one word", "Transfer!"),
        ("non-ASCII name", "Rahul — call me back."),
        ("very long text", ("Please stay calm and listen carefully. " * 60)),
    ]
    for name, text in cases:
        r = sm.analyze(text)
        print(f"{name:<18} score={r['coercion_score']:<5} status={r['status']}")


def check_no_persistence():
    print("\n--- No-persistence check ---")
    # The module must never write audio/transcripts to disk.
    write_patterns = re.compile(r"\b(open\(|\.write\(|to_csv|to_json|np\.save|sf\.write|dump)")
    offenders = []
    for fname in ("semantic_model.py", "semantic_config.py"):
        with open(os.path.join(HERE, fname), encoding="utf-8") as fh:
            for i, line in enumerate(fh, 1):
                if write_patterns.search(line):
                    offenders.append(f"{fname}:{i}: {line.strip()}")
    if offenders:
        print("WRITE CALLS FOUND:")
        for o in offenders:
            print("  ", o)
    else:
        print("PASS - no file-write calls in semantic_model.py / semantic_config.py.")


if __name__ == "__main__":
    data = json.load(open(FIXTURES, encoding="utf-8"))
    rows = run_fixtures(data["fixtures"])
    summarize(rows)
    run_edge_cases()
    check_no_persistence()
