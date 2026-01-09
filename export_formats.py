"""
Export prompts in various formats.
"""

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PromptMetadata:
    technique: str
    task: str
    created_at: str
    tags: list[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class PromptExporter:
    """Export prompts in various formats."""

    @staticmethod
    def to_json(prompt: str, metadata: Optional[PromptMetadata] = None) -> str:
        """Export as JSON for API calls."""
        data = {
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        if metadata:
            data["metadata"] = {
                "technique": metadata.technique,
                "task": metadata.task,
                "created_at": metadata.created_at,
                "tags": metadata.tags
            }
        
        return json.dumps(data, indent=2)

    @staticmethod
    def to_openai_format(prompt: str, system_prompt: str = None) -> str:
        """Export in OpenAI API format."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        return json.dumps({"messages": messages}, indent=2)

    @staticmethod
    def to_anthropic_format(prompt: str, system_prompt: str = None) -> str:
        """Export in Anthropic API format."""
        data = {
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system_prompt:
            data["system"] = system_prompt
        
        return json.dumps(data, indent=2)

    @staticmethod
    def to_markdown(prompt: str, metadata: Optional[PromptMetadata] = None) -> str:
        """Export as Markdown document."""
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
    def to_langchain(prompt: str, metadata: Optional[PromptMetadata] = None) -> str:
        """Export as LangChain PromptTemplate format."""
        # Escape curly braces for LangChain
        escaped = prompt.replace("{", "{{").replace("}", "}}")
        
        data = {
            "_type": "prompt",
            "input_variables": [],
            "template": escaped
        }
        
        if metadata:
            data["metadata"] = {
                "technique": metadata.technique,
                "task": metadata.task
            }
        
        return json.dumps(data, indent=2)

    @staticmethod
    def to_llamaindex(prompt: str, metadata: Optional[PromptMetadata] = None) -> str:
        """Export as LlamaIndex prompt format."""
        data = {
            "prompt_type": "custom",
            "prompt_template": prompt
        }
        
        if metadata:
            data["metadata"] = {
                "technique": metadata.technique,
                "task": metadata.task
            }
        
        return json.dumps(data, indent=2)

    @staticmethod
    def to_prompt_file(prompt: str, metadata: Optional[PromptMetadata] = None) -> str:
        """Export as .prompt file format (simple structured text)."""
        lines = []
        
        lines.append("---")
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


EXPORT_FORMATS = {
    "json": ("JSON (API)", PromptExporter.to_json, ".json"),
    "openai": ("OpenAI Format", PromptExporter.to_openai_format, ".json"),
    "anthropic": ("Anthropic Format", PromptExporter.to_anthropic_format, ".json"),
    "markdown": ("Markdown", PromptExporter.to_markdown, ".md"),
    "langchain": ("LangChain", PromptExporter.to_langchain, ".json"),
    "llamaindex": ("LlamaIndex", PromptExporter.to_llamaindex, ".json"),
    "prompt": ("Prompt File", PromptExporter.to_prompt_file, ".prompt"),
    "txt": ("Plain Text", lambda p, m=None: p, ".txt"),
}


def export_prompt(
    prompt: str,
    format_key: str,
    metadata: Optional[PromptMetadata] = None
) -> tuple[str, str]:
    """
    Export a prompt in the specified format.
    
    Returns: (exported_content, file_extension)
    """
    if format_key not in EXPORT_FORMATS:
        raise ValueError(f"Unknown format: {format_key}")
    
    _, exporter, extension = EXPORT_FORMATS[format_key]
    content = exporter(prompt, metadata)
    
    return content, extension


def list_formats() -> list[tuple[str, str]]:
    """List available export formats."""
    return [(key, name) for key, (name, _, _) in EXPORT_FORMATS.items()]
