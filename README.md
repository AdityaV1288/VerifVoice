# VerifVoice

**Privacy-preserving real-time AI that helps banks stop voice-coercion fraud.**

> *Banks authenticate who is paying. VerifVoice helps verify whether the decision to pay is being coerced.*

VerifVoice detects coercive voice scams while they happen and passes a privacy-preserving, expiring risk
signal to a bank so it can step up authentication before money leaves. Raw audio is never persisted, synthetic
speech is never treated as proof of fraud, and the user retains a safe override.

## Modules (by owner)

| Module | Owner | Purpose |
|---|---|---|
| `main.py` | Person 3 | FastAPI backend (`/health`, `/analyze`, `/analyze/upload`, `/payment/decision`, `/metrics`) — runs on LinuxONE |
| `pipeline.py` | Person 3 | Integration: runs Person 1 + Person 2 together (`analyze_call`) |
| `token_store.py` | Person 3 | In-memory risk tokens (TTL 120 s) |
| `risk_engine.py` | P4 (fallback by P3) | Risk fusion `R = 0.5C + 0.3S + 0.2N` + policy ladder |
| `semantic_model.py` | Person 2 | Speech & coercion detection (transcript → coercion score + reason codes) |
| `semantic_config.py` | Person 2 | Signals, weights, reason codes, gates |
| `audio_authenticity/` | Person 1 | Audio authenticity package (`analyze_audio` → spoof score) |
| `semantic_tests.py` | Person 2 | Smoke tests (6 core behaviours) |
| `run_eval.py` | Person 2 | Formal evaluation (23 fixtures + metrics + stability) |
| `vm_test.py` / `vm_evidence.py` | Person 3 | LinuxONE deployment smoke / evidence scripts |

## Setup

```powershell
. .\activate.ps1           # activates venv + ffmpeg on PATH
python -c "import semantic_model; print('ok')"
```

See `ENVIRONMENT.md` for the full setup guide.

## Quick checks

```powershell
python semantic_tests.py    # 6 smoke tests
python run_eval.py          # 22-fixture evaluation + safety metrics + stability
```

## Status

**Backend deployed and integrated** (tag `v1.0-integration`). Person 1 + Person 2 + Person 3 all wired: the full
`analyze → token → payment decision` loop is live on **LinuxONE s390x** (evidence in `DEPLOYMENT.md`).

- Person 2 rule engine: 23/23 fixtures pass (English + Hindi + Hinglish), 0 false positives.
- Open for **P1's adapter** and **P4's real risk engine** — both drop-in, no rearchitecture.
