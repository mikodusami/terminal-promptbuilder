"""
Token counting and cost estimation service.
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
    provider: str
    input_cost: float
    output_cost_1k: float
    
    @property
    def formatted_cost(self) -> str:
        if self.input_cost < 0.01:
            return f"${self.input_cost:.4f}"
        return f"${self.input_cost:.3f}"


# Pricing per 1K tokens (updated January 2026, derived from per-1M pricing)
# Formula: price_per_1k = price_per_1M / 1000
MODEL_PRICING = {
    # OpenAI models (per 1M: gpt-4.1=$2/$8, mini=$0.40/$1.60, nano=$0.10/$0.40, o4-mini=$1.10/$4.40, gpt-4o=$2.50/$10)
    "gpt-4.1": {"input": 0.002, "output": 0.008, "encoding": "o200k_base", "provider": "openai"},
    "gpt-4.1-mini": {"input": 0.0004, "output": 0.0016, "encoding": "o200k_base", "provider": "openai"},
    "gpt-4.1-nano": {"input": 0.0001, "output": 0.0004, "encoding": "o200k_base", "provider": "openai"},
    "o4-mini": {"input": 0.0011, "output": 0.0044, "encoding": "o200k_base", "provider": "openai"},
    "gpt-4o": {"input": 0.0025, "output": 0.01, "encoding": "o200k_base", "provider": "openai"},
    # Anthropic models (per 1M: sonnet=$3/$15, opus=$5/$25, haiku=$1/$5)
    "claude-sonnet-4-5-20250929": {"input": 0.003, "output": 0.015, "encoding": "cl100k_base", "provider": "anthropic"},
    "claude-opus-4-5-20251124": {"input": 0.005, "output": 0.025, "encoding": "cl100k_base", "provider": "anthropic"},
    "claude-haiku-4-5-20251015": {"input": 0.001, "output": 0.005, "encoding": "cl100k_base", "provider": "anthropic"},
    # Google models (per 1M: pro=$1.25/$10, flash=$0.30/$2.50, flash-lite=$0.10/$0.40)
    "gemini-2.5-pro": {"input": 0.00125, "output": 0.01, "encoding": "cl100k_base", "provider": "google"},
    "gemini-2.5-flash": {"input": 0.0003, "output": 0.0025, "encoding": "cl100k_base", "provider": "google"},
    "gemini-2.5-flash-lite": {"input": 0.0001, "output": 0.0004, "encoding": "cl100k_base", "provider": "google"},
}

# Models to show by provider
MODELS_BY_PROVIDER = {
    "openai": ["gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano"],
    "anthropic": ["claude-sonnet-4-5-20250929", "claude-haiku-4-5-20251015"],
    "google": ["gemini-2.5-flash", "gemini-2.5-flash-lite"],
}


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

    def count_tokens(self, text: str, model: str = "gpt-4.1") -> int:
        """Count tokens for a given text and model."""
        if not TIKTOKEN_AVAILABLE:
            return len(text) // 4
        
        pricing = MODEL_PRICING.get(model, MODEL_PRICING["gpt-4.1"])
        encoder = self._get_encoder(pricing["encoding"])
        
        if encoder:
            return len(encoder.encode(text))
        return len(text) // 4

    def estimate_cost(self, text: str, model: str = "gpt-4.1") -> TokenEstimate:
        """Estimate the cost for a prompt."""
        token_count = self.count_tokens(text, model)
        pricing = MODEL_PRICING.get(model, MODEL_PRICING["gpt-4.1"])
        
        input_cost = (token_count / 1000) * pricing["input"]
        
        return TokenEstimate(
            token_count=token_count,
            model=model,
            provider=pricing.get("provider", "unknown"),
            input_cost=input_cost,
            output_cost_1k=pricing["output"]
        )

    def estimate_for_providers(self, text: str, available_providers: list[str]) -> list[TokenEstimate]:
        """Estimate costs for models from available providers only."""
        estimates = []
        for provider in available_providers:
            models = MODELS_BY_PROVIDER.get(provider, [])
            for model in models:
                estimates.append(self.estimate_cost(text, model))
        return estimates

    def estimate_all_models(self, text: str, models: list[str] = None) -> list[TokenEstimate]:
        """Estimate costs across multiple models."""
        if models is None:
            # Default to a representative set
            models = ["gpt-4.1-mini", "claude-sonnet-4-5-20250929", "gemini-2.5-flash"]
        return [self.estimate_cost(text, model) for model in models if model in MODEL_PRICING]


def is_tiktoken_available() -> bool:
    """Check if tiktoken is available."""
    return TIKTOKEN_AVAILABLE
