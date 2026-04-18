import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "spendly.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    if conn.execute("SELECT 1 FROM users LIMIT 1").fetchone():
        conn.close()
        return
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = conn.execute(
        "SELECT id FROM users WHERE email = 'demo@spendly.com'"
    ).fetchone()["id"]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?,?,?,?,?)",
        [
            (user_id, 45.00, "Food",          "2026-04-01", "Weekly groceries"),
            (user_id, 12.50, "Transport",     "2026-04-03", "Bus pass top-up"),
            (user_id, 85.00, "Bills",         "2026-04-05", "Electricity bill"),
            (user_id, 30.00, "Health",        "2026-04-08", "Pharmacy"),
            (user_id, 15.00, "Entertainment", "2026-04-10", "Movie tickets"),
            (user_id, 60.00, "Shopping",      "2026-04-12", "New shirt"),
            (user_id, 20.00, "Other",         "2026-04-14", "Miscellaneous"),
            (user_id, 55.00, "Food",          "2026-04-16", "Restaurant dinner"),
        ],
    )
    conn.commit()
    conn.close()
