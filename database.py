import sqlite3
from contextlib import contextmanager

DB_PATH = "expenses.db"


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                amount          REAL    NOT NULL,
                date            TEXT    NOT NULL,
                description     TEXT    NOT NULL,
                category        TEXT    NOT NULL,
                merchant        TEXT,
                notes           TEXT,
                attachment_path TEXT,
                created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
