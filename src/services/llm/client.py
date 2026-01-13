"""
LLM Client - unified interface for multiple LLM providers.
"""

from typing import Optional
from dataclasses import dataclass
import asyncio

from .config import LLMConfig


@dataclass
class LLMResponse:
    content: str
    model: str
    provider: str
    input_tokens: int = 0
    output_tokens: int = 0
    error: Optional[str] = None


class LLMClient:
    """Unified client for OpenAI, Anthropic, and Google APIs."""

    def __init__(self, config: LLMConfig = None):
        self.config = config or LLMConfig()
        self._clients = {}

    def _get_openai_client(self):
        if "openai" not in self._clients:
            try:
                from openai import OpenAI
                provider = self.config.get_provider("openai")
                if provider and provider.api_key:
                    self._clients["openai"] = OpenAI(
                        api_key=provider.api_key,
                        base_url=provider.base_url
                    )
            except ImportError:
                pass
        return self._clients.get("openai")

    def _get_anthropic_client(self):
        if "anthropic" not in self._clients:
            try:
                from anthropic import Anthropic
                provider = self.config.get_provider("anthropic")
                if provider and provider.api_key:
                    self._clients["anthropic"] = Anthropic(api_key=provider.api_key)
            except ImportError:
                pass
        return self._clients.get("anthropic")

    def _get_google_client(self):
        if "google" not in self._clients:
            try:
                from google import genai
                provider = self.config.get_provider("google")
                if provider and provider.api_key:
                    client = genai.Client(api_key=provider.api_key)
                    self._clients["google"] = client
            except ImportError:
                pass
        return self._clients.get("google")

    async def complete(
        self,
        prompt: str,
        provider: str = None,
        model: str = None,
        system_prompt: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> LLMResponse:
        """Send a completion request to the specified provider."""
        
        if not provider or not model:
            default_provider, default_model = self.config.get_default_model()
            if not provider:
                provider = default_provider
            if not model:
                model = default_model
        
        if not provider:
            return LLMResponse(
                content="", model="", provider="",
                error="No API keys configured. Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY."
            )

        try:
            if provider == "openai":
                return await self._complete_openai(prompt, model, system_prompt, max_tokens, temperature)
            elif provider == "anthropic":
                return await self._complete_anthropic(prompt, model, system_prompt, max_tokens, temperature)
            elif provider == "google":
                return await self._complete_google(prompt, model, system_prompt, max_tokens, temperature)
            else:
                return LLMResponse(content="", model=model, provider=provider, error=f"Unknown provider: {provider}")
        except Exception as e:
            return LLMResponse(content="", model=model, provider=provider, error=str(e))

    async def _complete_openai(self, prompt, model, system_prompt, max_tokens, temperature) -> LLMResponse:
        client = self._get_openai_client()
        if not client:
            return LLMResponse(content="", model=model, provider="openai", 
                             error="OpenAI not available. Install: pip install openai")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=model, messages=messages, max_tokens=max_tokens, temperature=temperature
        )

        return LLMResponse(
            content=response.choices[0].message.content,
            model=model, provider="openai",
            input_tokens=response.usage.prompt_tokens if response.usage else 0,
            output_tokens=response.usage.completion_tokens if response.usage else 0
        )

    async def _complete_anthropic(self, prompt, model, system_prompt, max_tokens, temperature) -> LLMResponse:
        client = self._get_anthropic_client()
        if not client:
            return LLMResponse(content="", model=model, provider="anthropic",
                             error="Anthropic not available. Install: pip install anthropic")

        kwargs = {"model": model, "max_tokens": max_tokens, "messages": [{"role": "user", "content": prompt}]}
        if system_prompt:
            kwargs["system"] = system_prompt

        response = await asyncio.to_thread(client.messages.create, **kwargs)

        return LLMResponse(
            content=response.content[0].text,
            model=model, provider="anthropic",
            input_tokens=response.usage.input_tokens if response.usage else 0,
            output_tokens=response.usage.output_tokens if response.usage else 0
        )

    async def _complete_google(self, prompt, model, system_prompt, max_tokens, temperature) -> LLMResponse:
        client = self._get_google_client()
        if not client:
            return LLMResponse(content="", model=model, provider="google",
                             error="Google not available. Install: pip install google-genai")

        from google.genai import types

        contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        config = types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )
        
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=model,
            contents=contents,
            config=config,
        )

        input_tokens = response.usage_metadata.prompt_token_count if response.usage_metadata else 0
        output_tokens = response.usage_metadata.candidates_token_count if response.usage_metadata else 0

        return LLMResponse(
            content=response.text,
            model=model,
            provider="google",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
