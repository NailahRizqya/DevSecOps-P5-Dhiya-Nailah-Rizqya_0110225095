"""Application factory SecureNotes."""
import sqlite3

from flask import Flask, g, jsonify

from . import models
from .config import Config


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    if not app.config["SECRET_KEY"]:
        raise RuntimeError(
            "SECURENOTES_SECRET belum di-set. Isi environment variable tersebut."
        )

    # Untuk database in-memory, satu koneksi dipakai bersama agar data bertahan.
    shared = None
    if app.config["DATABASE"] == ":memory:":
        shared = sqlite3.connect(":memory:", check_same_thread=False)
        shared.row_factory = sqlite3.Row
        models.init_db(shared)
    else:
        with models.get_connection(app.config["DATABASE"]) as boot:
            models.init_db(boot)

    @app.before_request
    def open_db():
        g.db = shared or models.get_connection(app.config["DATABASE"])

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None and db is not shared:
            db.close()

    @app.errorhandler(404)
    def not_found(_e):
        return jsonify(error="Endpoint tidak ditemukan."), 404

    from .routes import bp

    app.register_blueprint(bp)
    return app
