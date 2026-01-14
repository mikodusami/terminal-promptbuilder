"""Tests for PromptBuilder."""

import pytest
from src.core import PromptBuilder, PromptConfig, PromptType


class TestPromptBuilder:
    """Test suite for PromptBuilder class."""

    def setup_method(self):
        self.builder = PromptBuilder()

    def test_build_cot_basic(self):
        """Test Chain of Thought prompt generation."""
        config = PromptConfig(task="Solve 2 + 2")
        result = self.builder.build(PromptType.CHAIN_OF_THOUGHT, config)
        
        assert "Task: Solve 2 + 2" in result
        assert "step-by-step" in result.lower()

    def test_build_cot_with_context(self):
        """Test CoT with context."""
        config = PromptConfig(
            task="Calculate the total",
            context="Shopping cart with 3 items"
        )
        result = self.builder.build(PromptType.CHAIN_OF_THOUGHT, config)
        
        assert "Context: Shopping cart" in result
        assert "Task: Calculate" in result

    def test_build_cot_with_constraints(self):
        """Test CoT with constraints."""
        config = PromptConfig(
            task="Solve the equation",
            constraints=["Show all work", "Use metric units"]
        )
        result = self.builder.build(PromptType.CHAIN_OF_THOUGHT, config)
        
        assert "Show all work" in result
        assert "Use metric units" in result

    def test_build_few_shot_basic(self):
        """Test Few-Shot prompt generation."""
        config = PromptConfig(
            task="Translate to French",
            examples=[
                {"input": "Hello", "output": "Bonjour"},
                {"input": "Goodbye", "output": "Au revoir"}
            ]
        )
        result = self.builder.build(PromptType.FEW_SHOT, config)
        
        assert "Example 1:" in result
        assert "Hello" in result
        assert "Bonjour" in result

    def test_build_role_based_default_role(self):
        """Test Role-Based with default role."""
        config = PromptConfig(task="Review this code")
        result = self.builder.build(PromptType.ROLE_BASED, config)
        
        assert "expert assistant" in result.lower()

    def test_build_role_based_custom_role(self):
        """Test Role-Based with custom role."""
        config = PromptConfig(
            task="Review this code",
            role="senior Python developer"
        )
        result = self.builder.build(PromptType.ROLE_BASED, config)
        
        assert "senior Python developer" in result

    def test_build_structured_default_format(self):
        """Test Structured Output with default JSON format."""
        config = PromptConfig(task="List the items")
        result = self.builder.build(PromptType.STRUCTURED, config)
        
        assert "JSON" in result

    def test_build_structured_custom_format(self):
        """Test Structured Output with custom format."""
        config = PromptConfig(
            task="List the items",
            output_format="Markdown table"
        )
        result = self.builder.build(PromptType.STRUCTURED, config)
        
        assert "Markdown table" in result

    def test_build_react(self):
        """Test ReAct prompt generation."""
        config = PromptConfig(task="Find the answer")
        result = self.builder.build(PromptType.REACT, config)
        
        assert "Thought:" in result
        assert "Action:" in result
        assert "Observation:" in result

    def test_build_tree_of_thoughts(self):
        """Test Tree of Thoughts prompt generation."""
        config = PromptConfig(task="Solve this problem")
        result = self.builder.build(PromptType.TREE_OF_THOUGHTS, config)
        
        assert "3 different initial approaches" in result
        assert "Feasibility" in result

    def test_build_self_consistency(self):
        """Test Self-Consistency prompt generation."""
        config = PromptConfig(task="Verify the answer")
        result = self.builder.build(PromptType.SELF_CONSISTENCY, config)
        
        assert "3 different ways" in result
        assert "consistent" in result.lower()

    def test_build_unknown_type_raises(self):
        """Test that unknown prompt type raises ValueError."""
        config = PromptConfig(task="Test")
        
        with pytest.raises(ValueError, match="Unknown prompt type"):
            self.builder.build("invalid_type", config)

    def test_all_prompt_types_supported(self):
        """Test that all PromptType values are supported."""
        config = PromptConfig(task="Test task")
        
        for prompt_type in PromptType:
            result = self.builder.build(prompt_type, config)
            assert isinstance(result, str)
            assert len(result) > 0
