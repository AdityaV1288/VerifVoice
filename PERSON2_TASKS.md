# Person 2 — Speech & Coercion Detection · Step-by-Step Tasks

> **Owner:** Person 2. **Companion doc:** `PERSON2_ARCHITECTURE.md` (read it first — it defines the interface
> contract and reason codes this task list references).
> **How to use this:** work top-to-bottom. Each task has a **goal**, **context**, **steps**, and a
> **Definition of Done**. The times map to the shared 8–10 hour schedule; if we fall behind, compress the
> *optional* tasks, never the integration/testing tasks.

---

## Phase 0 — Pre-event prep (do NOW, before the window opens)

> Allowed: this is research/planning, not submission code. **Do not** write `semantic_model.py` yet.

- [ ] **0.1 — Share the architecture with the team.** Send `PERSON2_ARCHITECTURE.md` to P3 (backend) and P4
  (fusion). Confirm they accept the §3 interface (the JSON schema + reason-code vocabulary).
  *(Files are ready to send — this check is YOUR action.)*
- [ ] **0.2 — Lock the reason-code vocabulary.** Get P4's sign-off that the 7 codes in §3.2 are the final set
  they'll merge into the risk token. *(Needs P4's actual sign-off — YOUR action.)*
- [x] **0.3 — Draft the keyword lists** (English + Hindi/Hinglish). See §5 below for the starter lists.
- [x] **0.4 — Prepare ~22 labelled example transcripts** (coercive vs benign) → done in
  `PERSON2_TRANSCRIPTS.md` (also the classifier's training data). **No real victim data.**
- [x] **0.5 — ASR path DECIDED:** faster-whisper on the laptop + **scripted-transcript fallback**; P3 calls the
  `analyze(source, input_type=...)` dispatcher. *(Remaining: confirm with P3 whether ASR runs on LinuxONE or
  laptop only.)*
- [x] **0.6 — Verify the environment** works (venv + ffmpeg + all imports — already verified in `ENVIRONMENT.md`).

**Phase 0 exit:** interface frozen, keyword lists drafted, example transcripts ready, environment verified.

---

## Phase 1 — Lock scope (0:00–0:30)

- [ ] **1.1 — Create the repo & your files.** With the team: `git init`, add the shared `.gitignore`. Create an
  empty `semantic_model.py` + `semantic_config.py` stub so the import path is agreed.
- [ ] **1.2 — Confirm the `/analyze` contract with P3.** *(Already DECIDED in architecture §3: P3 calls
  `analyze(source, input_type=...)` and you dispatch internally.)* Just verify P3's code matches.
- [ ] **1.3 — Hard-code a skeleton.** `analyze_transcript()` returns a **fixed** result matching the §3.1 schema
  (e.g. `coercion_score: 0.5, reason_codes: []`). This unblocks P3/P4 immediately.

**Phase 1 exit (Definition of Done):** your stub returns the correct JSON shape, and P3 can call it in their
skeleton even though it's hard-coded.

---

## Phase 2 — Skeleton: build the real rule engine (0:30–1:30)

> **This is the most important hour for Person 2.** The rule engine IS the deliverable. Do it now, while fresh.

- [ ] **2.1 — Implement the 7 signal detectors.** For each category in §3.2, a list of regex patterns + a
  `_count(text, patterns)` matcher. Start with the English lists in §5.
- [ ] **2.2 — Implement `analyze_transcript()`.** Normalize → length/language gate → run detectors → build
  `signals` (0/1) → compute `coercion_score` via the §3.3 formula → emit `reason_codes`.
- [ ] **2.3 — Put keywords + weights in `semantic_config.py`.** No hard-coded lists in the logic; everything
  tunable from one file (P4 will want to adjust weights with you).
- [ ] **2.4 — Smoke test on 3 transcripts.** Hand-check: one benign, one coercive, one emergency-only. Verify the
  scores and codes match §9 expectations.

**Phase 2 exit:** `analyze_transcript()` returns **real** scores/codes computed from rules (not hard-coded), and
your 3 smoke tests pass by hand.

---

## Phase 3 — MVP: wire into the backend + transcription (1:30–3:00)

- [ ] **3.1 — Add `transcribe()`.** Use faster-whisper (tiny model) to turn a sample `.wav` into text. Keep it
  wrapped so a failure returns `""` instead of crashing.
- [ ] **3.2 — Add the `analyze()` dispatcher.** `input_type="audio"` → transcribe → analyze; `"text"` → analyze.
- [ ] **3.3 — Integrate with P3's `/analyze`.** Confirm your result flows through the endpoint and into P4's
  fusion (even if P4's side is still partly stub). **Log latency** at each stage.
- [ ] **3.4 — Scripted-transcript fallback (if ASR is slow).** If faster-whisper is lagging, wire the demo to pass
  pre-written transcripts for the golden scenario. This keeps the demo reliable.

**Phase 3 exit:** one end-to-end scenario runs — audio (or scripted text) → your coercion score → visible in the
backend response → feeds P4.

---

## Phase 4 — IBM Z / LinuxONE (3:00–4:30)

- [ ] **4.1 — Confirm your core runs on LinuxONE.** The rule engine is pure Python stdlib → it runs anywhere.
  With P3, copy `semantic_model.py` + `semantic_config.py` to the VM and run one analysis there.
- [ ] **4.2 — Decide ASR placement.** If faster-whisper installs on s390x (P3 verifies `ctranslate2` wheel), run it
  there too; otherwise keep ASR on the laptop and declare the boundary explicitly in the demo.
- [ ] **4.3 — Record evidence.** Capture: `uname -m` (s390x), the running service, a real inference request, and
  latency. This is the "AI actually runs on LinuxONE" screenshot the judges want.

**Phase 4 exit:** your coercion analysis runs on LinuxONE with visible evidence (or a clearly-labelled boundary if
ASR stays on the laptop).

---

## Phase 5 — Test, fix, add safety (4:30–6:00)

- [ ] **5.1 — Run the 4 core scenarios** (§9 of the architecture) and record real scores/codes.
- [ ] **5.2 — Test the abstention rules:** < 5 words → `insufficient_text`; unsupported language →
  `unsupported_language`; garbled text → low confidence, never "fraud".
- [ ] **5.3 — Verify no transcript is written to disk** (grep for any `.txt`/`.log` output from your module).
- [ ] **5.4 — Fix crashes/edge cases:** empty string, non-ASCII, very long text, punctuation-only.
- [ ] **5.5 — Document + (optionally) mitigate the NEGATION LIMITATION.** A legit line like *"we will NEVER
  ask for your OTP/PIN"* fires `FINANCIAL_INSTRUCTION` (score +0.20, LOW — never blocks alone). Record it in the
  README limitations. *Optional:* add a light negation guard (detect "never/do not ask for X" and suppress the
  financial flag) if time permits — otherwise leave it as a documented tradeoff.

**Phase 5 exit:** reproducible results across scenarios; abstention works; no persistence; no crashes on edge cases;
negation limitation documented.

---

## Phase 6 — Evidence & limitations (6:00–7:00)

- [ ] **6.1 — Fill the results table.** Give Person 6 your measured scores, reason codes, and per-rule latency
  for every scenario.
- [ ] **6.2 — Write the limitations bullets** (goes in the README): rule layer catches high-precision cues (may
  miss paraphrases); declared language coverage; `coercion_score` is a demo heuristic, not a calibrated
  probability; ASR quality affects downstream recall.
- [ ] **6.3 — Document the model/data** if you added the classifier: what it is, what it was trained on, and its
  license.

**Phase 6 exit:** every claim about Person 2's output has a measured number or is explicitly labelled a target.

---

## Phase 7 — Rehearse & freeze (7:00–8:00)

- [ ] **7.1 — Run the golden path 3× without editing code.** Your module must return stable scores (no randomness
  in the rule engine).
- [ ] **7.2 — Freeze.** Stop changing rules/weights unless there's a demo-breaking bug.
- [ ] **7.3 — Be ready to explain** in 30 seconds: what your module does, how the score is computed, and what the
  reason codes mean (judges will ask "why did it flag this?").

**Phase 7 exit:** golden path stable; you can explain the module cold.

---

## Phase 8 — Stretch goals (8:00–10:00, only if core is stable)

- [ ] **8.1 — Hindi/Hinglish keyword lists** (code-switching scenario — high judge value).
- [ ] **8.2 — Compact classifier** (TF-IDF + logistic regression) to boost recall on paraphrased coercion.
- [ ] **8.3 — Richer `signals` for the dashboard** (per-category bar chart, highlight matched words).

> Do NOT add a new dependency that could break the working build.

---

## 5. Starter keyword lists (draft — refine during Phase 2)

These are **high-precision** starters. Tune them live; add Hindi/Hinglish in Phase 8.

```python
URGENCY  = [r"\bact now\b", r"\burgent", r"\bimmediately\b", r"\bright now\b",
            r"\bwithin \d+ minutes\b", r"\bdon'?t delay\b", r"\bhurry\b", r"\bquick\b"]
AUTHORITY = [r"\bpolice\b", r"\bbank\b", r"\brbi\b", r"\bhospital\b", r"\bdoctor\b",
             r"\bofficer\b", r"\bgovernment\b", r"\bcustoms\b", r"\btax department\b",
             r"\bcbi\b", r"\bed\b", r"\bincome tax\b"]
SECRECY = [r"\bdon'?t tell\b", r"\bkeep (it|this) (private|secret|confidential)\b",
           r"\bno one (else )?should know\b", r"\bdon'?t hang up\b", r"\bstay on the line\b"]
VERIF_REFUSAL = [r"\bdon'?t verify\b", r"\btrust me\b", r"\bno need to (check|confirm|call back)\b",
                 r"\bdon'?t call (the )?back\b", r"\bdon'?t (contact|ask)\b"]
FINANCIAL = [r"\btransfer\b", r"\bupi\b", r"\botp\b", r"\bpin\b", r"\bbank account\b",
             r"\bsend money\b", r"\bpay\b", r"\bnetbanking\b", r"\bqr code\b", r"\bpayment\b",
             r"\bamount\b"]
THREAT = [r"\barrest\b", r"\baccount (will be |is )?(blocked|frozen|closed)\b",
          r"\blegal action\b", r"\bfine\b", r"\bgo to jail\b", r"\byour money will be\b",
          r"\bcase filed\b"]
EMERGENCY = [r"\baccident\b", r"\binjured\b", r"\bhospital\b", r"\bsurgery\b", r"\bemergency\b",
             r"\bson\b", r"\bdaughter\b", r"\bhusband\b", r"\bwife\b", r"\bkidnapped\b"]
```

---

## 6. Coordination cheat-sheet (who you talk to, about what)

| With | About | When |
|---|---|---|
| **P3 (backend)** | The `/analyze` call signature; whether they pass text or audio; ASR placement (laptop vs LinuxONE) | Phase 1 & 3 |
| **P4 (fusion)** | The `coercion_score` + `reason_codes` format; the 0.5 weight; tuning thresholds together | Phase 0 & 5 |
| **P5 (frontend)** | The `signals` dict shape for the dashboard "why" breakdown | Phase 3 |
| **P6 (testing/evidence)** | Handing over measured scores, codes, latency, and limitations | Phase 6 |
| **P1 (audio)** | No direct dependency — but agree that P1's `spoof_score` and your `coercion_score` stay **independent** signals (neither gates a payment alone) | Phase 0 |

---

## 7. Time budget summary

| Phase | Person 2's core effort | Must-ship? |
|---|---|---|
| 0 — Pre-event | planning only | yes (prep) |
| 1 — Lock scope | 15 min | yes |
| 2 — Rule engine | **1 hr (the deliverable)** | yes |
| 3 — Wire + ASR | 45–90 min | yes (ASR optional) |
| 4 — LinuxONE | 30 min | yes (core is portable) |
| 5 — Test/safety | 1 hr | yes |
| 6 — Evidence | 30 min | yes |
| 7 — Freeze | 15 min | yes |
| 8 — Stretch | optional | no |

**The one non-negotiable:** Phase 2's rule engine must be done and correct by the end of hour 2. Everything else
is integration and polish.
