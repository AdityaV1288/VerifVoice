# VerifVoice — Deployment & Evidence (LinuxONE)

> **Owner:** team (Person 3 role). This documents what is deployed, how to reproduce it, and what is
> real vs simulated — for the judges and for the team.

## 1. What runs where

| Layer | Location | Why |
|---|---|---|
| `main.py` (FastAPI) | **LinuxONE s390x** | the scoring + decision endpoint |
| `pipeline.py` (P1+P2 integration) | LinuxONE s390x | pure Python |
| `semantic_model` rule engine (coercion) | **LinuxONE s390x** | the "AI runs on LinuxONE" evidence |
| `risk_engine` + token store | LinuxONE s390x | fusion + expiring token |
| `audio_authenticity` (spoof, AASIST ONNX) | **laptop only** | onnxruntime + scipy have no s390x wheels |
| ASR (`faster-whisper` + `librosa`) | **laptop only** | no s390x wheels; text path is the guaranteed LinuxONE path |

## 2. Reproduce the deployment (fresh VM)

```bash
# 1) Python 3.12 (RHEL 9 AppStream) + venv
sudo dnf -y install python3.12 python3.12-pip
python3.12 -m venv ~/verifvoice-env

# 2) backend deps (all pure-Python, s390x-safe)
~/verifvoice-env/bin/pip install fastapi uvicorn pydantic python-multipart

# 3) copy the backend files into ~/verifvoice/
#    main.py  pipeline.py  semantic_model.py  semantic_config.py
#    token_store.py  risk_engine.py  audio_authenticity/

# 4) run it
cd ~/verifvoice
setsid ~/verifvoice-env/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 < /dev/null &

# 5) verify
curl http://localhost:8000/health
~/verifvoice-env/bin/python vm_test.py      # full loop
~/verifvoice-env/bin/python vm_evidence.py  # evidence + stability
```

**Restart after a change:**
```bash
pkill -f "[u]vicorn main:app"   # bracket trick avoids self-match
# then re-run the "setsid ... uvicorn" command above
```

## 3. Live evidence (captured on the VM)

| Artifact | Value |
|---|---|
| Architecture | `s390x` |
| Running service | `python -m uvicorn main:app --host 0.0.0.0 --port 8000` (PID 4292) |
| `/health` | `{semantic_rules: ready, transcription: unavailable, audio_authenticity: model_unavailable, risk_engine: ready}` |
| Golden path ×3 | coercion **0.55** → decision **"verify"** → risk **0.64**, **identical all 3 runs** |
| Latency | `/analyze` ≈ 0.1 ms · `/payment/decision` ≈ 0.01 ms |
| Audio persistence | **0** `.wav` files under `~/verifvoice` |

## 4. Real vs simulated (say this plainly in the video)

- **Real:** the coercion rule engine, the token service, the fusion formula, the payment policy ladder, the
  FastAPI service — all executing on s390x.
- **Real:** the AASIST anti-spoofing model (MIT, ASVspoof 2019 LA pretrained) returns a genuine `spoof_score`
  on the **laptop** (e.g. 0.9997 on a TTS clip). It runs on the laptop, not LinuxONE, because ONNX Runtime and
  SciPy have no s390x wheels — the video states this boundary.
- **Real but uncalibrated:** `coercion_score` is a transparent rule heuristic, and `spoof_score` is an
  uncalibrated softmax — neither is a calibrated probability.
- **Simulated:** the bank action itself (we never touch a real transfer) — `decision` is a *proposed* policy
  action.
- **Honestly unavailable:** on LinuxONE, `spoof_score` is still `null` (fusion renormalizes onto coercion and
  flags `SPOOF_UNAVAILABLE`); ASR also runs on the laptop, not LinuxONE.

## 5. Open points (drop-in, no rearchitecture)

- **P1 (audio authenticity):** ✅ DONE — AASIST ONNX adapter integrated (`VERIFVOICE_ADAPTER=aasist_onnx`,
  `models/aasist.onnx`). Runs on the laptop. To make it run on LinuxONE, P1 would need s390x builds of
  onnxruntime + scipy (not available from PyPI today).
- **P4 (risk fusion):** replace the body of `risk_engine.decide()` (same signature + return shape). `main.py`
  needs no change.

## 6. No-persistence note

The only disk write in the backend is `main.py`'s upload endpoint saving the incoming file to a
**temporary directory** (deleted immediately after processing). No audio or transcript is written to permanent
storage anywhere in `main.py`, `pipeline.py`, `token_store.py`, `risk_engine.py`, or `semantic_model.py`.
