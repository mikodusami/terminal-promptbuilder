"""
Base storage utilities for SQLite-backed persistence.
"""

import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from .environment import get_data_dir


class BaseStorage:
    """Base class for SQLite-backed storage."""

    def __init__(self, db_name: str, db_path: Optional[str] = None):
        if db_path is None:
            db_path = str(get_data_dir() / db_name)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database schema. Override in subclasses."""
        pass

    @contextmanager
    def _get_connection(self):
        """Get a database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()) -> list:
        """Execute a query and return results."""
        with self._get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def execute_write(self, query: str, params: tuple = ()) -> int:
        """Execute a write query and return lastrowid."""
        with self._get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.lastrowid
