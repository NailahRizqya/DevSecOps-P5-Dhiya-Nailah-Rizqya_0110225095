"""Utilitas keamanan: hashing password dan token sesi bertanda tangan."""
import hashlib
import hmac
import secrets
import time

from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(password):
    return generate_password_hash(password)


def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)


def _sign(secret_key, payload):
    return hmac.new(secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()


def create_token(secret_key, user_id, ttl_seconds=3600, now=None):
    """Token berformat: user_id.expiry.nonce.signature"""
    now = int(now if now is not None else time.time())
    payload = f"{user_id}.{now + ttl_seconds}.{secrets.token_hex(8)}"
    return f"{payload}.{_sign(secret_key, payload)}"


def verify_token(secret_key, token, now=None):
    """Mengembalikan user_id (int) jika token valid, selain itu None."""
    try:
        user_id, expiry, nonce, signature = token.split(".")
        payload = f"{user_id}.{expiry}.{nonce}"
        if not hmac.compare_digest(signature, _sign(secret_key, payload)):
            return None
        current = int(now if now is not None else time.time())
        if current > int(expiry):
            return None
        return int(user_id)
    except (ValueError, AttributeError):
        return None
