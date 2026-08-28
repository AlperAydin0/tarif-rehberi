import sqlite3

import tarif_rehberi.globals as globals


def get_connection() -> sqlite3.Connection:
    globals.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(globals.DATABASE_PATH)
    connection.execute("PRAGMA foreign_key = ON")
    return connection
