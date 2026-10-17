"""Deployment smoke test — run ON the VM to verify the full backend loop."""
import json
import urllib.request
import urllib.error

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


print("=== /health ===")
print(call("/health"))

print("=== /analyze (coercive text) ===")
status, analyze = call("/analyze", "POST", {
    "source": "Transfer 50000 rupees immediately, do not tell anyone",
    "input_type": "text",
})
print(status, "coercion_score:", analyze["coercion_score"], "token:", analyze["token_id"][:8])

print("=== /payment/decision (new beneficiary) ===")
print(call("/payment/decision", "POST", {
    "token_id": analyze["token_id"], "amount": 50000, "new_beneficiary": True,
}))

print("=== /payment/decision (bad token) ===")
print(call("/payment/decision", "POST", {
    "token_id": "nope", "amount": 1, "new_beneficiary": False,
}))

print("=== /metrics ===")
print(call("/metrics"))
