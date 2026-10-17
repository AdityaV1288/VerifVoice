# VerifVoice — IBM Z Datathon 2026 · Master Context & Notes

> **This file is the single source of truth for the project.** It captures (a) full project
> context, (b) the project's "behaviours" (non-negotiable constraints & positioning), and
> (c) my own working notes. Read this first every session. Update it when decisions change.

---

## 0. Quick snapshot (read this in 30 seconds)

- **What:** VerifVoice — a consented, privacy-preserving, real-time **coercion-risk signal**
  for payment providers, running AI on **IBM LinuxONE**.
- **One-liner that wins:** *"Banks authenticate **who** is paying. VerifVoice helps verify
  whether the **decision to pay** is being coerced."*
- **Track:** Real-Time AI for Critical Decisions ("detect → decide → respond").
- **Pivot (critical):** Do **NOT** build/pitch a "nationwide wiretap" or "full UPI blocking".
  Build an **opt-in**, selective-analysis system with a **short-lived risk token** and
  **reversible, transaction-specific** friction.
- **Evidence bar:** Real model + decision loop on the **assigned LinuxONE Community Cloud VM**,
  real measured latency, no raw audio persisted. No product-name "architecture theater."
- **Target score:** 37–39/40 (vs 29–31/40 if we keep the old over-scoped framing).
- **Hard rules:** 24h build window (Oct 17–18); 3-min video max; public/reviewable repo;
  flowchart + working prototype; link all open-source resources.

---

## 1. The winning positioning (exact framing to use everywhere)

The strongest positioning, verbatim from the playbook:

> VerifVoice detects coercive voice scams while they happen and passes a
> privacy-preserving, expiring risk signal to the bank so it can step up
> authentication before money leaves. Raw audio is never persisted, synthetic
> speech is never treated as proof of fraud, and the user retains a safe override.

**Narrative (NOT "AI deepfake detector"):**
> A privacy-preserving, accessibility-aware transactional safety layer that detects
> when a payment decision is being coerced by a live call.

**Treat "AI Secured: Innovation Without Exposure" as a design advantage, not a second storyline.**

---

## 2. Competition rules & scorecard (reverse-engineered)

### Mandatory submission
- Public or reviewable repository **+** a video **≤ 3 minutes** covering: problem, supporting
  data, solution, tech stack, and a **demo of the LinuxONE instance + model**.
- **Flowchart** and **working prototype** recommended.
- **All open-source resources linked.**

### 24-hour rule
- All project code must be created during the **official Oct 17–18 hacking window**.
- **Allowed before:** research, dataset exploration, architecture planning, abstract writing,
  environment prep, diagrams, pitch scripts, model/dataset links.
- **Disallowed:** continuation hacks; reusing a prior personal/commercial codebase as the core entry.
- → Strategy: arrive with decisions + test plans + dependency knowledge + diagrams + scripts,
  **but create the repo/implementation during the event.**

### Scorecard (4 categories × 10 pts + separate "AI Innovation Excellence" rubric)

| Criterion | What "exceptional" really requires | VerifVoice evidence |
|---|---|---|
| **Community & theme** (10) | Critical specific need; victim story; authoritative fraud data; call + attempted payment on a synchronized timeline; measurable time-to-warning | One victim story; real fraud stats; "authentication can succeed while the decision is coerced" |
| **Novelty/originality** (10) | More than a generic classifier/dashboard; coherent end-to-end | Cross-domain fusion of **call risk + payment context** |
| **LinuxONE & AI** (10) | AI genuinely executes on LinuxONE; platform capabilities are necessary; evidence is visible & reproducible | s390x instance, running containers/processes, actual model, reproducible commands |
| **Execution & pitch** (10) | Working golden path; professional story; no overclaiming; inside 3 min | Live/recorded end-to-end demo; one architecture diagram; before/after; clear ask + limitations |

**Also:** official guide wants screenshots proving containerization, security, scalability,
compute, and the running model on LinuxONE Community Cloud.

---

## 3. Why the problem matters (authoritative data to cite)

- India digital-payment growth → strong impact story, but we must distinguish
  **fraudulent transactions** from **authorized payments made under deception** (a scam victim
  enters their own correct PIN/OTP — bank checks all pass while the decision is compromised).
- **PwC review:** UPI fraud losses rose **INR 573 crore (FY 2022–23) → INR 1,087 crore (FY 2023–24)**;
  social engineering incl. AI-generated voice calls / deepfake impersonation is a key path.
- **McAfee survey** (7,054 adults, 7 countries incl. 1,010 in India): ~1 in 4 experienced/knew
  someone hit by an AI voice scam — frame as **evidence of exposure**, not official crime incidence.
- **RBI guidance:** regulated entities must already identify suspicious transactional behavior,
  maintain preventive/detective controls, alert customers, update rules, differentiate false positives.
- → We **do not claim** to replace a bank fraud engine. We supply a new **time-sensitive
  coercion-risk signal**.

---

## 4. The timing thesis (our actual novelty)

> **A call and a payment are individually ambiguous, but jointly and temporally they can
> indicate coercion.**

- A synthetic voice alone may be assistive (AAC/TTS user). Words like "hospital" are normal in
  a real emergency. But it becomes suspicious when an **unknown caller uses authority, urgency,
  secrecy, or emergency language** AND the user **immediately attempts an unusual transfer to a
  new/risky payee**.
- **IBM Transactional AI fit:** IBM positions AI on Z as embedding predictive inference directly
  into transactional systems for decisions *while transactions occur*. We say VerifVoice "adds
  call-derived context to a transaction-time decision" — NOT "Telum magically makes audio
  understanding instantaneous."

---

## 5. Market landscape (what we're NOT claiming to be first at)

Do **not** claim to be first at: analyzing live calls, detecting voice deepfakes, or scam warnings.

| Category | What exists | Gap | VerifVoice differentiation |
|---|---|---|---|
| Carrier spam analytics | Airtel network system (velocity, inbound/outbound, SIM/device, geo) | Metadata can't infer real-time coercive intent of a specific conversation | Add **consented content** risk for selected calls, connect to payment-time decision |
| On-device scam warnings | Google Phone app (Pixel), scam-detection beeps | Limited device/geo coverage; warning may not reach bank | Enterprise risk signal + coordinated graduated **bank** action |
| Device-origin verification | Google 2026 fake-call detection (encrypted handshake) | Only saved contacts; can't handle unknown-caller social engineering | Handle unknown/impersonated institutions; fuse call + transaction |
| Contact-center deepfake | Pindrop (IVR/contact-center synthetic/replay/device/behavior) | Enterprise contact center, not a consumer being coerced on a P2P transfer | Consumer call-to-payment risk orchestration + user-protective policy |
| Bank transaction fraud engines | Device/amount/payee/history/behavior scoring; RBI controls | Usually can't see the customer is being pressured on a concurrent call | Supply short-lived **coercion-risk token** (not raw audio) |

---

## 6. Commercial wedge & product boundary

### First deployment
- **Bank-controlled policy pilot** (bank already owns the transaction decision + auth experience).
- Telco / call-analysis service should **never independently freeze an account** — it only issues
  an expiring risk assertion (reason codes + confidence); the bank applies policy.
- Other wedges: telco+bank joint pilot; digital-banking app consuming a call-risk token; eldercare/contact-center.

### VerifVoice owns exactly 4 things
1. Streaming call-risk inference.
2. Multi-signal fusion + uncertainty handling.
3. Privacy-minimized, expiring risk-token generation.
4. Policy simulator showing how a bank combines the token with transaction context.

### VerifVoice does NOT claim to own
Telecom lawful interception · NPCI network control · final bank authorization ·
law-enforcement reporting · fraud reimbursement. (Those are integrations/governance, not a
24-hour student feature.)

---

## 7. NON-NEGOTIABLE PIVOTS — the "behaviours" of this project

These are the project's personality/constraints. Violating any of them regresses the score.

1. **Opt-in selective analysis, not universal interception.**
   - Replace "network-level interceptor" → *"opt-in real-time scam-protection service integrated
     at a SIP/IMS media edge or demonstrated through an enterprise VoIP testbed."*
2. **SIPREC (RFC 7866) or an honest VoIP testbed, not passive packet mirroring.**
   - SIPREC = explicit, selective, metadata-aware, supports recording notifications. Use a
     SIPREC-capable SBC/SIP proxy/PBX. For the hackathon: **Asterisk / FreeSWITCH / minimal
     SIP-WebRTC bridge** to fork a demo call.
3. **Multi-signal decisioning, not "85% synthetic means fraud."**
   - Synthetic speech is a **supporting feature, not a prerequisite**. Many scams use real human
     voices, replay, voice conversion, or mixed audio.
   - `call_risk = f(synthetic_likelihood, coercion_intent, urgency, authority_claim, secrecy,
     payment_instruction, caller_reputation, model_quality, persistence)`
   - `decision_risk = g(call_risk, payment_amount, new_beneficiary, beneficiary_reputation,
     device_risk, customer_baseline, time_since_call)`
4. **Transaction-specific, reversible friction, not an account freeze / phone-number blacklist.**
   - The bank evaluates an individual **payment session**; a victim must not lose access to all
     P2P payments because a model disliked a call.
   - Use an **expiring risk token**:
     ```json
     {
       "risk_level": "high",
       "reason_codes": ["COERCIVE_URGENCY", "NEW_PAYEE_REQUEST", "SYNTHETIC_AUDIO_SUPPORT"],
       "confidence": 0.91,
       "model_quality": 0.84,
       "issued_at": "...",
       "expires_at": "...",
       "audio_retained": false
     }
     ```
   - Do NOT transmit caller/receiver phone numbers (transmit a pseudonymous subject reference).
5. **Real LinuxONE inference evidence, not product-name architecture theater.**
   - Truthful line: *"The prototype runs on LinuxONE Community Cloud. The production architecture
     is designed for Secure Execution and Telum-accelerated inference; the demo labels which
     controls are implemented and which are deployment targets."*
   - Validate, don't assert: export models to ONNX → run ONNX checker → attempt zDLC → record
     whether execution is CPU / partially-accelerated / accelerated → keep a known-compatible fallback.
6. **No Kafka/C++/Go micro-optimization before the golden path works.**
   - Kafka is only for durable score/audit events (NOT raw PCM). Decoded PCM stays in an
     in-memory ring buffer. Python is the correct orchestration language for 24h.
   - Don't chase sub-millisecond broker latency while waiting 6s for semantic context.
7. **Accessibility, language uncertainty, replay, and emergency payments as demonstrated tests.**
   - AAC/TTS user scenario must NOT trigger a payment pause.
   - Low-quality / unsupported-language input must **abstain**, not claim fraud.
8. **Secure Execution ≠ "privacy solved."** Technical isolation is only one control among consent,
   notice, purpose limitation, minimization, retention limits, auditability, user rights, governance.
9. **Two clocks for timing:**
   - **Acoustic clock:** score every 1–2s over an overlapping 4–6s audio ring buffer.
   - **Semantic clock:** partial transcript every 2s, classify intent over accumulated 6–12s context.

---

## 8. Recommended architecture

### Product definition
Consented real-time coercion-risk signal for payment providers. Listens only within an enrolled
protection session, keeps audio in volatile memory, produces an expiring risk token, lets the bank
combine it with transaction context for proportionate intervention.

### End-to-end flow (11 steps)
1. **Enrollment & notice** — user enables Scam Shield; clear notice about live call analysis;
   test call begins with audible/visible disclosure.
2. **Selective media fork** — SIPREC-capable SBC/PBX forks enrolled call's two audio legs to the
   VerifVoice Session Recording Server.
3. **Secure media termination** — SRTP terminated inside protected workload; decoded to mono PCM;
   stored only in bounded in-memory ring buffers.
4. **Quality gate** — audio quality assessed; low quality reduces confidence rather than forcing classification.
5. **Acoustic inference** — short-utterance anti-spoofing model → window-level synthetic/replay/manipulation scores, smoothed + model-quality metadata.
6. **Streaming transcription** — lightweight ASR → partial text; semantic model extracts urgency,
   authority claims, secrecy, threats, emergency narratives, credential/payment requests.
7. **Call-risk fusion** — compact calibrated model combines acoustic + semantic + quality +
   persistence + optional metadata → low/medium/high + human-readable reason codes.
8. **Risk-token service** — only pseudonymous subject ref, level, confidence, reason codes,
   timestamps, retention statement leave the protected zone. Raw audio/full transcript stay transient.
9. **Transaction correlation** — simulated bank starts a payment; combines unexpired token with
   amount, beneficiary novelty, prior relationship, device state, timing.
10. **Graduated response** — warn → out-of-band verify → short reversible hold → stronger auth.
    Never permanently freeze from the call signal alone.
11. **Audit & deletion** — show the buffer returning to zero; store only minimal event telemetry
    needed to explain the decision.

### Reference components (hackathon → production)

| Layer | Hackathon | Production |
|---|---|---|
| Call source | Asterisk/FreeSWITCH or browser WebRTC test call | Telco SBC/IMS media gateway w/ selective SIPREC |
| Media ingest | SIP/RTP receiver or WebSocket PCM bridge (if SIP costs too much time) | SIPREC SRS with SRTP, separate legs, admission control |
| Buffer | In-memory circular buffer | Per-session bounded encrypted memory with zeroization + backpressure |
| Acoustic model | Small pre-trained AASIST-family baseline or compact CNN; fallback MFCC model | Ensemble trained on multilingual, codec, replay, current TTS attacks |
| ASR | Whisper-tiny **only if** it installs & meets measured latency; else lightweight recognizer or scripted-transcript adapter | Streaming multilingual ASR w/ partial hypotheses + domain vocab |
| Intent model | Compact keyword + classifier hybrid | Multilingual transformer with calibrated intent + uncertainty |
| Fusion | Logistic regression / XGBoost / small MLP | Calibrated ensemble w/ drift monitoring, policy thresholds |
| Serving | Python/FastAPI control plane; direct in-process inference | Triton/zDLC or MLz serving, gRPC/REST, autoscaling |
| Event stream | In-memory events; optional Kafka for non-critical telemetry | Kafka for durable scores/monitoring — not raw audio |
| Bank integration | Simulated Payment Decision API + UI | Bank-owned risk orchestration + strong auth |
| Security | TLS, no disk audio, scoped identifiers, secrets outside repo | Secure Execution, HSM keys, remote attestation, strict IAM, audited policies |

---

## 9. Models & data strategy

### Three-signal model (present as THREE signals, not "two models + threshold")
1. **Audio authenticity** — synthetic / replayed / converted / manipulated?
2. **Coercion intent** — urgency, fear, secrecy, authority, directing a financial action?
3. **Transaction context** — payment to new/risky beneficiary during the danger window?

### Acoustic model order of operations
1. Attempt lightweight **AASIST / AASIST2-family** inference baseline on LinuxONE.
2. Fallback: MFCC/log-mel CNN or shallow classifier that genuinely runs on LinuxONE.
3. Test: short clips, telephone compression, replay (speaker→mic), noise, ≥1 unseen TTS generator.
4. Report **EER / ROC-AUC** for the experiment, but optimize the **product threshold around
   false interventions**, not balanced accuracy.

> Do NOT claim "99% accuracy." Judges trust an honest limitations slide with real measurements.
> AASIST's strong ASVspoof 2019 LA numbers are in-domain, not telephone-world proof.

### Semantic model choice
- Whisper-tiny is a sensible experiment but natively audio-oriented; must maintain rolling context,
  reuse the loaded model, avoid reloading per 2s chunk.
- **Preferred 24h hybrid:** ASR → partial text → **rule layer** catches high-precision concepts
  (`transfer, UPI, OTP, PIN, screen sharing, arrest, police, hospital, accident, secrecy,
  "do not hang up", "act now"`) → compact classifier scores combos + persistence → reason codes.
- **Generative AI is post-hoc only** (nice warning text), never in the critical path.

### Dataset plan (public, clearly separated train/val/adversarial)
- **ASVspoof 2019 LA** — baseline reproducibility.
- **ASVspoof 2021 DF** (or codec/channel-shifted set) — harder evaluation.
- **MLAAD** (or other multilingual synthetic-speech set, license permitting).
- Synthetic scripted scenarios: payment, human scam, voice clone, replayed clip, AAC/TTS user,
  noisy rural call, code-switching, failed transcription.
- **List every dataset + model license in the repo.** No copyrighted call recordings / real victim audio.

---

## 10. Evaluation matrix (scenarios to run & prove)

| Test | Expected safe behavior | Metric |
|---|---|---|
| Synthetic coercive call + new payee | High call risk; bank adds warning/hold/step-up | Time to alert; true positive |
| Human scammer + coercive intent | True positive WITHOUT deepfake dependency | Detection without synthetic score |
| AAC/TTS user buying from known merchant | No transaction restriction; authenticity offset by benign intent/context | Accessibility false-intervention rate |
| Genuine family emergency + known payee | Warning may appear but payment proceeds, minimal friction | False-intervention outcome |
| Genuine emergency + new personal QR | Strong warning + reversible step-up; safe override available | Override completion time |
| Replayed deepfake over speaker | Confidence may drop; system explains uncertainty | Replay robustness |
| Hindi/English code-switching | Detect core coercion/payment cues or fail safely | Intent recall by language |
| Bad network / packet loss | "Insufficient signal" rather than "fraud" | Abstention correctness |
| Benign synthetic customer-service bot | Synthetic score alone causes no bank action | False positive |
| Scam after call ends | Short-lived token still correlates with payment | Detection within expiry window |

---

## 11. Payment intervention policy (the ladder)

Four levels — step-up is fine; it's only "too complex" if every feature fires at once.

| Level | Conditions | Action |
|---|---|---|
| **0: Observe** | Low risk / inadequate evidence | No interruption; minimal telemetry |
| **1: Warn** | Suspicious language/caller context, no payment | In-call notice: *"This caller is requesting an urgent financial action. Verify using a known number."* |
| **2: Verify** | High call risk + payment to new/unusual payee | App shows reasons, asks user to end call, starts out-of-band verification |
| **3: Pause** | High combined risk + high-value/new beneficiary/device anomaly | Short reversible hold; biometric re-auth; bank callback or optional trusted-person confirmation |

- Trusted contact must be **opt-in, amount-sensitive, privacy-minimized** — message: *"Kumar is
  attempting a high-risk new-payee transfer; please check in"* (NOT the transcript or medical details).
- **Emergency payments:** don't hard-code "P2M allowed / P2P blocked" (rural providers use personal
  QR; fraudsters abuse merchant accounts). Use contextual policy. Override = end/pause call +
  device biometric + acknowledge named beneficiary + amount.
- The intervention **creates time to think**, doesn't decide whether the emergency is real. Never
  claim it "saves someone's life" or guarantees prevention.

### User message design
- ❌ Bad: "Deepfake detected. Payment blocked."
- ✅ Good: *"This call shows signs of urgent payment pressure. The recipient is new. End the call
  and verify using a number you already trust. Your payment is paused briefly; you can review or
  continue securely."*

---

## 12. Privacy & security

### Threat model (name these in the report/pitch)
Scammer (live speech / TTS / voice conversion / replay / mixed) · malicious/compromised infra admin ·
attacker stealing model outputs or linking pseudonymous IDs · coercer instructing victim to ignore
warnings · DoS flooding media ingestion · model evasion (noise, codecs, short utterances, adversarial
audio, code words, unsupported languages) · insider misuse of transcripts/metadata.

### Required controls
Explicit enrollment + notice + easy off switch · selective SIPREC only for enrolled sessions ·
encryption in transit + protected termination · no audio files / raw transcript in durable logs ·
bounded buffers + deletion after scoring · purpose-specific reason codes (not general surveillance) ·
RBAC + secret management + rate limits + audit events · model version/threshold/quality/action trace
for contestability · user override + appeal path · monitoring false interventions by language/disability/channel.

### Data lifecycle (the demo must visibly show all 6)
1. Ring-buffer size increases during the test call.
2. Inference consumes the rolling window.
3. No `.wav` or transcript file is written.
4. Call termination clears the buffer.
5. Bank receives only the risk token.
6. Audit record has model + action metadata but not call content.

→ This turns "we value privacy" into **observable technical behavior**.

---

## 13. LinuxONE implementation

### What must actually run on the assigned LinuxONE Community Cloud VM (minimum)
- Risk fusion model.
- At least one genuine AI inference component.
- FastAPI decision API.
- Risk-token generation.
- Payment policy simulator (or its decision endpoint).
- Metrics endpoint (measured latency + resource usage).
- *(Ideally also acoustic model or semantic classifier.)*

Media capture + UI may run elsewhere if network constraints require — but the video must make the
boundary explicit.

### zDLC path (recommended experiment)
1. Export compact model → ONNX. 2. Validate static input shape + operators. 3. Pull official zDLC
image from IBM Z/LinuxONE registry. 4. Compile for the **actual detected architecture**. 5. Run test
vectors through original + compiled. 6. Compare tolerance + measure p50/p95 latency. 7. Enable
accelerator targeting only if the assigned hardware exposes it AND compilation succeeds.
> Never paste an example `-march=z17 --maccel=NNPA` command without verifying it runs on the
> allocated system. Acceleration builds require compatible hardware.

### Dependency strategy
**Pre-event checklist (non-code):** Python version on VM · Podman/Docker? · IBM registry creds? ·
do PyTorch/ONNX-Runtime/librosa/soundfile/FFmpeg/ASR have s390x builds? · can we install system
packages? · which ports can be exposed? · is zDLC available to the account? · is the accelerator visible?

**During-event install priority:** 1. FastAPI + fusion model → 2. ONNX/zDLC compact model →
3. acoustic model → 4. ASR → 5. optional Kafka/extra services.
→ Always have a valid LinuxONE AI demo even if a sophisticated library fails.

### Languages/services
Python (orchestration, features, models, FastAPI) · Java (optional, not MVP) · Go (production only,
not 24h) · gRPC (optional between mature services; REST is fine) · Kafka (optional, score/audit only).

---

## 14. MVP scope

**Must build:** consented test call (live/streamed audio) · rolling audio windows + transient memory ·
one real acoustic/authenticity signal · one semantic/coercion signal · fusion score with reason codes +
uncertainty · expiring risk token · simulated bank payment flow with known/new beneficiary · graduated
warning + step-up · safe override · LinuxONE-hosted AI/decision API with visible evidence · measured
end-to-end latency + ≥6 scenario tests.

**Should build:** Hindi/English code-switching scenario · AAC/TTS accessibility scenario · replay
attack scenario · dashboard (per-stage latency + score timeline) · ONNX/zDLC compiled model if compatible ·
containerized deployment.

**Do NOT build:** real UPI/NPCI · real telecom interception · full lawful-intercept interfaces · national
blacklist · automated police reporting · production Kafka cluster · large LLM in critical path · permanent
audio storage · polished multi-page app before the core loop works · claims of nationwide capacity /
perfect accuracy / zero false positives / legal-compliance certification.

---

## 15. Twenty-four-hour plan

### Pre-event (maximize WITHOUT writing submission code)
Finalize architecture, risk policy, threat model, data dictionary, API contract, test cases, 3-min script ·
identify public datasets/licenses/checkpoints/exact download links · attend "How to Win" (Sept 18) +
LinuxONE setup (Oct 16) sessions · prepare a **blank** evidence checklist (not a prebuilt codebase) ·
decide fallback model + fallback call-ingestion method.

### Event schedule (hour-by-hour gates)

| Hours | Objective | Exit gate |
|---|---|---|
| 0–1 | Create repo, assign owners, confirm LinuxONE access, freeze MVP | Everyone can push; VM reachable; scope signed off |
| 1–4 | Vertical skeleton: sample call/audio → LinuxONE endpoint → risk token → bank simulator | One hard-coded golden path end-to-end |
| 4–8 | Integrate acoustic + semantic signals; log per-stage latency | Both signals produce real outputs on test audio |
| 8–11 | Fusion, reason codes, quality gate, token expiry | Human scam & synthetic-benign separate correctly |
| 11–14 | Bank policy ladder, override, known/new payee context | No global account block; emergency flow usable |
| 14–16 | Transient-buffer proof, security controls, container evidence | No raw audio persisted; deployment reproducible |
| 16–18 | Scenario matrix + capture metrics | Results table complete; limitations written |
| 18–20 | Feature freeze; fix only demo blockers; backups | Golden path succeeds 3× consecutively |
| 20–22 | Record 3-min video + LinuxONE proof | Video under limit, understandable w/o notes |
| 22–23 | Finalize README, licenses, architecture, setup commands, contributions | Fresh reviewer can reproduce core path |
| 23–24 | Validate links/title/access, submit early | Submission confirmation captured |

> **Feature freeze at hour 18 is essential.**

### Team roles — OPERATIVE (6-person, from the ChatGPT roadmap; use THIS mapping)
1. **Person 1 — AI & audio authenticity** → `audio_model.py` (score + quality/status field).
   Pretrained audio anti-spoofing model; test genuine vs synthetic/replayed; document limitations.
   *Fallback:* if no compatible model runs, use semantic classifier as primary + label audio as future module.
2. **Person 2 — Speech & coercion detection** → `semantic_model.py` (scores + reason codes).
   Transcript-analysis pipeline: urgency, secrecy, authority claims, verification refusal, financial
   instructions. Start with transparent rules; add compact classifier if time.
3. **Person 3 — IBM Z deployment & backend** → FastAPI service, API contracts, integration.
   Sets up LinuxONE, defines interfaces first, coordinates everyone. `/health`, `/analyze`,
   `/payment/decision`, `/metrics`.
4. **Person 4 — Risk fusion, privacy & bank simulation** → `risk_engine.py` + `bank_simulator.py`.
   Expiring tokens, new-beneficiary detection, proportionate actions, deletion checks.
5. **Person 5 — Frontend & live demo** → clean dashboard (sample select → Analyze → scores → reasons
   → transaction → bank response). Streamlit or HTML/JS; real backend, not a mockup.
6. **Person 6 — Testing, evidence & presentation** → representative samples, evaluation, latency,
   architecture diagram + slides, rehearse demo, backup recording.

> **CRITICAL coordination rule:** Person 3 defines the API contract IMMEDIATELY; Persons 1, 2, 4, 5
> build against it. Nobody waits until the end to integrate.
>
> (The playbook's 5-role split — Systems / ML / NLP-risk / Backend-security / Product-demo — maps onto
> the same work; the 6-role version above is the assignment the team is actually following.)

---

## 16. Demo design

### Golden scenario (one run, every subsystem touched)
Meera gets a call claiming her son was injured → caller uses an **AI-cloned "son" voice**, then a human
"hospital administrator" directs payment → acoustic detector raises synthetic/replay suspicion **but does
not act alone** → intent model detects emergency pressure + secrecy + transfer request → fusion score rises
low→high over several windows → LinuxONE correlates the short-lived call token with new-payee + timing →
bank pauses the specific transfer, asks her to end the call, offers known-channel callback → she verifies
the emergency is false and cancels → dashboard shows audio deletion + minimal audit event.
**Then** a 5-second accessibility counterexample: AAC user pays a previously-used pharmacy account —
audio is synthetic, but benign intent + trusted context prevent intervention.

### Three-minute storyboard

| Time | Content |
|---|---|
| 0:00–0:20 | Human problem + one authoritative data point; "authentication can succeed while the decision is coerced" |
| 0:20–0:40 | Solution sentence + simple architecture animation |
| 0:40–1:45 | Golden live demo: call risk rises → token reaches bank → payment-specific step-up |
| 1:45–2:05 | Accessibility counterexample + safe override |
| 2:05–2:35 | LinuxONE proof: s390x, running service/container, model inference, latency, no-audio-retention |
| 2:35–2:50 | Novelty: call + payment temporal fusion, not just deepfake detection |
| 2:50–3:00 | Impact statement + realistic pilot path |

### Opening script (verbatim)
> "A scam victim can enter the correct UPI PIN and still be defrauded, because the bank
> authenticates the user but cannot see that an urgent phone call is coercing the decision.
> VerifVoice is a consented, privacy-preserving signal running on IBM LinuxONE that detects live
> coercion patterns and lets the bank add proportionate friction before money leaves."

### IBM Z script (verbatim)
> "This is not a laptop mock-up. The scoring and payment decision endpoint run on our LinuxONE
> Community Cloud instance. Here is the s390x environment, the model service, a real inference
> request, measured latency, and the transient buffer returning to zero. In production, the same
> design targets Secure Execution and compatible Telum acceleration; the demo makes no claim for
> controls the assigned environment does not expose."

---

## 17. Metrics that matter + acceptance thresholds

**Report actual measurements:** time from first coercive phrase → first warning · bank request → policy
response · acoustic p50/p95 · semantic update latency · end-to-end p50/p95 · peak memory/CPU on LinuxONE ·
true-positive count (scam) · false-intervention count (benign/AAC/emergency) · abstention count (low quality) ·
% calls with raw audio files created (target 0%) · token expiry + deletion verification.

**Internal acceptance targets (not market claims):**
- Warning within **8s** of decisive coercion evidence.
- Payment policy response within **500ms** of the transaction request.
- No permanent block from call score alone.
- No raw audio / full transcript on disk.
- All high-risk actions carry ≥2 independent signals.
- AAC benign scenario does NOT trigger a pause.
- Low-quality audio can abstain.
- Golden path succeeds 3× consecutively before recording.

> Don't invent load-test scale. If the VM handles 5 concurrent streams, report 5; explain horizontal
> scaling as **architecture**, not benchmark.

---

## 18. Likely judge questions + answers

- **"Isn't analyzing calls illegal?"** → Opt-in, disclosed test calls. Architecture separates media
  processing from bank decisioning; technical isolation ≠ legal basis; production needs jurisdiction-specific
  telecom/banking/data-protection review.
- **"Why can't the bank's existing fraud model do this?"** → Transaction models know amount/device/beneficiary
  but can't see concurrent-call coercion. We supply a short-lived signal; the bank stays the decision owner.
- **"Why IBM Z?"** → Co-locate protected predictive inference with high-volume transaction decisions, avoid an
  external AI round trip, reduce sensitive-data exposure. IBM's Transactional AI positioning + LinuxONE
  isolation/enterprise serving.
- **"What if the voice is human?"** → Synthetic is only one feature. Coercive language, payment instructions,
  context, and timing can still raise risk.
- **"What about an AAC user?"** → Synthetic-alone can't block; benign intent + trusted transaction signals +
  abstention + AAC as a first-class safety test.
- **"Real hospital using a personal QR?"** → No permanent denial; short reversible transaction-specific pause +
  safe out-of-band override; known payees/verified institutions get lower friction.
- **"Regional languages?"** → Declared limited language set + code-switching. Acoustic is only partly
  language-agnostic; semantic coverage measured per language; unsupported → abstain/warn, not auto-restrict.
- **"Millions of calls?"** → We don't claim that benchmark. Production = opt-in/selective activation,
  metadata-first filtering, horizontal media workers, compact models, LinuxONE serving.
- **"Why not run everything on the phone?"** → On-device is a valid signal source, but coverage/device/capability/
  bank integration vary; we demonstrate an enterprise control plane consuming telco+device+payment signals.
- **"What stops the scammer coaching the override?"** → High-risk override = leave/pause call, re-authenticate
  in-app, review named beneficiary + amount, optional callback/trusted-person confirmation — time + independent
  channel, not a dismissible banner.

---

## 19. Predicted scoring

| Concept | Community | Novelty | Technical/LinuxONE | Execution | Total |
|---|---|---|---|---|---|
| **Current (over-scoped "wiretap")** | 9 | 9 | 6 | 5–7 | **29–31/40** |
| **Recommended (pivoted)** | 10 | 9–10 | 9–10 | 9 | **37–39/40** |

---

## 20. Validation checkpoints (pass/fail gates)

1. **Problem fit** — pass statement: *"Authorized push-payment victims authenticate themselves correctly,
   so VerifVoice adds a live coercion signal before the bank releases a risky new-payee transfer."*
2. **Theme fit** — detect → decide → respond in real time (not a post-call report).
3. **IBM necessity** — removing LinuxONE weakens security/latency/transaction-integration; ≥1 model really runs there.
4. **Safety** — synthetic alone can't block; low-quality/unsupported can abstain; AAC + emergency tested;
   holds reversible + transaction-specific; user gets a reason + safe next step.
5. **Demo completeness** — one run shows audio ingestion → model outputs → fusion → token → correlation →
   intervention → override/cancel → deletion.
6. **Evidence** — screenshots/logs prove s390x, model version/output, container/service state, real latency,
   no raw-audio retention, repo reproducibility.
7. **Submission** — correct title format; video ≤3 min; links work without private creds; open-source links +
   licenses present; uploaded before deadline.

---

## 21. README structure (13 sections)

1. One-sentence value proposition. 2. 30s demo GIF/video link. 3. Problem + evidence. 4. Architecture diagram.
5. What runs on LinuxONE. 6. Models + datasets. 7. Quick start. 8. API examples. 9. Privacy + threat model.
10. Evaluation results. 11. Accessibility + false-positive tests. 12. Limitations + production roadmap.
13. Open-source licenses + acknowledgments. 14. Team contributions.
+ an `evidence/` folder (sanitized screenshots, benchmark output, model-compat notes, test results).
**Do NOT commit secrets, real phone numbers, raw calls, or LinuxONE credentials.**

---

## 22. Abstract + final build decision

**Recommended abstract:** VerifVoice is a privacy-preserving real-time AI system that helps banks stop
voice-coercion fraud — analyzing transient audio for synthetic/replayed speech and coercive financial intent
on IBM LinuxONE, emitting only a short-lived pseudonymous risk token (never stored audio) to a bank risk engine.
When a high-risk call coincides with an unusual transfer to a new beneficiary, the bank applies proportionate
friction (warning / out-of-band verification / reversible pause). It fuses call intent, audio authenticity,
signal quality, and transaction context — protecting assistive users — and demonstrates a complete
detect-decide-respond loop, LinuxONE-hosted inference, reason-coded decisions, and verifiable data deletion.

**Final build decision:** Proceed under Real-Time AI track with the pivots in §7. *"This narrower system is
not less ambitious. It is more credible, safer, easier to build, better aligned with the rubric, and more
likely to survive expert questioning."*

---

## 23. References (from playbook, to keep handy)

1. Participant Guidebook_IBM Z Datathon 2026.pdf
2. IBM Z Datathon 2026 Official Rules & Guidelines.pdf
3. PwC — Combating payments fraud in India's digital payments landscape
4. McAfee — AI Voice Scams on the Rise (1 in 4 adults)
5. RBI — Digital Payment Security Controls directions
6. AI on IBM Z (Transactional AI)
7. Machine Learning for IBM z/OS (MLz)
8. Airtel AI-powered spam detection (GSMA)
9. Google Phone scam detection
10. Android fake call detection (device handshake)
11. Pindrop (deepfake detection, NIST-evaluated)
12. DPDP Act 2023 (consent requirements)
13. Compliances & Consents in Recording Digital Interactions
14. Telecom Act — interception prohibition
15. RFC 7866 — Session Recording Protocol (SIPREC)
16. RFC 7866 — SIPREC (guide books)
17. Audio Deepfake Detection at the First Greeting: "Hi!"
18. (same as 17)
19. Replay Attacks Against Audio Deepfake Detection (arXiv)
20. IBM Secure Execution for Linux
21. ONNX and the IBM Deep Learning Compiler (zDLC)
22. IBM/zDLC GitHub (ONNX-MLIR → shared libraries)
23. SIPREC module — OpenSIPS (RFC 7245)
24. Triton Inference Server on IBM Z 101 (s390x)
25. AI Toolkit for IBM Z and LinuxONE (zDLC auto-quantization)
26. clovaai/aasist (GitHub, official PyTorch)
27. MTUCI/AASIST3 (Hugging Face)
28. Pindrop Pulse (18 patents)
29. openai/whisper-tiny (Hugging Face)
30. ASVspoof (research institutes)
31. lab260/AASIST3 (Hugging Face)
32. AI/ML on IBM Z and LinuxONE: Hands-on Experience (YouTube)
33. Accelerated AI Processor on LinuxONE (IBM)
34. IBM Z Datathon 2026 | StarHacks

---

## 24. MY OWN NOTES (agent working notes — update as decisions evolve)

### What's locked vs open
- **LOCKED:** positioning (§1), pivots (§7), architecture (§8), ladder (§11), acceptance thresholds (§17),
  narrative ("authenticate who vs verify whether the decision is coerced").
- **OPEN / to confirm:** which of Person 1 / Person 2 the user will build (deep plans ready for both),
  exact LinuxONE allocation (verify Oct 16), final model choice (AASIST vs fallback CNN vs MFCC),
  ASR choice (Whisper-tiny vs scripted adapter).

### Person 1 — AI & audio authenticity (audio_model.py)
- **Role (resolved):** build/integrate a pretrained audio anti-spoofing model; test genuine + synthetic/replayed
  samples; record scores; document limitations. Deliverable `audio_model.py` returns a score + quality/status field.
- **Fallback (agreed):** if no compatible model runs, use the semantic classifier as primary and demo audio
  authenticity as a clearly-labeled future module.
- **Deep plan:** see `PERSON1_AUDIO_MODEL_PLAN.md`.

### Person 2 — Speech & coercion detection (semantic_model.py)  ← **WE ARE PERSON 2**
- **Role (resolved):** transcript-analysis pipeline. Detect urgency, secrecy, authority claims, verification
  refusal, financial instructions. Start with transparent rules; add compact classifier if time. Deliverable
  `semantic_model.py` returns scores + reason codes.
- **Build reference (code scaffolding):** `PERSON2_SEMANTIC_MODEL_PLAN.md`.
- **Architecture (share with group):** `PERSON2_ARCHITECTURE.md`.
- **Step-by-step tasks (share with group):** `PERSON2_TASKS.md`.

### Shared integration contract (all roles)
- Risk token JSON shape (§7.4) is the **interface** between call-risk and bank.
- Reason-code vocabulary: `COERCIVE_URGENCY`, `NEW_PAYEE_REQUEST`, `SYNTHETIC_AUDIO_SUPPORT`, etc.
- Fusion is a 3-signal model (audio authenticity + coercion intent + transaction context).
- Every stage logs latency → dashboard + metrics endpoint.

### Risks / mitigations to remember
- s390x wheel availability (PyTorch/ONNX-Runtime/librosa/soundfile/FFmpeg) → test early, keep MFCC fallback.
- No accelerator visible → still fine: CPU inference + honest "accelerator is a deployment target."
- Whisper-tiny too heavy → use scripted-transcript adapter or lightweight recognizer; rule layer does the work.
- Time: feature freeze at hour 18; golden path 3× before recording.

### Things I should verify or ask the user
- [x] Role mapping — RESOLVED: P1 = audio authenticity (`audio_model.py`), P2 = coercion detection (`semantic_model.py`).
- [x] Which role to build for — **Person 2 confirmed** (speech & coercion detection). Deep plans + architecture + tasks ready.
- [x] ChatGPT chat content — captured in §25 below.
- [ ] Team size confirmed = **six people** (ChatGPT roadmap) — note the playbook assumed five; reconcile with the real team.
- [ ] LinuxONE VM facts (Python version, Docker/Podman, registry creds, ports, zDLC, accelerator) — confirm Oct 16.

### If I help write code tomorrow, the order is:
1. Repo + README skeleton + `.gitignore` (secrets).
2. Vertical skeleton (hard-coded golden path): audio → endpoint → token → bank sim.
3. Add real acoustic + semantic signals.
4. Fusion + reason codes + expiry.
5. Policy ladder + override + known/new payee.
6. Buffer-zeroization proof + container evidence.
7. Scenario matrix + metrics + limitations.
8. 3-min video + submission QA.

---

## 25. ChatGPT roadmap — OPERATIONAL DETAILS (from the share chat, verbatim-condensed)

> This is the practical execution layer. The playbook (§1–23) gives positioning/evidence; THIS section
> gives the exact interfaces, formulas, thresholds, schedule, and test suite the team codes against.
> Where the two differ, note it explicitly (see "Discrepancies" below).

### 25.1 The simplified demo (what we actually show)
- **Input = a short uploaded/selected sample recording**, processed **in memory**. **Live phone integration
  is NOT required** for the hackathon. (This de-risks the whole build vs the playbook's SIPREC fork.)
- Finish line: judge selects a sample → clicks **Analyze** → sees model output + why it's risky → triggers a
  simulated bank response. *That beats a polished UI with a dead backend.*

### 25.2 Simplified architecture (6 boxes)
`Sample call audio (uploaded file, no interception)` → `Audio processing + speech analysis (real inference,
quality checks, coercion signals)` → `Risk fusion service — LinuxONE (scores, thresholds, reason codes,
uncertainty)` → `Expiring risk-token API — LinuxONE (pseudonymous ID, level, expiry, reasons)` →
`Bank policy simulator (amount + beneficiary history → warn/verify/pause)` → `Dashboard + audit evidence
(explain decision; show deletion + perf metrics)`.

### 25.3 Tech stack (small & practical)
| Component | Recommendation |
|---|---|
| Backend | Python + FastAPI |
| Frontend | Streamlit (speed) or existing HTML/JS |
| Audio analysis | Pretrained **ONNX** model if compatible; else a lightweight supported classifier |
| Speech analysis | Lightweight recognizer + rules, or a compact classifier |
| Risk fusion | Python scoring function with calibrated thresholds |
| Token expiry | **In-memory TTL** for demo; Redis optional |
| Metrics | Python timing + basic CPU/memory |
| Hosting | LinuxONE Community Cloud VM (or the assigned environment) |

> **s390x constraint:** a model/dependency that installs on a laptop may NOT run on the assigned server.
> Test early. Don't burn half the day compiling a large model — if it fails, switch to fallback + document.

### 25.4 Risk formula (use the SIMPLE one)
- Original design: `R = 0.40·S + 0.35·C + 0.25·(1−M) + B`
  (S = synthetic/replay score, C = coercion score, M = speaker-match if available, B = pressure/refusal signal).
- **Day-one simplification (use this):** `R = 0.5·C + 0.3·S + 0.2·N`
  where **N = new beneficiary (0 or 1)**. Normalize inputs to 0–1, clamp, keep weights configurable.
- **Synthetic speech must never alone trigger high-risk.** Low-quality / model-unavailable / unsupported-language
  → report uncertainty, don't manufacture confidence.

### 25.5 Policy thresholds (configurable)
| R range | Response |
|---|---|
| < 0.30 | No additional friction |
| 0.30 – 0.55 | Monitor / mild caution |
| 0.55 – 0.75 | Prompt user to verify |
| > 0.75 **with financial intent** | Strong warning + out-of-band verification (brief hold = *simulated* policy action) |

> Never imply we actually paused a real bank transfer.

### 25.6 API contract (Person 3 owns this — define FIRST)
| Endpoint | Purpose |
|---|---|
| `GET /health` | Server status + model readiness |
| `POST /analyze` | Accept a sample (or reference to a locally stored sample) → return risk signals |
| `POST /payment/decision` | Combine an unexpired risk token with transaction context |
| `GET /metrics` | Timing, request counts, model status |

Illustrative `/analyze` response:
```json
{
  "request_id": "demo-001",
  "audio_status": "analyzed",
  "spoof_score": 0.82,
  "coercion_score": 0.91,
  "risk_level": "high",
  "reason_codes": ["COERCIVE_URGENCY", "FINANCIAL_INSTRUCTION"],
  "token_ttl_seconds": 120
}
```
- **If audio model is NOT implemented, return an explicit `unavailable` status — never invent a `spoof_score`.**
- Token = random opaque identifier + short expiry + server-side storage (or signed token with enforced expiry).
  **Never include transcript, phone number, or audio in the token.** In-memory storage + explicit cleanup is fine.

### 25.7 Test suite (4 cases minimum — record real numbers)
| Test | Scenario | Expected |
|---|---|---|
| **A** | Normal conversation, known beneficiary | Low risk, no friction |
| **B** | Urgent payment demand, new beneficiary (discourages verification) | Elevated risk + reason codes + OOB verification prompt |
| **C** | Synthetic/replayed voice, **no** coercion | Authenticity warning only (if supported) — **no auto high-risk decision** |
| **D** | Genuine emergency / assistive speech | Considers context + uncertainty; never equates synthetic with fraud; preserves override |

Also measure: **inference latency** (model only) · **end-to-end latency** (request → policy response) ·
**model evaluation** (precision/recall/false-positives if enough samples) · **privacy** (any audio/transcript on
disk? buffers cleared?). **No fabricated accuracy %.**

### 25.8 Hour-by-hour schedule (8–10h usable; compress optional, NOT integration/testing)
| Phase | Time | Objective | Exit condition |
|---|---|---|---|
| 1. Lock scope | 0:00–0:30 | Agree demo flow; assign 6 roles; create repo + board; **P3 writes API contract + tests LinuxONE** | Everyone knows what they build; no one waiting on architecture |
| 2. Skeleton | 0:30–1:30 | Backend `/health` + `/analyze`; frontend Analyze button; AI team runs 1 real inference; risk team makes deterministic scoring; slides started | Request reaches backend and returns a result (even with placeholders) |
| 3. MVP | 1:30–3:00 | Integrate 1 AI component; add coercion signals; fusion + reason codes; bank simulator; frontend shows real API results | One end-to-end scenario: sample → bank response |
| 4. IBM Z | 3:00–4:30 | Backend + risk engine on LinuxONE; check model/packages on s390x; test token API/expiry/policy; measure latency separately | Can demonstrate which parts run on IBM Z, with evidence |
| 5. Test/privacy | 4:30–6:00 | Benign/suspicious/ambiguous runs; new-beneficiary affects policy; low-quality → uncertainty; no audio/transcript persisted; fix crashes | Reproducible results; ≥1 failure handled gracefully |
| 6. Evidence | 6:00–7:00 | Screenshots; results table; architecture diagram; report latency + eval; label simulated/unimplemented controls | Every claim has evidence or is labeled a target |
| 7. Rehearse/freeze | 7:00–8:00 | Full demo 2× without edits; prerecorded backup; verify submission format/deadlines; freeze features | Any member can explain problem/architecture/results/limitations |
| 8. Stretch | 8:00–10:00 | Only if stable: polish UI, 2nd model, more samples, token-expiry visualization, privacy lifecycle view | Don't add a dependency that breaks the working build |

### 25.9 Presentation structure (4–5 min if rules allow; adjust to the real limit)
Problem (30s) → Insight (30s: linked-in-time > independent) → **Live demo (90–120s: benign + suspicious,
reason codes, bank response)** → Technical architecture (45s: model, fusion, token expiry, API, what's on
LinuxONE) → Evidence + limitations (30–45s: real latency, tests, privacy, false-positive risks, boundaries).
**Closing line:** *"Banks authenticate who is paying. VerifVoice helps verify whether the decision to pay is
being coerced."*

### 25.10 Final submission checklist (16 items, 4 groups)
- **Working product:** end-to-end demo runs · frontend uses real backend · ≥1 genuine AI inference · policy
  changes with call-risk + transaction context.
- **Technical evidence:** architecture diagram matches implementation · real latency + test results · IBM Z
  deployment + component boundaries verified · dependencies + startup instructions documented.
- **Privacy/ethics:** no persistent raw audio/transcript · token expiry + cleanup tested · uncertain/unsupported
  handled honestly · no automatic permanent block.
- **Presentation/delivery:** slides cover problem/solution/architecture/evidence · limitations stated · demo
  rehearsed 2× · backup demo + submissions ready.

### 25.11 DISCREPANCIES to reconcile (playbook vs ChatGPT chat)
1. **Team size:** playbook says 5 roles; ChatGPT says **6**. → Team is following the 6-person split (§15).
2. **Video vs presentation:** playbook = **3-min video cap** (official); ChatGPT = 4–5 min live presentation.
   → **3-min is the hard submission rule; the live pitch may be longer.** Confirm with the official rules.
3. **Call ingestion:** playbook wants SIPREC/live fork; ChatGPT = **uploaded sample, no live phone**. →
   **Default to uploaded sample** (satisfies the demo); treat SIPREC as a "production direction" slide.
4. **Build window:** playbook = full 24h (Oct 17–18); ChatGPT = ~8–10h usable. → Plan for the tighter 8–10h
   of real coding; use the 24h plan's "pre-event prep" to compress.
