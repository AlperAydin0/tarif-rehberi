import sqlite3

from tarif_rehberi import globals_


def get_connection() -> sqlite3.Connection:
    globals_.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(globals_.DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
