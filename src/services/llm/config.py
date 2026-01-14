"""
LLM configuration - manage API keys and provider settings.
"""

import os
import json
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

from ...platform.environment import get_config_dir, get_env


@dataclass
class ProviderConfig:
    name: str
    api_key: Optional[str]
    base_url: Optional[str] = None
    models: list[str] = field(default_factory=list)
    is_available: bool = False


PROVIDERS = {
    "openai": {
        "env_key": "OPENAI_API_KEY",
        "models": [
            "gpt-4.1",           # Latest flagship, 1M context
            "gpt-4.1-mini",      # Balanced performance/cost
            "gpt-4.1-nano",      # Cheapest, fast
            "o4-mini",           # Reasoning model
            "gpt-4o",            # Legacy, still supported
        ],
    },
    "anthropic": {
        "env_key": "ANTHROPIC_API_KEY",
        "models": [
            "claude-sonnet-4-5-20250929",   # Best balance of speed/intelligence
            "claude-opus-4-5-20251124",     # Most capable
            "claude-haiku-4-5-20251015",    # Cheapest, fastest
        ],
    },
    "google": {
        "env_key": "GOOGLE_API_KEY",
        "models": [
            "gemini-2.5-pro",        # Most capable
            "gemini-2.5-flash",      # Fast, balanced
            "gemini-2.5-flash-lite", # Cheapest, fastest
        ],
    }
}


class LLMConfig:
    """Manage API keys for multiple LLM providers."""

    def __init__(self):
        self.config_path = get_config_dir() / "api_config.json"
        self.providers: dict[str, ProviderConfig] = {}
        self.default_provider: Optional[str] = None
        self.default_model: Optional[str] = None
        self._load_config()

    def _load_config(self) -> None:
        """Load API keys from environment and config file."""
        file_config = {}
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    file_config = json.load(f)
            except Exception:
                pass

        # Load default model settings
        self.default_provider = file_config.get("default_provider")
        self.default_model = file_config.get("default_model")

        for name, info in PROVIDERS.items():
            api_key = get_env(info["env_key"]) or file_config.get(name, {}).get("api_key")
            base_url = file_config.get(name, {}).get("base_url")
            
            self.providers[name] = ProviderConfig(
                name=name,
                api_key=api_key,
                base_url=base_url,
                models=info["models"],
                is_available=bool(api_key)
            )

    def save_config(self):
        """Save current config to file."""
        config = {}
        for name, provider in self.providers.items():
            if provider.api_key:
                config[name] = {
                    "api_key": provider.api_key,
                    "base_url": provider.base_url
                }
        
        # Save default model settings
        if self.default_provider:
            config["default_provider"] = self.default_provider
        if self.default_model:
            config["default_model"] = self.default_model
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)

    def set_api_key(self, provider: str, api_key: str, base_url: str = None):
        """Set API key for a provider."""
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")
        
        self.providers[provider].api_key = api_key
        self.providers[provider].is_available = bool(api_key)
        if base_url:
            self.providers[provider].base_url = base_url
        
        self.save_config()

    def set_default_model(self, provider: str, model: str):
        """Set the default provider and model."""
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")
        if model not in self.providers[provider].models:
            raise ValueError(f"Unknown model: {model}")
        
        self.default_provider = provider
        self.default_model = model
        self.save_config()

    def get_default_model(self) -> tuple[Optional[str], Optional[str]]:
        """Get the default provider and model."""
        # Return configured default if valid
        if self.default_provider and self.default_model:
            if self.providers.get(self.default_provider, ProviderConfig("", None)).is_available:
                return self.default_provider, self.default_model
        
        # Fall back to first available
        available = self.get_available_providers()
        if available:
            provider = available[0]
            model = self.providers[provider].models[0]
            return provider, model
        
        return None, None

    def get_available_providers(self) -> list[str]:
        """Get list of providers with valid API keys."""
        return [name for name, p in self.providers.items() if p.is_available]

    def get_available_models(self) -> list[tuple[str, str]]:
        """Get all available models as (provider, model) tuples."""
        models = []
        for name, provider in self.providers.items():
            if provider.is_available:
                for model in provider.models:
                    models.append((name, model))
        return models

    def get_provider(self, name: str) -> Optional[ProviderConfig]:
        """Get provider config by name."""
        return self.providers.get(name)

    def has_any_provider(self) -> bool:
        """Check if at least one provider is configured."""
        return any(p.is_available for p in self.providers.values())

    def has_multiple_providers(self) -> bool:
        """Check if multiple providers are configured."""
        return len(self.get_available_providers()) > 1
