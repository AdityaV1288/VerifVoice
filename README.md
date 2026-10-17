# VerifVoice

**Privacy-preserving real-time AI that helps banks stop voice-coercion fraud.**

> *Banks authenticate who is paying. VerifVoice helps verify whether the decision to pay is being coerced.*

VerifVoice detects coercive voice scams while they happen and passes a privacy-preserving, expiring risk
signal to a bank so it can step up authentication before money leaves. Raw audio is never persisted, synthetic
speech is never treated as proof of fraud, and the user retains a safe override.

## Modules (by owner)

| Module | Owner | Purpose |
|---|---|---|
| `semantic_model.py` | Person 2 | Speech & coercion detection (transcript → coercion score + reason codes) |
| `semantic_config.py` | Person 2 | Signals, weights, reason codes, gates |
| `semantic_tests.py` | Person 2 | Smoke tests (6 core behaviours) |
| `run_eval.py` | Person 2 | Formal evaluation — 22 fixtures + metrics + stability + no-persistence |
| `example_api.py` | Person 3 (reference) | Working FastAPI reference showing how to call `semantic_model` — rename to `main.py` |
| `audio_model.py` | Person 1 | Audio authenticity / anti-spoofing (spoof score) |
| `risk_engine.py` | Person 4 | Risk fusion `R = 0.5C + 0.3S + 0.2N` + expiring risk token |
| `bank_simulator.py` | Person 4 | Payment policy ladder + safe override |
| `main.py` | Person 3 | FastAPI backend (`/health`, `/analyze`, `/payment/decision`, `/metrics`) |
| `app.py` | Person 5 | Dashboard |

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

**Person 2 module: feature-complete** (tag `v0.1-freeze`, + Phase 8). Rule engine + ASR + dispatcher +
evaluation all working: **23/23 fixtures pass** (English + Hindi + Hinglish), 0 false positives, golden path
stable across 3 runs. See `EVALUATION_RESULTS.md` for the full evidence handoff to Person 6.
