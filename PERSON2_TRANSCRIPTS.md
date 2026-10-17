# Person 2 — Labelled Example Transcripts (Phase 0 prep)

> **Owner:** Person 2. **Status:** prep data, NOT submission code.
> **How to use:** Phase 2 smoke tests → Phase 5 formal tests → Phase 8 classifier training data. During the
> event, convert these to test fixtures (JSON/CSV) under `data/transcripts/`. **No real victim data — all of
> these are invented.**
>
> **Scoring key** (from the architecture §3.3): each of 6 signals contributes if it fires —
> urgency 0.25 · financial 0.20 · threat 0.20 · verif-refusal 0.15 · authority 0.10 · secrecy 0.10.
> `emergency_narrative` is reported but NOT scored. Bands: **low** < 0.30 · **moderate** 0.30–0.55 ·
> **high** ≥ 0.70.

---

## Coercive (scam) examples

### T01 — "Son in hospital" · GOLDEN SCENARIO
**Label:** coercive · **Scenario:** A (demo golden path)
> "Hello, is this Meera? This is Dr. Sharma calling from City Hospital. Your son Rahul has been in a serious
> accident and needs emergency surgery right now. We need you to transfer ₹50,000 immediately to book the
> operation theatre. Please do not tell anyone about this, it is very delicate. And do not try to call the
> hospital to verify — the lines are down. If we don't operate in the next hour, he may not survive."

**Signals that fire:** urgency, authority_claim, financial_instruction, secrecy_pressure, verification_refusal, threat, emergency_narrative
**Expected reason codes:** `COERCIVE_URGENCY`, `AUTHORITY_CLAIM`, `FINANCIAL_INSTRUCTION`, `SECRECY_PRESSURE`, `VERIFICATION_REFUSAL`, `THREAT`, `EMERGENCY_NARRATIVE`
**Expected band:** HIGH (≈ 1.00) · **Why:** every coercive signal present; the "don't verify" + "don't tell anyone" + "may not survive" are the tell.

### T02 — "Police / legal settlement" 
**Label:** coercive · **Scenario:** B
> "This is Inspector Verma from the Cyber Crime department. Your Aadhaar number has been linked to a money
> laundering case. You will be arrested within 24 hours unless you transfer ₹25,000 to the official settlement
> account right now. Do not call the police station to verify, and do not tell your family — this is confidential."

**Signals:** urgency, authority_claim, financial_instruction, secrecy_pressure, verification_refusal, threat
**Reason codes:** `COERCIVE_URGENCY`, `AUTHORITY_CLAIM`, `FINANCIAL_INSTRUCTION`, `SECRECY_PRESSURE`, `VERIFICATION_REFUSAL`, `THREAT`
**Band:** HIGH (≈ 0.90)

### T03 — "Bank OTP / account blocked"
**Label:** coercive · **Scenario:** B
> "Dear customer, your bank account will be blocked in the next 10 minutes due to suspicious activity. To stop
> this, share the OTP that has just been sent to your mobile and transfer your balance to the safe account
> immediately. Do not contact the bank, this line is secure."

**Signals:** urgency, authority_claim, financial_instruction, secrecy_pressure, verification_refusal, threat
**Reason codes:** `COERCIVE_URGENCY`, `AUTHORITY_CLAIM`, `FINANCIAL_INSTRUCTION`, `SECRECY_PRESSURE`, `VERIFICATION_REFUSAL`, `THREAT`
**Band:** HIGH (≈ 0.90)

### T04 — "Customs / parcel held"
**Label:** coercive · **Scenario:** B
> "This is a call from Customs. A parcel addressed to you has been seized containing illegal items. Pay a
> ₹15,000 clearance fee right now via UPI or a case will be filed against you."

**Signals:** urgency, authority_claim, financial_instruction, threat
**Reason codes:** `COERCIVE_URGENCY`, `AUTHORITY_CLAIM`, `FINANCIAL_INSTRUCTION`, `THREAT`
**Band:** HIGH (≈ 0.75)

### T05 — "Lottery / prize fee"
**Label:** coercive · **Scenario:** B
> "Congratulations! You have won ₹10 lakh in the KBC lottery. To receive the prize, you must pay a processing
> fee of ₹5,000 today. Send it now to claim your winnings before the offer expires."

**Signals:** urgency, financial_instruction
**Reason codes:** `COERCIVE_URGENCY`, `FINANCIAL_INSTRUCTION`
**Band:** MODERATE (≈ 0.45) · **Why:** no threat/authority/refusal — shows why the score is graded, not binary.

### T06 — "Kidnapping-style threat"
**Label:** coercive · **Scenario:** B (max-threat)
> "We have your daughter. Do not call anyone. Do not tell the police. Transfer ₹2 lakh now or you will never
> see her again."

**Signals:** urgency, financial_instruction, secrecy_pressure, verification_refusal, threat, emergency_narrative
**Reason codes:** `COERCIVE_URGENCY`, `FINANCIAL_INSTRUCTION`, `SECRECY_PRESSURE`, `VERIFICATION_REFUSAL`, `THREAT`, `EMERGENCY_NARRATIVE`
**Band:** HIGH (≈ 1.00)

### T07 — "Electricity disconnection"
**Label:** coercive · **Scenario:** B
> "Your electricity bill is overdue. Your power will be disconnected in 30 minutes. Pay ₹4,000 immediately by
> UPI to this number to avoid disconnection."

**Signals:** urgency, authority_claim, financial_instruction, threat
**Reason codes:** `COERCIVE_URGENCY`, `AUTHORITY_CLAIM`, `FINANCIAL_INSTRUCTION`, `THREAT`
**Band:** HIGH (≈ 0.75)

### T08 — "Hindi/Hinglish code-switching"
**Label:** coercive · **Scenario:** B (code-switching)
> "Namaste, main police station se bol raha hoon. Aapka account block ho jayega turant. Jaldi se OTP bata do aur
> ₹30,000 transfer karo. Kisi ko mat batana, yeh secret hai. Abhi karo!"

**Signals:** urgency, authority_claim, financial_instruction, secrecy_pressure, threat
**Reason codes:** `COERCIVE_URGENCY`, `AUTHORITY_CLAIM`, `FINANCIAL_INSTRUCTION`, `SECRECY_PRESSURE`, `THREAT`
**Band:** HIGH (≈ 0.85) · **Why:** Phase 8 — requires Hindi/Hinglish keywords. Until added, this may score lower
or abstain; that is the expected, honest behaviour.

---

## Benign (safe) examples

### T09 — Family catch-up
**Label:** benign · **Scenario:** A
> "Hi beta, how are you? How was school today? Did you have lunch? We were just thinking about you and wanted
> to say hello."

**Signals:** none
**Reason codes:** (none)
**Band:** LOW (0.00)

### T10 — Genuine emergency, no money asked
**Label:** benign · **Scenario:** D
> "Hello? Uncle, dad had a small accident and we are at the hospital. The doctors say he is stable. Can you
> please come to the hospital? We are waiting near the emergency ward."

**Signals:** emergency_narrative (only)
**Reason codes:** `EMERGENCY_NARRATIVE`
**Band:** LOW (0.00) · **Why:** emergency alone is NOT scored — this is the key safety behaviour.

### T11 — AAC/TTS user paying a known pharmacy
**Label:** benign (synthetic voice) · **Scenario:** C + accessibility
> "Hello, this is my regular order. Please pay my usual amount to the pharmacy for this month's medicine as
> always. Thank you."

**Signals:** financial_instruction (mild — "pay"), possibly none
**Reason codes:** (none, or `FINANCIAL_INSTRUCTION` only)
**Band:** LOW (< 0.30) · **Why:** synthetic voice is P1's signal, not P2's; language here is benign and the
payee is known — must NOT trigger a pause.

### T12 — Legit bank fraud-alert call (no info requested)
**Label:** benign · **Scenario:** A
> "This is your bank's security team. We noticed a login from a new device. If this was not you, please open our
> official app to review it. We will never ask for your OTP or PIN. You can call the number on your card."

**Signals:** authority_claim (bank), financial_instruction (mild — "review")
**Reason codes:** `AUTHORITY_CLAIM`
**Band:** LOW (≈ 0.10) · **Why:** authority alone, with explicit "we will never ask for OTP/PIN" and "call the
number on your card" — the opposite of a scam.

### T13 — Friend splitting a bill
**Label:** benign · **Scenario:** A
> "Hey, that dinner was ₹1,200 total. Can you send me your ₹600 share whenever you get a chance? No rush."

**Signals:** financial_instruction (mild — "send")
**Reason codes:** (none, or `FINANCIAL_INSTRUCTION` only)
**Band:** LOW (< 0.30) · **Why:** "no rush" negates urgency; known beneficiary.

### T14 — Appointment reminder
**Label:** benign · **Scenario:** A
> "Hello, this is a reminder that you have a dental appointment tomorrow at 11 AM. Please confirm if you will be
> attending."

**Signals:** none
**Reason codes:** (none)
**Band:** LOW (0.00)

### T15 — Known merchant payment
**Label:** benign · **Scenario:** A
> "Hi, the grocery delivery is here. The total is ₹850. Please pay via UPI as usual. Thanks!"

**Signals:** financial_instruction (mild)
**Reason codes:** (none, or `FINANCIAL_INSTRUCTION` only)
**Band:** LOW (< 0.30) · **Why:** known payee + routine — P4's `N=0` keeps this low even if C is mildly elevated.

---

## Ambiguous / edge-case examples

### T16 — Insufficient text
**Label:** ambiguous · **Scenario:** edge (abstention)
> "Hello?"

**Signals:** (gate trips) · **Reason codes:** (none)
**Band:** LOW → `status: "insufficient_text"` · **Why:** < 5 words → abstain, never "fraud."

### T17 — Unsupported / garbled language
**Label:** ambiguous · **Scenario:** edge (abstention)
> "…[unintelligible audio / a language the model doesn't support]…"

**Signals:** (gate trips) · **Reason codes:** (none)
**Band:** LOW → `status: "unsupported_language"` · **Why:** abstain, never auto-restrict.

### T18 — Genuine emergency + new payee (the override case)
**Label:** ambiguous (real emergency) · **Scenario:** D
> "It's me. There's been a bad accident and I need you to send ₹40,000 to this new account right away for the
> ambulance and admission. I'll explain everything, just please hurry."

**Signals:** urgency, financial_instruction, emergency_narrative
**Reason codes:** `COERCIVE_URGENCY`, `FINANCIAL_INSTRUCTION`, `EMERGENCY_NARRATIVE`
**Band:** MODERATE (≈ 0.45) · **Why:** no threat/secrecy/refusal — score is moderate, and P4's policy must keep a
**safe override** available. This is the case that proves we don't block real emergencies.

### T19 — Paraphrased coercion (no trigger words)
**Label:** ambiguous (recall gap) · **Scenario:** edge (limitations)
> "I need you to move some money to a different account for me. It has to happen fast, and I'd rather you didn't
> mention it to anyone just yet."

**Signals:** financial_instruction (mild — "move money"), secrecy_pressure ("didn't mention it to anyone")
**Reason codes:** `FINANCIAL_INSTRUCTION`, `SECRECY_PRESSURE`
**Band:** LOW–MODERATE (≈ 0.30) · **Why:** paraphrased, no high-precision trigger words → the rule layer's known
**recall limitation**. Document this; it's why the classifier (Phase 8) and P1's signal exist.

### T20 — Urgent legitimate hospital bill to known payee
**Label:** ambiguous (legitimate) · **Scenario:** D
> "The hospital needs the ₹25,000 admission deposit now or they will move your father to a different ward.
> Please pay the hospital's account quickly."

**Signals:** urgency, financial_instruction, authority_claim (hospital), emergency_narrative
**Reason codes:** `COERCIVE_URGENCY`, `FINANCIAL_INSTRUCTION`, `AUTHORITY_CLAIM`, `EMERGENCY_NARRATIVE`
**Band:** MODERATE (≈ 0.55) · **Why:** known payee (`N=0`) + no secrecy/refusal → P4 should apply friction but
NOT block; override preserved.

### T21 — Romance/investment scam
**Label:** coercive · **Scenario:** B
> "My love, I found an amazing investment. Transfer ₹50,000 today and we will double it. Don't tell your family
> yet — it's a surprise. Trust me, this is a once-in-a-lifetime chance. Act now."

**Signals:** urgency, financial_instruction, secrecy_pressure, verification_refusal
**Reason codes:** `COERCIVE_URGENCY`, `FINANCIAL_INSTRUCTION`, `SECRECY_PRESSURE`, `VERIFICATION_REFUSAL`
**Band:** HIGH (≈ 0.70)

### T22 — Tech-support remote-access scam
**Label:** coercive · **Scenario:** B
> "I'm calling from Microsoft technical support. Your computer has a virus and your bank details are exposed. I
> need you to download the remote-access app right now and share the OTP. Do not restart your computer and do
> not tell your bank. If you delay, your account will be emptied."

**Signals:** urgency, authority_claim, financial_instruction, secrecy_pressure, verification_refusal, threat
**Reason codes:** `COERCIVE_URGENCY`, `AUTHORITY_CLAIM`, `FINANCIAL_INSTRUCTION`, `SECRECY_PRESSURE`, `VERIFICATION_REFUSAL`, `THREAT`
**Band:** HIGH (≈ 0.90)

---

## Summary table (quick reference)

| ID | Label | Scenario | Expected band | Key reason codes |
|---|---|---|---|---|
| T01 | coercive | A (golden) | HIGH | URGENCY, AUTHORITY, FINANCIAL, SECRECY, REFUSAL, THREAT, EMERGENCY |
| T02 | coercive | B | HIGH | URGENCY, AUTHORITY, FINANCIAL, SECRECY, REFUSAL, THREAT |
| T03 | coercive | B | HIGH | URGENCY, AUTHORITY, FINANCIAL, SECRECY, REFUSAL, THREAT |
| T04 | coercive | B | HIGH | URGENCY, AUTHORITY, FINANCIAL, THREAT |
| T05 | coercive | B | MODERATE | URGENCY, FINANCIAL |
| T06 | coercive | B | HIGH | URGENCY, FINANCIAL, SECRECY, REFUSAL, THREAT, EMERGENCY |
| T07 | coercive | B | HIGH | URGENCY, AUTHORITY, FINANCIAL, THREAT |
| T08 | coercive | B (code-switch) | HIGH* | URGENCY, AUTHORITY, FINANCIAL, SECRECY, THREAT |
| T09 | benign | A | LOW | — |
| T10 | benign | D | LOW | EMERGENCY only |
| T11 | benign | C + accessibility | LOW | — |
| T12 | benign | A | LOW | AUTHORITY only |
| T13 | benign | A | LOW | — |
| T14 | benign | A | LOW | — |
| T15 | benign | A | LOW | FINANCIAL only |
| T16 | ambiguous | edge | LOW (abstain) | — |
| T17 | ambiguous | edge | LOW (abstain) | — |
| T18 | ambiguous | D (override) | MODERATE | URGENCY, FINANCIAL, EMERGENCY |
| T19 | ambiguous | edge (recall gap) | LOW–MOD | FINANCIAL, SECRECY |
| T20 | ambiguous | D (legit) | MODERATE | URGENCY, FINANCIAL, AUTHORITY, EMERGENCY |
| T21 | coercive | B | HIGH | URGENCY, FINANCIAL, SECRECY, REFUSAL |
| T22 | coercive | B | HIGH | URGENCY, AUTHORITY, FINANCIAL, SECRECY, REFUSAL, THREAT |

\* T08 scores HIGH only after Hindi/Hinglish keywords are added (Phase 8); before that it abstains or scores low.

---

## Notes for the team

- **P4:** these bands assume your `N` (new beneficiary) is set per scenario. The *combined* risk `R` may differ
  from `coercion_score` alone — that's expected and correct.
- **P6:** use the "Expected reason codes" as the ground truth when recording test results; a mismatch is a bug
  in the rule engine, not a test failure.
- **P1:** nothing here depends on your `spoof_score` — P2's signal must work identically for human and synthetic
  voices (T11 proves it).
- All transcripts are fictional. No real people, numbers, or victim recordings.
