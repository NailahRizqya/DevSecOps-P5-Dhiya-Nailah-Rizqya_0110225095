"""Konfigurasi aplikasi. Nilai sensitif dibaca dari environment variable,
bukan ditulis langsung (hardcoded) di dalam source code."""
import os


class Config:
    DATABASE = os.environ.get("SECURENOTES_DB", "securenotes.db")
    SECRET_KEY = os.environ.get("SECURENOTES_SECRET", "")
    MAX_TITLE_LENGTH = 100
    MAX_CONTENT_LENGTH_CHARS = 5000
    MIN_PASSWORD_LENGTH = 8
    TOKEN_TTL_SECONDS = 3600


class TestConfig(Config):
    DATABASE = ":memory:"
    SECRET_KEY = "kunci-khusus-pengujian"
    TESTING = True
