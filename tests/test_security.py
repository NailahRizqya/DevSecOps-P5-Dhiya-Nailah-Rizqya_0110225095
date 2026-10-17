from app import security

SECRET = "kunci-uji"


def test_password_hash_roundtrip():
    h = security.hash_password("rahasia123")
    assert h != "rahasia123"
    assert security.verify_password(h, "rahasia123")
    assert not security.verify_password(h, "salah")


def test_token_valid():
    token = security.create_token(SECRET, 7, ttl_seconds=60)
    assert security.verify_token(SECRET, token) == 7


def test_token_expired():
    token = security.create_token(SECRET, 7, ttl_seconds=60, now=1000)
    assert security.verify_token(SECRET, token, now=2000) is None


def test_token_tampered_or_garbage():
    token = security.create_token(SECRET, 7)
    assert security.verify_token("kunci-lain", token) is None
    assert security.verify_token(SECRET, "bukan-token") is None
    assert security.verify_token(SECRET, None) is None
