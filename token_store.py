"""token_store.py — in-memory risk-token service (Person 3).

A token is a random opaque id mapping to the *scores* produced by /analyze,
with a short time-to-live. It never carries audio or transcript content.

In-memory is sufficient for the demo; Redis would be the production choice.
"""

import time
import uuid

TOKEN_TTL_SECONDS = 120

# token_id -> {"coercion_score", "spoof_score", "reason_codes",
#              "created_at", "expires_at"}
_tokens: dict = {}


def create_token(scores: dict) -> tuple[str, int]:
    """Store scores under a new opaque id. Returns (token_id, ttl_seconds)."""
    now = time.time()
    _purge_expired(now)
    token_id = uuid.uuid4().hex
    _tokens[token_id] = {
        **scores,
        "created_at": now,
        "expires_at": now + TOKEN_TTL_SECONDS,
    }
    return token_id, TOKEN_TTL_SECONDS


def get_token(token_id: str) -> dict | None:
    """Return the stored scores if the token exists and hasn't expired."""
    token = _tokens.get(token_id)
    if token is None:
        return None
    if time.time() > token["expires_at"]:
        _tokens.pop(token_id, None)
        return None
    return token


def _purge_expired(now: float) -> None:
    """Lazily drop expired tokens (called on each create_token)."""
    expired = [k for k, t in _tokens.items() if now > t["expires_at"]]
    for k in expired:
        _tokens.pop(k, None)
