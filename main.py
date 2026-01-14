#!/usr/bin/env python3
"""
Prompt Builder - Create exceptional prompts using modern prompt engineering techniques.

This is the main entry point. It bootstraps the application and renders
a menu from dynamically discovered features in src/workbench/contrib/.
"""

import asyncio
from dataclasses import dataclass
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from simple_term_menu import TerminalMenu
    MENU_AVAILABLE = True
except ImportError:
    MENU_AVAILABLE = False

from src.core import PromptBuilder
from src.services.token_counter import TokenCounter
from src.services.llm.config import LLMConfig
from src.services.llm.client import LLMClient

from src.workbench import get_registry, reset_registry
from src.workbench.contract import FeatureContext, FeatureCategory
from src.workbench.contrib.history.service import HistoryService
from src.workbench.contrib.analytics.service import PromptAnalytics

console = Console() if RICH_AVAILABLE else None


@dataclass
class AppState:
    """Mutable application state that features can modify."""
    preview_mode: bool = False
    llm_client: Optional[LLMClient] = None


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


class PromptBuilderApp:
    """Main application class - discovers features and renders menu."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
        # Core services
        self.api_config = LLMConfig()
        self.llm_client = LLMClient(self.api_config)
        self.token_counter = TokenCounter()
        self.prompt_builder = PromptBuilder()
        self.history = HistoryService()
        self.analytics = PromptAnalytics()
        
        # Mutable app state
        self.state = AppState(
            preview_mode=False,
            llm_client=self.llm_client,
        )
        
        # Initialize feature registry
        self.registry = get_registry()
        
        if not RICH_AVAILABLE:
            print("[yellow]Install 'rich' for the best experience: pip install rich[/]")

    def run(self):
        """Run the main application loop."""
        self._show_header()
        
        while True:
            feature = self._show_main_menu()
            
            if feature is None:
                continue
            
            # Execute the selected feature
            result = self._execute_feature(feature)
            
            # Check for quit signal
            if result and result.data and result.data.get("action") == "quit":
                break

    def _show_header(self) -> None:
        """Display the application header."""
        if RICH_AVAILABLE:
            header = Text()
            header.append("⚡ PROMPT BUILDER ⚡\n", style="bold bright_white")
            header.append("Modern Prompt Engineering Techniques", style="dim")
            console.print(Panel(header, border_style="bright_blue", box=box.DOUBLE))
            console.print()
        else:
            print("\n" + "=" * 50)
            print("⚡ PROMPT BUILDER - Prompt Engineering Techniques")
            print("=" * 50 + "\n")

    def _show_main_menu(self):
        """Show main menu built from discovered features."""
        # Get all features sorted by menu_order
        features = self.registry.list_all()
        features = sorted(features, key=lambda f: f.manifest.menu_order)
        
        # Build menu options
        menu_options = []
        has_api = self.api_config.has_any_provider()
        preview_status = "ON" if self.state.preview_mode else "OFF"
        
        for feature in features:
            m = feature.manifest
            
            # Add status indicators for special features
            display_name = m.display_name
            if m.name == "preview":
                display_name = f"Preview Mode [{preview_status}]"
            
            # Show API indicator for AI features
            if m.requires_api_key:
                indicator = "●" if has_api else "○"
                option = f"{m.icon} {display_name:<24} [{indicator}] {m.description}"
            else:
                option = f"{m.icon} {display_name:<28} {m.description}"
            
            menu_options.append(option)
        
        if RICH_AVAILABLE:
            console.print("\n[bold]Main Menu[/] [dim](↑↓ to navigate, Enter to select)[/]\n")
        
        idx = interactive_select(menu_options, title="")
        
        if idx is not None and 0 <= idx < len(features):
            return features[idx]
        
        return None

    def _execute_feature(self, feature):
        """Execute a feature and return its result."""
        # Build context for the feature
        ctx = FeatureContext(
            console=console,
            llm_client=self.state.llm_client,
            history=self.history,
            config=self.api_config,
            analytics=self.analytics,
            prompt_builder=self.prompt_builder,
            token_counter=self.token_counter,
            preview_mode=self.state.preview_mode,
            app_state=self.state,
        )
        
        try:
            # Check if feature requires API key
            if feature.manifest.requires_api_key and not self.api_config.has_any_provider():
                if RICH_AVAILABLE:
                    console.print(Panel(
                        "[yellow]No API keys configured![/]\n\n"
                        "This feature requires at least one LLM provider.\n"
                        "Go to [bold]Settings[/] to add your API keys.",
                        title="[yellow]⚠️ API Keys Required[/]",
                        border_style="yellow"
                    ))
                else:
                    print("\n⚠️ No API keys configured! Go to Settings to add your keys.\n")
                return None
            
            # Execute the feature (handle both sync and async)
            result = feature.run(ctx)
            
            if asyncio.iscoroutine(result):
                result = asyncio.run(result)
            
            return result
            
        except Exception as e:
            if RICH_AVAILABLE:
                console.print(f"[red]Error: {e}[/]")
            else:
                print(f"Error: {e}")
            return None


def main():
    """Entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Prompt Builder - Modern Prompt Engineering Techniques")
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed discovery logs and errors at startup"
    )
    args = parser.parse_args()
    
    if not RICH_AVAILABLE:
        print("💡 Tip: Install 'rich' for a better experience: pip install rich\n")
    
    app = PromptBuilderApp(verbose=args.verbose)
    app.run()


if __name__ == "__main__":
    main()
