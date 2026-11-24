import sqlite3
import config
import threading
from flask import Flask

_thread_local = threading.local()


def init(app: Flask) -> None:
    
    app.config.update(DATABASE=config.DATABASE_PATH)
    database_conn = sqlite3.connect(config.DATABASE_PATH, timeout=10)
    

    try:
        database_conn.execute("PRAGMA journal_mode=WAL")

        database_conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                password_hash TEXT NOT NULL,
                score INTEGER NOT NULL DEFAULT 0
            );
        """)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        database_conn.close()

    # call cleanup_connection() at the end of every http request
    app.teardown_appcontext(cleanup_connection)
    

def get_connection() -> sqlite3.Connection:

    if not hasattr(_thread_local, "conn"):
        _thread_local.conn = sqlite3.connect(config.DATABASE_PATH, timeout=10)
        _thread_local.conn.row_factory = sqlite3.Row

    return _thread_local.conn

# makes sure that there is no pending database query
def cleanup_connection(exception = None) -> None:

    conn = getattr(_thread_local, "conn", None)

    if conn is not None and conn.in_transaction:
        conn.rollback()