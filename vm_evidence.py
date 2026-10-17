"""vm_evidence.py — LinuxONE deployment evidence (run ON the VM).

Captures the artifacts judges check: architecture, live service, golden-path
stability (3x), latency, and no-audio-persistence.
"""
import glob
import json
import os
import subprocess
import urllib.error
import urllib.request

BASE = "http://localhost:8000"


def call(path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


print("=== ARCHITECTURE ===")
print(subprocess.run(["uname", "-m"], capture_output=True, text=True).stdout.strip())

print("=== RUNNING SERVICE ===")
print(subprocess.run(["sh", "-c", "ps -ef | grep 'uvicorn main:app' | grep -v grep"],
                     capture_output=True, text=True).stdout.strip())

print("=== /health ===")
print(call("/health"))

print("=== GOLDEN PATH x3 (analyze -> token -> payment) ===")
COERCIVE = "Transfer 50000 rupees immediately, do not tell anyone"
runs = []
for i in range(3):
    _, a = call("/analyze", "POST", {"source": COERCIVE, "input_type": "text"})
    _, d = call("/payment/decision", "POST",
                {"token_id": a["token_id"], "amount": 50000, "new_beneficiary": True})
    runs.append((a["coercion_score"], d["decision"], d["risk_score"]))
    print(f"run {i+1}: coercion={a['coercion_score']} decision={d['decision']} risk={d['risk_score']}")

print("STABLE (all 3 identical):", len(set(runs)) == 1)

print("=== NO AUDIO PERSISTENCE ===")
wavs = glob.glob(os.path.expanduser("~/verifvoice/**/*.wav"), recursive=True)
print("wav files under ~/verifvoice:", wavs if wavs else "NONE")

print("=== /metrics (latency) ===")
print(call("/metrics"))
