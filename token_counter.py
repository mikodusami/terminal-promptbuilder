"""
Token Counter & Cost Estimator for prompts.
"""

from dataclasses import dataclass
from typing import Optional

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


@dataclass
class TokenEstimate:
    token_count: int
    model: str
    input_cost: float
    output_cost_1k: float  # Cost per 1K output tokens (estimated)
    
    @property
    def formatted_cost(self) -> str:
        if self.input_cost < 0.01:
            return f"${self.input_cost:.4f}"
        return f"${self.input_cost:.3f}"


# Pricing per 1K tokens (as of late 2024 - update as needed)
MODEL_PRICING = {
    "gpt-4o": {"input": 0.0025, "output": 0.01, "encoding": "o200k_base"},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006, "encoding": "o200k_base"},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03, "encoding": "cl100k_base"},
    "gpt-4": {"input": 0.03, "output": 0.06, "encoding": "cl100k_base"},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015, "encoding": "cl100k_base"},
    "claude-3-opus": {"input": 0.015, "output": 0.075, "encoding": "cl100k_base"},
    "claude-3-sonnet": {"input": 0.003, "output": 0.015, "encoding": "cl100k_base"},
    "claude-3-haiku": {"input": 0.00025, "output": 0.00125, "encoding": "cl100k_base"},
    "claude-3.5-sonnet": {"input": 0.003, "output": 0.015, "encoding": "cl100k_base"},
}

DEFAULT_MODELS = ["gpt-4o", "gpt-4o-mini", "claude-3.5-sonnet", "claude-3-haiku"]


class TokenCounter:
    """Count tokens and estimate costs for prompts."""

    def __init__(self):
        self._encoders = {}

    def _get_encoder(self, encoding_name: str):
        """Get or create a tiktoken encoder."""
        if not TIKTOKEN_AVAILABLE:
            return None
        
        if encoding_name not in self._encoders:
            try:
                self._encoders[encoding_name] = tiktoken.get_encoding(encoding_name)
            except Exception:
                return None
        return self._encoders[encoding_name]

    def count_tokens(self, text: str, model: str = "gpt-4o") -> int:
        """Count tokens for a given text and model."""
        if not TIKTOKEN_AVAILABLE:
            # Fallback: rough estimate of ~4 chars per token
            return len(text) // 4
        
        pricing = MODEL_PRICING.get(model, MODEL_PRICING["gpt-4o"])
        encoder = self._get_encoder(pricing["encoding"])
        
        if encoder:
            return len(encoder.encode(text))
        
        # Fallback
        return len(text) // 4

    def estimate_cost(self, text: str, model: str = "gpt-4o") -> TokenEstimate:
        """Estimate the cost for a prompt."""
        token_count = self.count_tokens(text, model)
        pricing = MODEL_PRICING.get(model, MODEL_PRICING["gpt-4o"])
        
        input_cost = (token_count / 1000) * pricing["input"]
        output_cost_1k = pricing["output"]
        
        return TokenEstimate(
            token_count=token_count,
            model=model,
            input_cost=input_cost,
            output_cost_1k=output_cost_1k
        )

    def estimate_all_models(self, text: str, models: list[str] = None) -> list[TokenEstimate]:
        """Estimate costs across multiple models."""
        if models is None:
            models = DEFAULT_MODELS
        
        return [self.estimate_cost(text, model) for model in models]

    def format_estimates(self, text: str, models: list[str] = None) -> str:
        """Format token estimates as a readable string."""
        estimates = self.estimate_all_models(text, models)
        
        lines = ["Token & Cost Estimates:", "-" * 40]
        for est in estimates:
            lines.append(
                f"{est.model:<18} {est.token_count:>6} tokens  "
                f"Input: {est.formatted_cost:<8} Output/1K: ${est.output_cost_1k:.4f}"
            )
        
        return "\n".join(lines)


def is_tiktoken_available() -> bool:
    """Check if tiktoken is available."""
    return TIKTOKEN_AVAILABLE
