"""
Export service - export prompts in various formats.
"""

import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class ExportFormat(Enum):
    JSON = "json"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MARKDOWN = "markdown"
    LANGCHAIN = "langchain"
    LLAMAINDEX = "llamaindex"
    PROMPT_FILE = "prompt"
    TEXT = "txt"


@dataclass
class ExportMetadata:
    technique: str
    task: str
    created_at: str
    tags: list[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


FORMAT_INFO = {
    ExportFormat.JSON: ("JSON (API)", ".json"),
    ExportFormat.OPENAI: ("OpenAI Format", ".json"),
    ExportFormat.ANTHROPIC: ("Anthropic Format", ".json"),
    ExportFormat.MARKDOWN: ("Markdown", ".md"),
    ExportFormat.LANGCHAIN: ("LangChain", ".json"),
    ExportFormat.LLAMAINDEX: ("LlamaIndex", ".json"),
    ExportFormat.PROMPT_FILE: ("Prompt File", ".prompt"),
    ExportFormat.TEXT: ("Plain Text", ".txt"),
}


class ExportService:
    """Export prompts in various formats."""

    @staticmethod
    def export(prompt: str, format: ExportFormat, metadata: Optional[ExportMetadata] = None) -> tuple[str, str]:
        """Export prompt in specified format. Returns (content, extension)."""
        exporters = {
            ExportFormat.JSON: ExportService._to_json,
            ExportFormat.OPENAI: ExportService._to_openai,
            ExportFormat.ANTHROPIC: ExportService._to_anthropic,
            ExportFormat.MARKDOWN: ExportService._to_markdown,
            ExportFormat.LANGCHAIN: ExportService._to_langchain,
            ExportFormat.LLAMAINDEX: ExportService._to_llamaindex,
            ExportFormat.PROMPT_FILE: ExportService._to_prompt_file,
            ExportFormat.TEXT: ExportService._to_text,
        }
        
        exporter = exporters.get(format, ExportService._to_text)
        content = exporter(prompt, metadata)
        _, extension = FORMAT_INFO.get(format, ("Text", ".txt"))
        
        return content, extension

    @staticmethod
    def _to_json(prompt: str, metadata: Optional[ExportMetadata]) -> str:
        data = {"messages": [{"role": "user", "content": prompt}]}
        if metadata:
            data["metadata"] = {
                "technique": metadata.technique,
                "task": metadata.task,
                "created_at": metadata.created_at,
                "tags": metadata.tags
            }
        return json.dumps(data, indent=2)

    @staticmethod
    def _to_openai(prompt: str, metadata: Optional[ExportMetadata]) -> str:
        return json.dumps({
            "messages": [{"role": "user", "content": prompt}]
        }, indent=2)

    @staticmethod
    def _to_anthropic(prompt: str, metadata: Optional[ExportMetadata]) -> str:
        return json.dumps({
            "messages": [{"role": "user", "content": prompt}]
        }, indent=2)

    @staticmethod
    def _to_markdown(prompt: str, metadata: Optional[ExportMetadata]) -> str:
        lines = []
        if metadata:
            lines.append(f"# {metadata.task}")
            lines.append("")
            lines.append(f"**Technique:** {metadata.technique}")
            lines.append(f"**Created:** {metadata.created_at}")
            if metadata.tags:
                lines.append(f"**Tags:** {', '.join(metadata.tags)}")
            lines.append("")
            lines.append("---")
            lines.append("")
        lines.append("## Prompt")
        lines.append("")
        lines.append("```")
        lines.append(prompt)
        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def _to_langchain(prompt: str, metadata: Optional[ExportMetadata]) -> str:
        escaped = prompt.replace("{", "{{").replace("}", "}}")
        data = {"_type": "prompt", "input_variables": [], "template": escaped}
        return json.dumps(data, indent=2)

    @staticmethod
    def _to_llamaindex(prompt: str, metadata: Optional[ExportMetadata]) -> str:
        data = {"prompt_type": "custom", "prompt_template": prompt}
        return json.dumps(data, indent=2)

    @staticmethod
    def _to_prompt_file(prompt: str, metadata: Optional[ExportMetadata]) -> str:
        lines = ["---"]
        if metadata:
            lines.append(f"technique: {metadata.technique}")
            lines.append(f"task: {metadata.task}")
            lines.append(f"created: {metadata.created_at}")
            if metadata.tags:
                lines.append(f"tags: {', '.join(metadata.tags)}")
        lines.append("---")
        lines.append("")
        lines.append(prompt)
        return "\n".join(lines)

    @staticmethod
    def _to_text(prompt: str, metadata: Optional[ExportMetadata]) -> str:
        return prompt


def export_prompt(prompt: str, format_key: str, metadata: Optional[ExportMetadata] = None) -> tuple[str, str]:
    """Export a prompt in the specified format. Returns (content, extension)."""
    format_map = {
        "json": ExportFormat.JSON,
        "openai": ExportFormat.OPENAI,
        "anthropic": ExportFormat.ANTHROPIC,
        "markdown": ExportFormat.MARKDOWN,
        "langchain": ExportFormat.LANGCHAIN,
        "llamaindex": ExportFormat.LLAMAINDEX,
        "prompt": ExportFormat.PROMPT_FILE,
        "txt": ExportFormat.TEXT,
    }
    fmt = format_map.get(format_key, ExportFormat.TEXT)
    return ExportService.export(prompt, fmt, metadata)
