"""Fungsi validasi input pengguna (username, password, judul, isi catatan)."""
import re

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,30}$")


def validate_username(username):
    if not isinstance(username, str) or not USERNAME_PATTERN.match(username):
        return "Username harus 3-30 karakter (huruf, angka, underscore)."
    return None


def validate_password(password, min_length=8):
    if not isinstance(password, str) or len(password) < min_length:
        return f"Password minimal {min_length} karakter."
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return "Password harus mengandung huruf dan angka."
    return None


def validate_note(title, content, max_title=100, max_content=5000):
    if not isinstance(title, str) or not title.strip():
        return "Judul catatan wajib diisi."
    if len(title) > max_title:
        return f"Judul maksimal {max_title} karakter."
    if not isinstance(content, str):
        return "Isi catatan harus berupa teks."
    if len(content) > max_content:
        return f"Isi catatan maksimal {max_content} karakter."
    return None
