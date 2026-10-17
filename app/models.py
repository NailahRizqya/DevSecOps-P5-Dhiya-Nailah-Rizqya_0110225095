"""Lapisan data (SQLite). Seluruh query memakai parameterized statement
untuk mencegah SQL Injection."""
import sqlite3


def get_connection(database):
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
    )
    conn.commit()


def create_user(conn, username, password_hash):
    try:
        cur = conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return None


def get_user_by_username(conn, username):
    return conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()


def create_note(conn, user_id, title, content):
    cur = conn.execute(
        "INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)",
        (user_id, title, content),
    )
    conn.commit()
    return cur.lastrowid


def list_notes(conn, user_id, keyword=None):
    if keyword:
        rows = conn.execute(
            "SELECT * FROM notes WHERE user_id = ? AND title LIKE ? ORDER BY id",
            (user_id, f"%{keyword}%"),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM notes WHERE user_id = ? ORDER BY id", (user_id,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_note(conn, user_id, note_id):
    row = conn.execute(
        "SELECT * FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id)
    ).fetchone()
    return dict(row) if row else None


def delete_note(conn, user_id, note_id):
    cur = conn.execute(
        "DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id)
    )
    conn.commit()
    return cur.rowcount > 0
