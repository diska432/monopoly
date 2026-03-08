"""
JWT verification for Supabase Auth tokens.
Fetches the JWKS public key from Supabase and verifies ES256-signed JWTs.
Falls back to HS256 with JWT_SECRET for legacy projects.
"""
from __future__ import annotations
import json, time, urllib.request
import jwt
from jwt import PyJWK
from fastapi import HTTPException, Request, WebSocket
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import SUPABASE_URL, SUPABASE_JWT_SECRET

_LOG_PATH = "/Users/iskanderdauletov/Documents/Projects/Monopoly/.cursor/debug-b45bcf.log"

def _dlog(location, message, data=None, hypothesis_id=""):
    # #region agent log
    try:
        entry = {"sessionId":"b45bcf","location":location,"message":message,"data":data or {},"timestamp":int(time.time()*1000),"hypothesisId":hypothesis_id}
        with open(_LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass
    # #endregion

_jwks_cache: dict = {}
_jwks_cache_ts: float = 0
_JWKS_TTL = 3600


def _get_jwks() -> list[dict]:
    """Fetch and cache JWKS keys from Supabase."""
    global _jwks_cache, _jwks_cache_ts
    now = time.time()
    if _jwks_cache and (now - _jwks_cache_ts) < _JWKS_TTL:
        return _jwks_cache.get("keys", [])
    jwks_url = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
    # #region agent log
    _dlog("auth.py:_get_jwks", "Fetching JWKS", {"url": jwks_url}, "H1-fix")
    # #endregion
    try:
        req = urllib.request.Request(jwks_url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        _jwks_cache = data
        _jwks_cache_ts = now
        # #region agent log
        _dlog("auth.py:_get_jwks.ok", "JWKS fetched", {"num_keys": len(data.get("keys", []))}, "H1-fix")
        # #endregion
        return data.get("keys", [])
    except Exception as e:
        # #region agent log
        _dlog("auth.py:_get_jwks.error", "JWKS fetch failed", {"error": str(e)}, "H1-fix")
        # #endregion
        return []


def _find_key_for_token(token: str) -> tuple[str, str | object]:
    """Determine the correct algorithm and key to verify the token.
    Returns (algorithm, key_material)."""
    try:
        header = jwt.get_unverified_header(token)
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Malformed token header.")

    alg = header.get("alg", "")
    kid = header.get("kid", "")

    # #region agent log
    _dlog("auth.py:_find_key", "Token header parsed", {"alg": alg, "kid": kid}, "H1-fix")
    # #endregion

    if alg == "HS256" and SUPABASE_JWT_SECRET:
        return "HS256", SUPABASE_JWT_SECRET

    if alg in ("ES256", "RS256"):
        keys = _get_jwks()
        for jwk_data in keys:
            if jwk_data.get("kid") == kid:
                jwk_obj = PyJWK(jwk_data)
                return alg, jwk_obj.key
        if keys:
            jwk_obj = PyJWK(keys[0])
            return alg, jwk_obj.key

    if SUPABASE_JWT_SECRET:
        return "HS256", SUPABASE_JWT_SECRET

    raise HTTPException(status_code=500, detail="No signing key available for JWT verification.")


class JWTBearer(HTTPBearer):
    """FastAPI dependency that extracts and verifies a Supabase JWT from the Authorization header."""

    async def __call__(self, request: Request) -> dict:
        # #region agent log
        _dlog("auth.py:JWTBearer.__call__", "JWTBearer called", {"auth_header": request.headers.get("authorization", "<missing>")[:80]}, "H1-fix")
        # #endregion
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=401, detail="Missing token.")
        return verify_token(credentials.credentials)


def verify_token(token: str) -> dict:
    """Decode and verify a Supabase JWT. Returns the payload dict or raises."""
    if not SUPABASE_URL and not SUPABASE_JWT_SECRET:
        raise HTTPException(status_code=500, detail="Neither SUPABASE_URL nor JWT secret configured.")

    alg, key = _find_key_for_token(token)

    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=[alg],
            audience="authenticated",
        )
        # #region agent log
        _dlog("auth.py:verify_token.ok", "Token verified OK", {"alg": alg, "sub": payload.get("sub"), "email": payload.get("email")}, "H1-fix")
        # #endregion
        return payload
    except jwt.ExpiredSignatureError:
        # #region agent log
        _dlog("auth.py:verify_token.expired", "Token EXPIRED", {"alg": alg}, "H1-fix")
        # #endregion
        raise HTTPException(status_code=401, detail="Token expired.")
    except jwt.InvalidTokenError as e:
        # #region agent log
        _dlog("auth.py:verify_token.invalid", "Token INVALID", {"alg": alg, "error": str(e)}, "H1-fix")
        # #endregion
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


async def verify_ws_token(websocket: WebSocket, token: str) -> dict | None:
    """Verify a JWT for WebSocket connections. Returns payload or None."""
    if not SUPABASE_URL and not SUPABASE_JWT_SECRET:
        return None
    try:
        alg, key = _find_key_for_token(token)
        payload = jwt.decode(
            token,
            key,
            algorithms=[alg],
            audience="authenticated",
        )
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
    except HTTPException:
        return None
