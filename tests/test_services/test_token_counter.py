"""Tests for TokenCounter service."""

import pytest
from src.services.token_counter import TokenCounter, MODEL_PRICING, is_tiktoken_available


class TestTokenCounter:
    """Test suite for TokenCounter class."""

    def setup_method(self):
        self.counter = TokenCounter()

    def test_count_tokens_returns_positive(self):
        """Test that token count is positive for non-empty text."""
        count = self.counter.count_tokens("Hello, world!")
        assert count > 0

    def test_count_tokens_empty_string(self):
        """Test token count for empty string."""
        count = self.counter.count_tokens("")
        assert count == 0

    def test_count_tokens_scales_with_length(self):
        """Test that longer text has more tokens."""
        short = self.counter.count_tokens("Hello")
        long = self.counter.count_tokens("Hello, this is a much longer piece of text")
        assert long > short

    def test_estimate_cost_returns_estimate(self):
        """Test that estimate_cost returns a TokenEstimate."""
        estimate = self.counter.estimate_cost("Test prompt", "gpt-4.1")
        
        assert estimate.token_count > 0
        assert estimate.model == "gpt-4.1"
        assert estimate.provider == "openai"
        assert estimate.input_cost >= 0

    def test_estimate_cost_different_models(self):
        """Test cost estimation for different models."""
        text = "This is a test prompt for cost estimation."
        
        gpt_estimate = self.counter.estimate_cost(text, "gpt-4.1")
        claude_estimate = self.counter.estimate_cost(text, "claude-sonnet-4-5-20250929")
        
        # Different providers
        assert gpt_estimate.provider == "openai"
        assert claude_estimate.provider == "anthropic"

    def test_estimate_cost_unknown_model_uses_default(self):
        """Test that unknown model falls back to default pricing."""
        estimate = self.counter.estimate_cost("Test", "unknown-model")
        
        # Should use gpt-4.1 pricing as fallback
        assert estimate.token_count > 0

    def test_estimate_all_models(self):
        """Test estimating costs across multiple models."""
        estimates = self.counter.estimate_all_models("Test prompt")
        
        assert len(estimates) > 0
        for est in estimates:
            assert est.token_count > 0

    def test_formatted_cost_small_value(self):
        """Test formatted cost for small values."""
        estimate = self.counter.estimate_cost("Hi", "gpt-4.1-nano")
        
        # Should have 4 decimal places for small costs
        assert "$" in estimate.formatted_cost

    def test_model_pricing_has_required_fields(self):
        """Test that all models in pricing have required fields."""
        required_fields = {"input", "output", "encoding", "provider"}
        
        for model, pricing in MODEL_PRICING.items():
            assert required_fields.issubset(pricing.keys()), f"{model} missing fields"


class TestTiktokenAvailability:
    """Test tiktoken availability check."""

    def test_is_tiktoken_available_returns_bool(self):
        """Test that availability check returns boolean."""
        result = is_tiktoken_available()
        assert isinstance(result, bool)
