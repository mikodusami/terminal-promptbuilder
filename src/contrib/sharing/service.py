"""
Sharing feature - service for sharing prompt libraries.
"""

import json
import base64
import gzip
from dataclasses import asdict
from typing import Optional
from pathlib import Path

from ...platform.environment import get_config_dir
from .common import SharedPrompt, PromptLibrary


class SharingService:
    """Handle prompt library export/import and sharing."""

    def __init__(self):
        self.library_path = get_config_dir() / "libraries"
        self.library_path.mkdir(parents=True, exist_ok=True)

    def create_library(self, name: str, description: str, prompts: list[SharedPrompt],
                       author: str = "", version: str = "1.0.0") -> PromptLibrary:
        return PromptLibrary(name=name, description=description, version=version,
                            author=author, prompts=prompts)

    def export_library(self, library: PromptLibrary, path: str = None) -> str:
        if path is None:
            path = self.library_path / f"{library.name.lower().replace(' ', '_')}.json"
        
        data = {
            "name": library.name, "description": library.description,
            "version": library.version, "author": library.author,
            "created_at": library.created_at,
            "prompts": [asdict(p) for p in library.prompts]
        }
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        return str(path)

    def import_library(self, path: str) -> PromptLibrary:
        with open(path) as f:
            data = json.load(f)
        prompts = [SharedPrompt(**p) for p in data.get("prompts", [])]
        return PromptLibrary(
            name=data.get("name", "Imported"),
            description=data.get("description", ""),
            version=data.get("version", "1.0.0"),
            author=data.get("author", ""),
            prompts=prompts
        )

    def generate_share_code(self, library: PromptLibrary) -> str:
        data = {"name": library.name, "prompts": [asdict(p) for p in library.prompts]}
        json_str = json.dumps(data, separators=(',', ':'))
        compressed = gzip.compress(json_str.encode('utf-8'))
        return f"pb://{base64.urlsafe_b64encode(compressed).decode('ascii')}"

    def import_from_share_code(self, code: str) -> PromptLibrary:
        if not code.startswith("pb://"):
            raise ValueError("Invalid share code")
        compressed = base64.urlsafe_b64decode(code[5:])
        data = json.loads(gzip.decompress(compressed).decode('utf-8'))
        prompts = [SharedPrompt(**p) for p in data.get("prompts", [])]
        return PromptLibrary(name=data.get("name", "Shared"), description="",
                            version="1.0.0", author="", prompts=prompts)

    def list_local_libraries(self) -> list[str]:
        return [f.stem for f in self.library_path.glob("*.json")]

    def load_local_library(self, name: str) -> Optional[PromptLibrary]:
        path = self.library_path / f"{name}.json"
        return self.import_library(str(path)) if path.exists() else None
