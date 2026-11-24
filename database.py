import sqlite3
import config
from flask import g
from flask import Flask


def init(app: Flask) -> None:
    
    app.config.update(DATABASE=config.DATABASE_PATH)
    database_conn = sqlite3.connect(app.config['DATABASE'], timeout=10)

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

# def get_connection