"""UI components for the settings feature."""

from typing import Optional
from rich.console import Console
from rich.prompt import Prompt

try:
    from simple_term_menu import TerminalMenu
    MENU_AVAILABLE = True
except ImportError:
    MENU_AVAILABLE = False


def interactive_select(options: list[str], title: str = "") -> Optional[int]:
    """Show an interactive selection menu."""
    if MENU_AVAILABLE:
        menu = TerminalMenu(options, title=title)
        return menu.show()
    else:
        print(f"\n{title}" if title else "")
        for i, opt in enumerate(options, 1):
            print(f"  [{i}] {opt}")
        try:
            choice = input("Select: ").strip()
            idx = int(choice) - 1
            return idx if 0 <= idx < len(options) else None
        except (ValueError, IndexError):
            return None


def show_status(console: Console, config) -> None:
    """Show current API key status."""
    default_provider, default_model = config.get_default_model()
    
    status_lines = []
    for name, provider in config.providers.items():
        status = "✓" if provider.is_available else "✗"
        status_lines.append(f"{name.capitalize()}: {status}")
    
    default_display = f"{default_provider}/{default_model}" if default_provider else "Not set"
    
    console.print("\n[bold]⚙️ Settings[/]\n")
    console.print(f"API Keys: {' | '.join(status_lines)}")
    console.print(f"Default Model: {default_display}\n")


def set_api_key(console: Console, provider: str, config, app_state) -> None:
    """Set API key for a provider."""
    key = Prompt.ask(f"[bold]Enter {provider.capitalize()} API key[/]", password=True)
    
    if key:
        config.set_api_key(provider, key)
        # Reinitialize LLM client
        if app_state:
            from src.services.llm.client import LLMClient
            app_state.llm_client = LLMClient(config)
        console.print(f"[green]✓ {provider.capitalize()} API key saved[/]")


def set_default_model(console: Console, config, app_state) -> None:
    """Set the default model for AI features."""
    available_models = config.get_available_models()
    
    if not available_models:
        console.print("[yellow]No API keys configured. Add keys first.[/]")
        return
    
    model_info = {
        "gpt-4.1": "Flagship, 1M context",
        "gpt-4.1-mini": "Balanced",
        "gpt-4.1-nano": "Cheapest, fast",
        "o4-mini": "Reasoning model",
        "gpt-4o": "Legacy",
        "claude-sonnet-4-5-20250929": "Best balance",
        "claude-opus-4-5-20251124": "Most capable",
        "claude-haiku-4-5-20251015": "Cheapest, fast",
        "gemini-2.5-pro": "Most capable",
        "gemini-2.5-flash": "Fast, balanced",
        "gemini-2.5-flash-lite": "Cheapest, fast",
    }
    
    menu_options = []
    for provider, model in available_models:
        info = model_info.get(model, "")
        info_str = f" ({info})" if info else ""
        menu_options.append(f"{provider}: {model}{info_str}")
    
    console.print("\n[bold]Select Default Model[/]\n")
    
    idx = interactive_select(menu_options, title="")
    
    if idx is not None and 0 <= idx < len(available_models):
        provider, model = available_models[idx]
        config.set_default_model(provider, model)
        
        if app_state:
            from src.services.llm.client import LLMClient
            app_state.llm_client = LLMClient(config)
        
        console.print(f"\n[green]✓ Default set to {provider} / {model}[/]")
