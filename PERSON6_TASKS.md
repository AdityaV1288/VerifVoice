# Person 6 — Testing, Evidence & Presentation · Step-by-Step Tasks

> **Owner:** Person 6. **Goal:** turn the working system into a submittable entry — evidence, slides,
> README, video, and a rehearsed demo.
> **Key point:** most of the *raw* evidence already exists (built during P2/P3). P6's job is **assemble +
> polish**, not rebuild.

---

## Phase 0 — Inventory: what already exists (do this FIRST, don't redo)

| Artifact | Where | Ready? |
|---|---|---|
| Coercion results table (23 fixtures) + safety metrics | `EVALUATION_RESULTS.md` §1–2 | ✅ |
| Limitations (lift into README) | `EVALUATION_RESULTS.md` §6 | ✅ |
| Model/data licenses | `EVALUATION_RESULTS.md` §7 | ✅ |
| 30-second explainer | `EVALUATION_RESULTS.md` §8 | ✅ |
| LinuxONE evidence (s390x, latency, no-audio) | `DEPLOYMENT.md` §3 | ✅ |
| Reproduce commands | `DEPLOYMENT.md` §2 | ✅ |
| Real vs simulated statement | `DEPLOYMENT.md` §4 | ✅ |
| Architecture (mermaid) | `PERSON2_ARCHITECTURE.md`, `PERSON3_ARCHITECTURE.md` | ✅ |
| Machine-readable results | `data/transcripts/results.json` | ✅ |
| 3-min video storyboard + scripts | `VERIFVOICE_MASTER_CONTEXT.md` §16 | ✅ |

**DoD:** you've read the five files above and know exactly what's missing (below).

---

## Phase 1 — Capture the evidence screenshots (≈30 min)

- [ ] **1.1 — LinuxONE screenshots.** On the VM run `~/verifvoice-env/bin/python vm_evidence.py` and
  screenshot: `uname -m` (s390x), the running `uvicorn` process, `/health`, the golden-path output, and the
  `wav files ... NONE` line.
- [ ] **1.2 — Live API screenshots.** `curl` (or `vm_test.py`) and screenshot `/analyze` → token →
  `/payment/decision` with the `verify` decision + reason codes.
- [ ] **1.3 — Evaluation screenshot.** Run `python run_eval.py` locally and screenshot the results table +
  safety metrics (`10/10 coercive`, `7/7 benign`, `0 false positives` → now `11/11` / `7/7`).
- [ ] **1.4 — No-persistence screenshot.** The `DEPLOYMENT.md` §6 finding (only the temporary upload write,
  no permanent `.wav`/transcript).

**DoD:** an `evidence/` folder with 4–6 sanitized screenshots (no secrets, no real phone numbers).

---

## Phase 2 — Architecture diagram + slide deck (≈60 min)

- [ ] **2.1 — One clean architecture diagram.** Turn the mermaid from `PERSON3_ARCHITECTURE.md` §2 into a
  single image (draw.io / Excalidraw / Mermaid render). One diagram, labelled: sample audio → P1 spoof + P2
  coercion → fusion → token → bank policy → dashboard, with "runs on LinuxONE" highlighted.
- [ ] **2.2 — Slide deck (5–6 slides):**
  1. **Problem** — "authentication can succeed while the decision is coerced" + one stat (UPI fraud ₹573cr → ₹1,087cr).
  2. **Insight** — a call and a payment are ambiguous alone, coercive together.
  3. **Demo** — the golden scenario (Meera / son-in-hospital).
  4. **Architecture** — the diagram from 2.1.
  5. **Evidence** — s390x proof, latency, 11/11 & 7/7, no-audio.
  6. **Limitations + ask** — rule-based (not an LLM), spoof model pending, simulated bank action.
- [ ] **2.3 — Closing line** on the last slide: *"Banks authenticate who is paying. VerifVoice helps verify
  whether the decision to pay is being coerced."*

**DoD:** one diagram + one deck; anyone on the team can present it cold.

---

## Phase 3 — Finalize the README (≈45 min)

Follow the playbook's 13-section structure; pull text from `EVALUATION_RESULTS.md` + `DEPLOYMENT.md`:

1. One-sentence value proposition ✅ (exists)
2. 30s demo GIF/video link (add once recorded)
3. Problem + evidence → `EVALUATION_RESULTS.md`
4. Architecture diagram → from Phase 2.1
5. What runs on LinuxONE → `DEPLOYMENT.md` §1
6. Models & datasets → `EVALUATION_RESULTS.md` §7
7. Quick start → `DEPLOYMENT.md` §2 + `ENVIRONMENT.md`
8. API examples → curl the 5 endpoints
9. Privacy & threat model → `PERSON2_ARCHITECTURE.md` / master context §12
10. Evaluation results → `EVALUATION_RESULTS.md` §1–2
11. Accessibility & false-positive tests → §2 + T11/T17/T18/T20 rows
12. Limitations & roadmap → `EVALUATION_RESULTS.md` §6
13. Licenses & acknowledgments → §7
14. Team contributions → add last (each member 1 line)

**DoD:** a fresh reviewer can run + reproduce from the README alone.

---

## Phase 4 — Rehearse + record the 3-min video (≈60 min)

Storyboard (from `VERIFVOICE_MASTER_CONTEXT.md` §16):

| Time | Content |
|---|---|
| 0:00–0:20 | Human problem + one data point: "authentication can succeed while the decision is coerced" |
| 0:20–0:40 | Solution sentence + architecture animation |
| 0:40–1:45 | **Golden live demo** — call risk rises → token → bank step-up |
| 1:45–2:05 | Accessibility counterexample + safe override |
| 2:05–2:35 | **LinuxONE proof** — s390x, running service, real inference, latency, no-audio |
| 2:35–2:50 | Novelty: call + payment *temporal* fusion, not just deepfake detection |
| 2:50–3:00 | Impact + realistic pilot path |

- [ ] **4.1 — Run the golden demo end-to-end 2×** without editing code (audio → analyze → token → decision).
- [ ] **4.2 — Record a backup demo** (screen capture) in case live fails.
- [ ] **4.3 — Record the 3-min video** (screen + optional voiceover). **Hard cap: 3:00.**
- [ ] **4.4 — Verify** the video shows the LinuxONE s390x screen + a real inference request.

**DoD:** golden path stable 2×; a video under 3:00; a backup recording saved.

---

## Phase 5 — Submission QA (≈30 min)

- [ ] **5.1 — Title format** matches the required team-name convention.
- [ ] **5.2 — Video ≤ 3:00** and covers: problem, data, solution, stack, LinuxONE demo.
- [ ] **5.3 — Repo public/reviewable**, links work without private credentials.
- [ ] **5.4 — No secrets in repo** (`git ls-files | grep -E '\.pem|\.key|\.env'` → empty).
- [ ] **5.5 — All open-source links + licenses present** in README.
- [ ] **5.6 — Submit early**, capture the confirmation.

---

## The 16-item final checklist (from the ChatGPT roadmap)

**Working product**
- [ ] End-to-end demo runs
- [ ] Frontend uses real backend responses
- [ ] ≥1 genuine AI inference demonstrated
- [ ] Payment policy changes with call-risk + transaction context

**Technical evidence**
- [ ] Architecture diagram matches implementation
- [ ] Real latency + test results recorded
- [ ] IBM Z deployment + component boundaries verified
- [ ] Dependencies + startup instructions documented

**Privacy & ethics**
- [ ] No persistent raw audio/transcript
- [ ] Token expiry + cleanup tested
- [ ] Uncertain/unsupported inputs handled honestly
- [ ] No automatic permanent transaction blocking

**Presentation & delivery**
- [ ] Slides cover problem/solution/architecture/evidence
- [ ] Known limitations stated
- [ ] Demo rehearsed 2×
- [ ] Backup demo + submissions ready

---

## Coordination cheat-sheet

| With | About |
|---|---|
| **P5** | is the dashboard ready for the demo? if not, demo the API directly (curl/vm_test.py) as fallback |
| **P1** | if their adapter lands before submission, re-run `/analyze` + screenshot a real `spoof_score` |
| **P4** | if their `risk_engine` lands, confirm the ladder outputs match the storyboard |
| **P3 (you covering)** | LinuxONE restart command + SSH tunnel are in `DEPLOYMENT.md` |
| **P2 (you)** | the 30-sec explainer + limitations are ready in `EVALUATION_RESULTS.md` |

---

## Critical path (if time is short)

1. **Phase 1 screenshots** → 2. **Phase 4.3 video** → 3. **Phase 5.6 submit**.

The video + submission are non-negotiable; slides and README polish can be trimmed.
