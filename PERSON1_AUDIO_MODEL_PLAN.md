# PERSON 1 — AI & Audio Authenticity · `audio_model.py`

> **Your job:** produce one real (or honestly-labelled) audio-authenticity signal: is the speech likely
> genuine, synthetic, replayed, or otherwise manipulated? Return a **score + a quality/status field**.
> **Deliverable file:** `audio_model.py`. **Fallback (agreed):** if no compatible model runs, the semantic
> classifier (Person 2) becomes primary and your module returns `status: "unavailable"` with audio
> authenticity documented as a future module.
>
> **Non-negotiable:** a synthetic/replay score must NEVER alone trigger a bank action. Your output is ONE
> of THREE signals feeding the fusion engine (`R = 0.5·C + 0.3·S + 0.2·N`).

---

## 0. Your exact interface (lock this with Person 3)

Agree on this function shape so Person 3/4 can call it regardless of which model you use:

```python
# audio_model.py
def analyze_audio(path_or_bytes: str | bytes) -> dict:
    """
    Returns:
      {
        "status":   "analyzed" | "unavailable" | "low_quality" | "error",
        "spoof_score": float 0..1,   # 1 = most likely synthetic/replayed/manipulated
        "quality":  float 0..1,      # audio quality / confidence gate
        "model":    str,             # e.g. "aasist2", "mfcc_cnn", "heuristic", "unavailable"
        "detail":   dict,            # optional: per-window scores, duration, sample rate
        "error":    str | None
      }
    """
```

**Key rules:**
- If you have NOT actually run a model, return `status: "unavailable"` and `spoof_score: None` — **never
  invent a number.**
- Low quality (`quality < threshold`, e.g. < 0.35) → `status: "low_quality"`, lower confidence; the fusion
  engine treats this as "insufficient signal," not "fraud."

---

## 1. Model option ladder (try in this order, stop when something runs)

### Option A — Pretrained AASIST-family (best credibility, hardest to run on s390x)
- `clovaai/aasist` (GitHub, official PyTorch, ASVspoof 2019 LA) — reference #26.
- `MTUCI/AASIST3` / `lab260/AASIST3` (Hugging Face) — reference #27/#31.
- **Reality check:** needs PyTorch. PyTorch s390x wheels are NOT reliably available on LinuxONE Community
  Cloud. **Only attempt this on your laptop for a "reference score," and timebox it to ~45 min.**
- If it runs locally, export to ONNX (`torch.onnx.export`) so it *can* target LinuxONE via ONNX Runtime/zDLC.

### Option B — Compact pretrained ONNX anti-spoofing / audio model (best LinuxONE fit)
- Look for a small ONNX audio classifier (e.g. a speech/audio-tagging or anti-spoof model on Hugging Face
  with an `.onnx` artifact). Verify it loads under **onnxruntime** (which has s390x wheels more often than
  PyTorch — but still verify on the VM).
- This is the path that makes the "real inference on LinuxONE" evidence story work.

### Option C — Lightweight MFCC/log-mel CNN or shallow classifier (guaranteed to run)
- Extract **MFCC or log-mel** features (librosa) → feed a **small sklearn model** (LogisticRegression /
  RandomForest / tiny MLP) or a tiny hand-written CNN (numpy or onnxruntime).
- Train on a **tiny, clearly-labelled** set you create: a few real clips + a few synthetic (TTS) + a few
  replayed clips. **Be honest:** this is a *demo heuristic on a handful of samples*, not a production detector.
- Runs on any CPU including s390x (numpy/sklearn/onnxruntime are far more portable than torch).

### Option D — Explicit fallback (zero model)
- `status: "unavailable"`, `spoof_score: None`, with a note that semantic model is primary. **Document this
  in the README as a labeled future module.** This is an acceptable, honest outcome per the plan.

> **Decision rule:** spend at most 45–60 min on A, 60 min on B, then commit to C (or D). Do NOT burn half
> the day compiling torch.

---

## 2. Feature extraction (shared by B and C)

```python
import numpy as np
import librosa  # verify it installs on s390x; else fall back to scipy/numpy FFT

def extract_features(path_or_bytes, sr=16000, n_mfcc=20, n_mels=40):
    y, actual_sr = librosa.load(path_or_bytes, sr=sr, mono=True)
    # quality gate: duration, clipping, energy
    duration = len(y) / actual_sr
    rms = np.sqrt(np.mean(y**2))
    clipping = np.mean(np.abs(y) > 0.99)
    quality = float(np.clip(1.0 - 0.5*clipping - (0.0 if rms > 1e-4 else 0.5), 0.0, 1.0))

    mfcc = librosa.feature.mfcc(y=y, sr=actual_sr, n_mfcc=n_mfcc)      # (n_mfcc, T)
    mel  = librosa.feature.melspectrogram(y=y, sr=actual_sr, n_mels=n_mels)
    logmel = librosa.power_to_db(mel)
    # aggregate to a fixed-size vector (mean + std over time) for the shallow model
    feats = np.concatenate([mfcc.mean(1), mfcc.std(1), logmel.mean(1), logmel.std(1)])
    return feats.astype(np.float32), {"duration": duration, "rms": float(rms),
                                      "clipping": clipping, "quality": quality, "sr": actual_sr}
```

- **Portability note:** if `librosa`/`soundfile`/`FFmpeg` don't install on s390x, pre-extract features on the
  laptop and send feature vectors (or pre-decoded PCM) to the server. Keep the boundary explicit in the demo.
- **No disk audio:** load into memory, process, and release. Never write `.wav`/features to disk.

---

## 3. Fallback shallow model (Option C) — train during the event

```python
# train once during the event (keep it tiny, keep it honest)
from sklearn.ensemble import RandomForestClassifier  # or LogisticRegression

# X: rows of extract_features() vectors; y: 0=genuine, 1=synthetic/replay/manipulated
clf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=0)
clf.fit(X_train, y_train)
# spoof_score = predicted probability of class 1
spoof_score = float(clf.predict_proba(feat.reshape(1, -1))[0][1])
```

- **Split honestly:** train/val/test separation; report the small test-set accuracy/ROC-AUC and clearly state
  sample count. Do NOT report a "99% accuracy" headline from 8 clips.
- **Calibrate:** scores are relative to your tiny training set — describe them as a *demo heuristic*, not a
  real-world probability. Consider a monotonic remap so a mid-score reads as "uncertain."

---

## 4. ONNX export + zDLC attempt (your LinuxONE evidence contribution)

1. Export your small sklearn/numpy/CNN model to ONNX (sklearn → `skl2onnx` or a tiny numpy forward pass
   re-implemented in onnxruntime-friendly ops).
2. `python -m onnxruntime.tools.checker <model.onnx>` → validate.
3. Inspect operators: `onnx.helper` / `onnxruntime` supported ops on s390x.
4. If zDLC is available on the VM: pull the official IBM zDLC image, compile for the **detected** arch
   (`uname -m`), run test vectors through original vs compiled, compare tolerance + measure p50/p95.
5. **Record the truth:** CPU / partially-accelerated / accelerated. Label honestly.
6. Keep a small fallback that definitely runs (Option C) in case zDLC/ONNX compilation fails.

---

## 5. Test plan (Person 6 will formalize — you supply the numbers)

Prepare at least these, then run `audio_model.py` on each and record the score + quality:

| # | Sample | Expect | What you record |
|---|---|---|---|
| 1 | Genuine human speech (clean) | low spoof_score, high quality | score, quality, latency |
| 2 | TTS / cloned voice (synthetic) | elevated spoof_score (if model works) | score, quality |
| 3 | Replay (speaker → mic) | model may degrade — note it | score, quality + note |
| 4 | Noisy / clipped / too-short clip | `low_quality` or `unavailable`, not "fraud" | quality gate behavior |
| 5 | Silence / non-speech | abstain / low quality | abstention correctness |

Also measure **inference latency** (model-only) vs end-to-end.

---

## 6. What to prepare BEFORE the event (allowed, no submission code)

- [ ] Download model checkpoints / ONNX artifacts + note their **licenses** and exact URLs.
- [ ] Collect a handful of **publicly licensed** genuine + synthetic + replay clips (ASVspoof sample files,
      public TTS demos). **No real victim audio, no copyrighted recordings in the repo.**
- [ ] Verify which deps have s390x wheels (librosa, soundfile, onnxruntime, skl2onnx, numpy). Have a
      feature-pre-extraction fallback plan.
- [ ] Write down the interface contract above and share with Person 3.
- [ ] Draft your "limitations" bullets (honest): cross-domain EER degradation, replay weakness, tiny training
      set, no real-world calibration.

## 7. What to write DURING the event (keep it minimal)
`audio_model.py` = `extract_features()` + `analyze_audio()` (+ optional `load_model()`). Plus a small
`train_fallback.py` only if you use Option C. A `models/` folder with the checkpoint + a `LICENSES.md` line.

---

## 8. Limitations to document (be the honest team)
- Synthetic/replay score is a **supporting** signal; never gates a payment alone.
- Model may be trained on a small, non-representative set → treat scores as relative, not calibrated.
- Replay and cross-codec conditions degrade detectors (cite the "Replay Attacks Against Audio Deepfake
  Detection" paper and ASVspoof 2021 cross-dataset EER results).
- If `status: "unavailable"`, say so plainly — the demo still works via the semantic model.
