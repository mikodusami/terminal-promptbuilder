"""
Sharing feature - common types.
"""

from dataclasses import dataclass
from datetime import datetime
import hashlib


@dataclass
class SharedPrompt:
    id: str
    name: str
    technique: str
    prompt: str
    description: str = ""
    tags: list[str] = None
    author: str = ""
    created_at: str = ""
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.id:
            self.id = hashlib.md5(f"{self.name}{self.prompt}".encode()).hexdigest()[:12]


@dataclass
class PromptLibrary:
    name: str
    description: str
    version: str
    author: str
    prompts: list[SharedPrompt]
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
