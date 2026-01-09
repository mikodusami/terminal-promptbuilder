"""
Prompt History - SQLite-based storage for prompts with tagging and favorites.
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class SavedPrompt:
    id: int
    technique: str
    task: str
    prompt: str
    tags: list[str]
    is_favorite: bool
    created_at: datetime

    @classmethod
    def from_row(cls, row: tuple) -> "SavedPrompt":
        return cls(
            id=row[0],
            technique=row[1],
            task=row[2],
            prompt=row[3],
            tags=row[4].split(",") if row[4] else [],
            is_favorite=bool(row[5]),
            created_at=datetime.fromisoformat(row[6])
        )


class PromptHistory:
    """Manage prompt history with SQLite storage."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            config_dir = Path.home() / ".promptbuilder"
            config_dir.mkdir(exist_ok=True)
            db_path = str(config_dir / "history.db")
        
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    technique TEXT NOT NULL,
                    task TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    tags TEXT DEFAULT '',
                    is_favorite INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_technique ON prompts(technique)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_favorite ON prompts(is_favorite)")
            conn.commit()

    def save(self, technique: str, task: str, prompt: str, tags: list[str] = None) -> int:
        """Save a prompt and return its ID."""
        tags_str = ",".join(tags) if tags else ""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO prompts (technique, task, prompt, tags) VALUES (?, ?, ?, ?)",
                (technique, task, prompt, tags_str)
            )
            conn.commit()
            return cursor.lastrowid

    def get(self, prompt_id: int) -> Optional[SavedPrompt]:
        """Get a prompt by ID."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM prompts WHERE id = ?", (prompt_id,)
            ).fetchone()
            return SavedPrompt.from_row(row) if row else None

    def list_recent(self, limit: int = 10) -> list[SavedPrompt]:
        """List recent prompts."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT * FROM prompts ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
            return [SavedPrompt.from_row(r) for r in rows]

    def list_favorites(self) -> list[SavedPrompt]:
        """List favorite prompts."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT * FROM prompts WHERE is_favorite = 1 ORDER BY created_at DESC"
            ).fetchall()
            return [SavedPrompt.from_row(r) for r in rows]

    def search(self, query: str) -> list[SavedPrompt]:
        """Search prompts by task or tags."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT * FROM prompts WHERE task LIKE ? OR tags LIKE ? ORDER BY created_at DESC",
                (f"%{query}%", f"%{query}%")
            ).fetchall()
            return [SavedPrompt.from_row(r) for r in rows]

    def search_by_technique(self, technique: str) -> list[SavedPrompt]:
        """List prompts by technique."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT * FROM prompts WHERE technique = ? ORDER BY created_at DESC",
                (technique,)
            ).fetchall()
            return [SavedPrompt.from_row(r) for r in rows]

    def toggle_favorite(self, prompt_id: int) -> bool:
        """Toggle favorite status, returns new status."""
        with sqlite3.connect(self.db_path) as conn:
            current = conn.execute(
                "SELECT is_favorite FROM prompts WHERE id = ?", (prompt_id,)
            ).fetchone()
            if current is None:
                return False
            new_status = 0 if current[0] else 1
            conn.execute(
                "UPDATE prompts SET is_favorite = ? WHERE id = ?",
                (new_status, prompt_id)
            )
            conn.commit()
            return bool(new_status)

    def add_tags(self, prompt_id: int, new_tags: list[str]):
        """Add tags to a prompt."""
        with sqlite3.connect(self.db_path) as conn:
            current = conn.execute(
                "SELECT tags FROM prompts WHERE id = ?", (prompt_id,)
            ).fetchone()
            if current:
                existing = set(current[0].split(",")) if current[0] else set()
                existing.update(new_tags)
                existing.discard("")
                conn.execute(
                    "UPDATE prompts SET tags = ? WHERE id = ?",
                    (",".join(existing), prompt_id)
                )
                conn.commit()

    def delete(self, prompt_id: int) -> bool:
        """Delete a prompt."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
            conn.commit()
            return cursor.rowcount > 0

    def clear_all(self) -> int:
        """Clear all prompts, returns count deleted."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM prompts")
            conn.commit()
            return cursor.rowcount
