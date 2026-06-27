import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt

from config import Config


config = Config()


def _get_secret_key() -> str:
    secret_key = config.secret_key or os.getenv("SECRET_KEY")
    if not secret_key:
        raise ValueError("SECRET_KEY is not configured")
    return secret_key


def _get_algorithm() -> str:
    algorithm = config.algorithem or os.getenv("ALGORITHM") or "HS256"
    if algorithm != "HS256":
        raise ValueError("Only HS256 JWT signing is supported")
    return algorithm


def _get_expiry_minutes() -> int:
    raw_value = (
        config.time_limit
        or os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        or os.getenv("ACCESS_TOKEN-EXPIRE_MINUTS")
        or 30
    )
    try:
        return int(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Access token expiry must be an integer number of minutes") from exc


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode("utf-8")[:72]
    hashed_password_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    algorithm = _get_algorithm()
    expire_at = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=_get_expiry_minutes())
    )
    payload = data.copy()
    payload["exp"] = int(expire_at.timestamp())

    header = {"alg": algorithm, "typ": "JWT"}
    encoded_header = _base64url_encode(
        json.dumps(header, separators=(",", ":")).encode("utf-8")
    )
    encoded_payload = _base64url_encode(
        json.dumps(payload, separators=(",", ":"), default=str).encode("utf-8")
    )
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    signature = hmac.new(
        _get_secret_key().encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()

    return f"{encoded_header}.{encoded_payload}.{_base64url_encode(signature)}"
