"""example_api.py — FastAPI reference for Person 3 (backend).

Shows exactly how to wire Person 2's `semantic_model` into the shared API.
Person 3 owns this file (rename it to `main.py` when you take it over).

Integration points marked "TODO":
  * P1 (audio authenticity) plugs its `audio_model` into /analyze's `spoof_score`.
  * P4 (risk fusion) plugs its `risk_engine` into /payment/decision and fills
    `risk_level` / `token_ttl_seconds`.

Run (from the repo root):
    . .\activate.ps1
    uvicorn example_api:app --reload --port 8000

Try it:
    GET  http://127.0.0.1:8000/health
    POST http://127.0.0.1:8000/analyze   {"source": "Transfer 50000 now, don't tell anyone", "input_type": "text"}
    POST http://127.0.0.1:8000/analyze   {"source": "C:/path/to/call.wav", "input_type": "audio"}
    GET  http://127.0.0.1:8000/metrics
"""

import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import semantic_model  # Person 2's module

# --------------------------------------------------------------------------- #
# Request / response models
# --------------------------------------------------------------------------- #


class AnalyzeRequest(BaseModel):
    source: str = Field(..., description="Transcript text, or a path to an audio file")
    input_type: str = Field("text", description="'text' or 'audio'")
    lang: str = Field("en", description="Semantic-analysis language (e.g. 'en')")


class AnalyzeResponse(BaseModel):
    request_id: str
    # --- Person 2 fields (live) ---
    audio_status: str            # "analyzed" | "insufficient_text" | "unsupported_language"
    coercion_score: float
    reason_codes: list[str]
    signals: dict
    lang: str
    # --- P1 / P4 fields (filled once those modules exist) ---
    spoof_score: float | None = None          # TODO(P1): audio_model.spoof_score
    risk_level: str | None = None             # TODO(P4): risk_engine.risk_level
    token_ttl_seconds: int | None = None      # TODO(P4): token expiry


class PaymentDecisionRequest(BaseModel):
    risk_token: dict = Field(..., description="Unexpired risk token from P4's /analyze")
    amount: float = Field(..., description="Proposed transfer amount (INR)")
    new_beneficiary: bool = Field(False, description="True if payee is new/unusual")


class PaymentDecisionResponse(BaseModel):
    decision: str                              # "observe" | "warn" | "verify" | "pause"
    reason_codes: list[str]
    message: str


# --------------------------------------------------------------------------- #
# App + lifecycle
# --------------------------------------------------------------------------- #

# Lightweight in-memory metrics (reset on restart).
_metrics: dict = {"analyze_requests": 0, "payment_requests": 0,
                  "last_analyze_ms": None, "last_payment_ms": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm up the ASR model so the first /analyze (audio) isn't slow.
    if semantic_model.transcription_ready():
        try:
            semantic_model._get_model()
        except Exception:
            pass  # ASR optional; the text path always works
    yield


app = FastAPI(title="VerifVoice API", version="0.1.0", lifespan=lifespan)


# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #


@app.get("/health")
def health():
    """Server status + model readiness (per the shared contract)."""
    return {
        "status": "ok",
        "semantic_rules": "ready",                       # Person 2 core (always)
        "transcription": ("ready" if semantic_model.transcription_ready() else "unavailable"),
    }


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    """Accept a sample (text or audio) and return the coercion signal."""
    t0 = time.perf_counter()
    result = semantic_model.analyze(req.source, input_type=req.input_type, lang=req.lang)

    _metrics["analyze_requests"] += 1
    _metrics["last_analyze_ms"] = round((time.perf_counter() - t0) * 1000, 2)

    # TODO(P1): result["spoof_score"] = audio_model.analyze_audio(...).spoof_score
    # TODO(P4): compute risk_level + token_ttl_seconds here, or in /payment/decision.
    return AnalyzeResponse(
        request_id=str(uuid.uuid4()),
        audio_status=result["status"],
        coercion_score=result["coercion_score"],
        reason_codes=result["reason_codes"],
        signals=result["signals"],
        lang=result["lang"],
        spoof_score=None,           # TODO(P1)
        risk_level=None,            # TODO(P4)
        token_ttl_seconds=None,     # TODO(P4)
    )


@app.post("/payment/decision", response_model=PaymentDecisionResponse)
def payment_decision(req: PaymentDecisionRequest):
    """Combine an unexpired risk token with transaction context.

    This is P4's domain (risk_engine.py + bank_simulator.py). The stub below
    shows the contract P4 will fill: R = 0.5*C + 0.3*S + 0.2*N.
    """
    t0 = time.perf_counter()
    _metrics["payment_requests"] += 1
    _metrics["last_payment_ms"] = round((time.perf_counter() - t0) * 1000, 2)

    # TODO(P4): replace with a real call to risk_engine / bank_simulator.
    raise HTTPException(
        status_code=501,
        detail="Payment decision is Person 4's module — not wired yet.",
    )


@app.get("/metrics")
def metrics():
    """Timing + request counts (per the shared contract)."""
    return {
        **_metrics,
        "transcription": ("ready" if semantic_model.transcription_ready() else "unavailable"),
    }
