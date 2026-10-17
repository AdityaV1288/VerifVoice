# Person 3 — Backend & LinuxONE Deployment · Step-by-Step Tasks

> **Owner:** team (covering P3). **Companion doc:** `PERSON3_ARCHITECTURE.md` (read §3 contract first).
> **How to use:** work top-to-bottom. Each task = **goal → steps → Definition of Done**. Many tasks are already
> half-done because `example_api.py` exists — build on it, don't rebuild.

---

## Phase 0 — Prep (do NOW, before writing code)

- [ ] **0.1 — Confirm LinuxONE access.** Get the VM address, username, and the SSH key (the `VerifVoice.pem`
  you moved out of the repo is likely this). Test `ssh -i <key> user@<host>` connects. **Keep the key out of git.**
- [ ] **0.2 — Read the existing backend.** Open `example_api.py` (it already has `/health`, `/analyze` wired to
  `pipeline`, `/metrics`) and `pipeline.py`. You're renaming + extending, not starting over.
- [ ] **0.3 — Freeze the §3 contract with P4/P5.** Send them `PERSON3_ARCHITECTURE.md`. Confirm P4 accepts the
  `/payment/decision` request/response shape and P5 accepts the `/analyze` response.

**Exit:** SSH works; contract sent; you know exactly what `example_api.py` already does.

---

## Phase 1 — Lock scope: make the backend real (≈45 min)

- [ ] **1.1 — Rename `example_api.py` → `main.py`.** Update the module docstring. Confirm it still runs:
  `uvicorn main:app --reload --port 8000`, then `GET /health`.
- [ ] **1.2 — Add `CORS`** so P5's frontend can call it from another origin.
  ```python
  from fastapi.middleware.cors import CORSMiddleware
  app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
  ```
- [ ] **1.3 — Smoke-test both `/analyze` paths** (text and a real `.wav`) and confirm the response matches §3.

**Exit (DoD):** `main.py` runs, `/health` + `/analyze` (text + audio) return correct shapes.

---

## Phase 2 — Token service + payment decision (≈60 min)

- [ ] **2.1 — Add the in-memory token store** (`token_store.py`):
  - `create_token(scores: dict) -> (token_id, ttl)` — id = `uuid4().hex`, `expires_at = now + 120`, purge expired.
  - `get_token(token_id) -> dict | None` — returns None if unknown or expired.
  - Store only `{coercion_score, spoof_score, reason_codes}` — **never transcript/audio**.
- [ ] **2.2 — Have `/analyze` create a token.** Add `token_id` + `token_ttl_seconds` to the response.
- [ ] **2.3 — Add `/payment/decision`** with an **inline fallback risk engine** (P4 not built yet):
  ```python
  def _fallback_decide(C, S, new_beneficiary):
      if S is None:                       # spoof model unavailable → renormalize, don't fabricate
          R = 0.8*C + 0.2*(1 if new_beneficiary else 0)
      else:
          R = 0.5*C + 0.3*S + 0.2*(1 if new_beneficiary else 0)
      # ladder (from architecture §6)
      if R < 0.30: return "observe", R
      if R < 0.55: return "warn", R
      if R < 0.75: return "verify", R
      return "pause", R
  ```
  - Look up the token; expired/missing → `HTTP 400 {"detail": "token expired or unknown"}`.
  - Return `{decision, risk_score, reason_codes, message}` (§3).
- [ ] **2.4 — Message copy.** Use the recommended wording from the playbook:
  *"This call shows signs of urgent payment pressure. The recipient is new. End the call and verify using a
  number you already trust."* (Never "Deepfake detected. Payment blocked.")

**Exit (DoD):** `/analyze` → token → `/payment/decision` returns a ladder decision; expired token → 400.

---

## Phase 3 — File upload + P4 integration (≈45 min)

- [ ] **3.1 — Accept an uploaded file** (so P5 doesn't need a server-side path):
  ```python
  from fastapi import UploadFile, File
  @app.post("/analyze/upload")
  async def analyze_upload(file: UploadFile = File(...)):
      with TemporaryDirectory() as d:
          p = Path(d) / "call.wav"; p.write_bytes(await file.read())
          return _analyze(str(p), input_type="audio")
  ```
  (Refactor the body of `/analyze` into a helper `_analyze(source, input_type, lang)` both endpoints share.)
- [ ] **3.2 — When P4 delivers `risk_engine.py`/`bank_simulator.py`:** replace `_fallback_decide` with
  `from risk_engine import decide`. Keep the fallback behind a flag (`USE_FALLBACK_RISK = True`) so you can
  switch without breaking the demo.
- [ ] **3.3 — `/health` reports real status** for every module (call `semantic_model.transcription_ready()`,
  `analyze_audio` health, and whether `risk_engine` imported).

**Exit (DoD):** upload works; `/health` is honest; fallback swappable for P4's real engine.

---

## Phase 4 — LinuxONE deployment (≈90 min, do this EARLY — it's the differentiator)

- [ ] **4.1 — SSH in and record the environment.**
  ```bash
  ssh -i <key> user@<host>
  uname -m                       # MUST say s390x — screenshot this
  python3 --version
  pip3 --version
  ```
- [ ] **4.2 — Install the backend deps** (pure-Python, so this should just work):
  ```bash
  pip3 install fastapi uvicorn pydantic
  ```
  Do **not** try to install `torch`/`librosa`/`faster-whisper` on s390x yet — that's the ASR path, and it may
  not have wheels. The rule engine + backend are stdlib+fastapi only.
- [ ] **4.3 — Copy the backend files** (scp/rsync): `main.py`, `pipeline.py`, `semantic_model.py`,
  `semantic_config.py`, `token_store.py`, `risk_engine.py`, `audio_authenticity/`.
- [ ] **4.4 — Run it and hit it.**
  ```bash
  nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
  curl http://localhost:8000/health
  curl -X POST http://localhost:8000/analyze -H 'Content-Type: application/json' \
       -d '{"source":"Transfer 50000 now, do not tell anyone","input_type":"text"}'
  ```
- [ ] **4.5 — Capture the evidence** (screenshots): `uname -m`, the running process, the `/health` and
  `/analyze` responses, latency, and `find . -name '*.wav'` → empty (no audio persisted).

**Exit (DoD):** backend runs on s390x; a text `/analyze` returns a real coercion score there; evidence captured.

---

## Phase 5 — Privacy & security pass (≈30 min)

- [ ] **5.1 — No-audio-persistence proof:** `grep -R "open(\|.write(\|to_csv\|np.save\|sf.write" main.py token_store.py pipeline.py` → no matches (mirror what `run_eval.py` already checks for P2).
- [ ] **5.2 — Secrets out of the repo.** Confirm `.env` and `*.pem` are gitignored; add `.env.example` documenting
  any env vars (e.g. `VERIFVOICE_ADAPTER`, `VERIFVOICE_THRESHOLD`).
- [ ] **5.3 — (optional) Rate limit** `/analyze` with a simple per-IP dict + 429.

**Exit (DoD):** no disk writes in the backend path; no secrets tracked; `.env.example` present.

---

## Phase 6 — Evidence handoff (≈30 min)

- [ ] **6.1 — Record real latency** for `/analyze` (text) and `/payment/decision` into `/metrics` (already wired).
- [ ] **6.2 — Write `README.md` Quick start** (how to run locally + on LinuxONE) — P6 will polish.
- [ ] **6.3 — Note what's simulated vs real** for the video: `/payment/decision` is a *simulated* bank action;
  spoof model is *unavailable*; rule engine + fusion + token + LinuxONE are *real*.

**Exit (DoD):** a fresh reviewer can run `uvicorn main:app` and reproduce the golden path.

---

## Phase 7 — Freeze & rehearse (≈30 min)

- [ ] **7.1 — Golden path 3× without edits:** audio → `/analyze` → token → `/payment/decision`, identical
  decision each time.
- [ ] **7.2 — Freeze.** Tag `v1.0-integration`. No new features after this; only demo-blocking fixes.

**Exit (DoD):** golden path stable 3×; tag created.

---

## The critical path (if time runs short, do ONLY these)

1. **1.1 rename** → 2. **2.1–2.3 token + payment** → 3. **4.x LinuxONE** → 4. **7.1 golden path**.

Everything else (upload, CORS polish, rate limiting, P4 swap) is additive. **The demo works without P4's code**
because of the fallback risk engine — do not block on P4.

---

## Coordination cheat-sheet

| With | About | When |
|---|---|---|
| **P4** | `/payment/decision` shape + when `risk_engine.py` is ready (you have a fallback until then) | Phase 0 & 3 |
| **P5** | `/analyze` response fields + CORS + upload endpoint | Phase 1 & 3 |
| **P1** | `VERIFVOICE_ADAPTER` / model readiness for `/health` | Phase 3 |
| **P2** | `transcription_ready()` for `/health`; text path is the LinuxONE-guaranteed path | Phase 4 |
| **P6** | latency numbers + LinuxONE screenshots | Phase 6 |
