"""Endpoint REST API SecureNotes."""
from functools import wraps

from flask import Blueprint, current_app, g, jsonify, request

from . import models, security, validators

bp = Blueprint("api", __name__)


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify(error="Token tidak ditemukan."), 401
        user_id = security.verify_token(
            current_app.config["SECRET_KEY"], header[len("Bearer "):]
        )
        if user_id is None:
            return jsonify(error="Token tidak valid atau kedaluwarsa."), 401
        g.user_id = user_id
        return view(*args, **kwargs)

    return wrapper


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username, password = data.get("username"), data.get("password")
    error = validators.validate_username(username) or validators.validate_password(
        password, current_app.config["MIN_PASSWORD_LENGTH"]
    )
    if error:
        return jsonify(error=error), 400
    user_id = models.create_user(g.db, username, security.hash_password(password))
    if user_id is None:
        return jsonify(error="Username sudah dipakai."), 409
    return jsonify(id=user_id, username=username), 201


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    user = models.get_user_by_username(g.db, data.get("username", ""))
    if user is None or not security.verify_password(
        user["password_hash"], data.get("password", "")
    ):
        return jsonify(error="Username atau password salah."), 401
    token = security.create_token(
        current_app.config["SECRET_KEY"],
        user["id"],
        current_app.config["TOKEN_TTL_SECONDS"],
    )
    return jsonify(token=token)


@bp.post("/notes")
@login_required
def add_note():
    data = request.get_json(silent=True) or {}
    title, content = data.get("title"), data.get("content", "")
    error = validators.validate_note(
        title,
        content,
        current_app.config["MAX_TITLE_LENGTH"],
        current_app.config["MAX_CONTENT_LENGTH_CHARS"],
    )
    if error:
        return jsonify(error=error), 400
    note_id = models.create_note(g.db, g.user_id, title.strip(), content)
    return jsonify(id=note_id, title=title.strip()), 201


@bp.get("/notes")
@login_required
def get_notes():
    return jsonify(models.list_notes(g.db, g.user_id, request.args.get("q")))


@bp.get("/notes/<int:note_id>")
@login_required
def read_note(note_id):
    note = models.get_note(g.db, g.user_id, note_id)
    if note is None:
        return jsonify(error="Catatan tidak ditemukan."), 404
    return jsonify(note)


@bp.delete("/notes/<int:note_id>")
@login_required
def remove_note(note_id):
    if not models.delete_note(g.db, g.user_id, note_id):
        return jsonify(error="Catatan tidak ditemukan."), 404
    return "", 204
