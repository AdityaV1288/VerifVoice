"""Deployment smoke test — run ON the VM to verify the backend end-to-end."""
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
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


print("=== /health ===")
print(call("/health"))
print("=== /analyze (text) ===")
print(call("/analyze", "POST", {
    "source": "Transfer 50000 rupees immediately, do not tell anyone",
    "input_type": "text",
}))
print("=== /metrics ===")
print(call("/metrics"))
