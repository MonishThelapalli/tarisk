"""Database utilities with SQLite fallback.

This module prefers a sqlite database (local file) when DB_CONNECTION_STRING
is not explicitly provided or points to sqlite. If a non-sqlite DSN is used,
it will attempt to use pyodbc as before.

We keep the same function names to minimize changes elsewhere.
"""

import threading
import time
from typing import Any, List, Dict

from config import settings

_thread_local = threading.local()


def _is_sqlite(conn_str: str) -> bool:
    return settings.is_sqlite_connection(conn_str)


def get_connection():
    """Return a DB-API connection object.

    - If DB_CONNECTION_STRING is sqlite, use sqlite3 (standard library).
    - Otherwise attempt to use pyodbc with the provided connection string.
    """
    conn_str = settings.DB_CONNECTION_STRING

    if _is_sqlite(conn_str):
        # Ensure directory exists
        db_path = conn_str.replace("sqlite:///", "").lstrip("/")
        import os
        os.makedirs(os.path.dirname(db_path) or os.getcwd(), exist_ok=True)

        if not hasattr(_thread_local, "connection") or _thread_local.connection is None:
            import sqlite3
            _thread_local.connection = sqlite3.connect(db_path, check_same_thread=False)
            # Return rows as dictionaries
            _thread_local.connection.row_factory = sqlite3.Row
        return _thread_local.connection

    # Non-sqlite: attempt to use pyodbc and similar pooling as before
    try:
        import pyodbc
    except Exception as e:
        raise ImportError("pyodbc is required for non-sqlite databases") from e

    if not hasattr(_thread_local, "connection") or _thread_local.connection is None:
        _thread_local.connection = pyodbc.connect(conn_str)
    return _thread_local.connection


def execute_query_with_retry(query: str, params: Any = None, max_retries: int = 3) -> Any:
    """Execute a SQL query with retries and return results.

    For SELECT queries, returns list[dict]. For others returns True on success.
    """
    retry_count = 0
    last_error = None

    while retry_count < max_retries:
        try:
            conn = get_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            sql = query.strip().lower()
            if sql.startswith("select"):
                rows = cursor.fetchall()
                # Convert to list of dicts
                if hasattr(rows, "keys"):
                    # sqlite3 Row support
                    result = [dict(row) for row in rows]
                else:
                    cols = [col[0] for col in cursor.description]
                    result = [dict(zip(cols, r)) for r in rows]
                cursor.close()
                return result

            else:
                conn.commit()
                cursor.close()
                return True

        except Exception as e:
            retry_count += 1
            last_error = e
            print(f"Database query failed (attempt {retry_count}/{max_retries}): {e}")
            if retry_count < max_retries:
                time.sleep(0.5)
            else:
                raise


def close_connections():
    """Close thread-local connection if present."""
    if hasattr(_thread_local, "connection") and _thread_local.connection is not None:
        try:
            _thread_local.connection.close()
            _thread_local.connection = None
            print("Closed thread-local database connection")
        except Exception as e:
            print(f"Error closing connection: {e}")