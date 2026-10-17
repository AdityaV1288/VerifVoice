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

## Status

In progress — Person 2 module: Phase 1 skeleton committed (interface final, rule engine next).
