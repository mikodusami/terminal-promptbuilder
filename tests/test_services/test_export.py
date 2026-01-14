"""Tests for ExportService."""

import json
import pytest
from src.services.export import ExportService, ExportFormat, ExportMetadata


class TestExportService:
    """Test suite for ExportService class."""

    def test_export_json_format(self):
        """Test JSON export format."""
        content, ext = ExportService.export("Test prompt", ExportFormat.JSON)
        
        assert ext == ".json"
        data = json.loads(content)
        assert "messages" in data
        assert data["messages"][0]["content"] == "Test prompt"

    def test_export_json_with_metadata(self):
        """Test JSON export with metadata."""
        metadata = ExportMetadata(
            technique="cot",
            task="Test task",
            created_at="2026-01-13",
            tags=["test", "example"]
        )
        content, _ = ExportService.export("Test prompt", ExportFormat.JSON, metadata)
        
        data = json.loads(content)
        assert data["metadata"]["technique"] == "cot"
        assert data["metadata"]["tags"] == ["test", "example"]

    def test_export_openai_format(self):
        """Test OpenAI export format."""
        content, ext = ExportService.export("Test prompt", ExportFormat.OPENAI)
        
        assert ext == ".json"
        data = json.loads(content)
        assert data["messages"][0]["role"] == "user"

    def test_export_anthropic_format(self):
        """Test Anthropic export format."""
        content, ext = ExportService.export("Test prompt", ExportFormat.ANTHROPIC)
        
        assert ext == ".json"
        data = json.loads(content)
        assert data["messages"][0]["role"] == "user"

    def test_export_markdown_format(self):
        """Test Markdown export format."""
        metadata = ExportMetadata(
            technique="role",
            task="Code review",
            created_at="2026-01-13"
        )
        content, ext = ExportService.export("Test prompt", ExportFormat.MARKDOWN, metadata)
        
        assert ext == ".md"
        assert "# Code review" in content
        assert "```" in content
        assert "Test prompt" in content

    def test_export_langchain_format(self):
        """Test LangChain export format."""
        content, ext = ExportService.export("Hello {name}", ExportFormat.LANGCHAIN)
        
        assert ext == ".json"
        data = json.loads(content)
        assert data["_type"] == "prompt"
        # Braces should be escaped
        assert "{{name}}" in data["template"]

    def test_export_llamaindex_format(self):
        """Test LlamaIndex export format."""
        content, ext = ExportService.export("Test prompt", ExportFormat.LLAMAINDEX)
        
        assert ext == ".json"
        data = json.loads(content)
        assert data["prompt_type"] == "custom"

    def test_export_prompt_file_format(self):
        """Test .prompt file format."""
        metadata = ExportMetadata(
            technique="few_shot",
            task="Translation",
            created_at="2026-01-13"
        )
        content, ext = ExportService.export("Test prompt", ExportFormat.PROMPT_FILE, metadata)
        
        assert ext == ".prompt"
        assert "---" in content
        assert "technique: few_shot" in content
        assert "Test prompt" in content

    def test_export_text_format(self):
        """Test plain text export format."""
        content, ext = ExportService.export("Test prompt", ExportFormat.TEXT)
        
        assert ext == ".txt"
        assert content == "Test prompt"


class TestExportMetadata:
    """Test ExportMetadata dataclass."""

    def test_metadata_defaults(self):
        """Test metadata default values."""
        metadata = ExportMetadata(
            technique="cot",
            task="Test",
            created_at="2026-01-13"
        )
        
        assert metadata.tags == []

    def test_metadata_with_tags(self):
        """Test metadata with tags."""
        metadata = ExportMetadata(
            technique="cot",
            task="Test",
            created_at="2026-01-13",
            tags=["a", "b"]
        )
        
        assert metadata.tags == ["a", "b"]
