#!/usr/bin/env python3
"""
Prompt Builder - Create exceptional prompts using modern prompt engineering techniques.

Techniques included:
- Chain of Thought (CoT)
- Few-Shot Learning
- Role-Based Prompting
- Structured Output
- Self-Consistency
- Tree of Thoughts
- ReAct (Reasoning + Acting)
"""

from datetime import datetime
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich.text import Text
    from rich.markdown import Markdown
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from simple_term_menu import TerminalMenu
    MENU_AVAILABLE = True
except ImportError:
    MENU_AVAILABLE = False

from src.core import PromptBuilder, PromptConfig, PromptType
from src.platform.clipboard import copy_to_clipboard, is_clipboard_available
from src.services.token_counter import TokenCounter, is_tiktoken_available
from src.services.export import ExportService as PromptExporter, ExportMetadata as PromptMetadata, FORMAT_INFO as EXPORT_FORMATS, export_prompt
from src.services.llm.config import LLMConfig as APIConfig
from src.services.llm.client import LLMClient
from src.services.context import ContextManager

# Workbench discovery system - all features accessed through discovery
from src.workbench import (
    get_registry,
    reset_registry,
    CLIIntegration,
    FeatureCategory,
    FeatureContext,
    FeatureResult,
)

# Minimal imports for core functionality that main.py needs directly
# History and Analytics are needed for prompt saving and tracking
from src.workbench.contrib.history.service import HistoryService
from src.workbench.contrib.history.common import SavedPrompt
from src.workbench.contrib.analytics.service import PromptAnalytics

console = Console() if RICH_AVAILABLE else None


def interactive_select(options: list[str], title: str = "", multi_select: bool = False) -> int | list[int] | None:
    """Show an interactive selection menu.
    
    Args:
        options: List of menu option strings to display
        title: Optional title for the menu
        multi_select: Whether to allow multiple selections
        
    Returns:
        Single index for single-select, list of indices for multi-select, or None if cancelled
    """
    if MENU_AVAILABLE:
        menu = TerminalMenu(
            options,
            title=title,
            multi_select=multi_select,
            show_multi_select_hint=multi_select,
            multi_select_select_on_accept=False,
            multi_select_empty_ok=False,
        )
        result = menu.show()
        if multi_select:
            return list(menu.chosen_menu_indices) if menu.chosen_menu_indices else None
        return result
    else:
        # Fallback to numbered input
        print(f"\n{title}" if title else "")
        for i, opt in enumerate(options, 1):
            print(f"  [{i}] {opt}")
        try:
            if multi_select:
                choices = input("Select numbers (space-separated): ").strip().split()
                return [int(c) - 1 for c in choices if c.isdigit() and 0 < int(c) <= len(options)]
            else:
                choice = input("Select: ").strip()
                idx = int(choice) - 1
                return idx if 0 <= idx < len(options) else None
        except (ValueError, IndexError):
            return None


class InteractivePromptBuilder:
    """Interactive CLI for building prompts with rich formatting."""

    TECHNIQUES = [
        (PromptType.CHAIN_OF_THOUGHT, "Chain of Thought", "🧠", "cyan", 
         "Step-by-step reasoning for complex problems"),
        (PromptType.FEW_SHOT, "Few-Shot Learning", "📚", "green",
         "Learn patterns from examples you provide"),
        (PromptType.ROLE_BASED, "Role-Based", "🎭", "magenta",
         "Assign expert persona for domain-specific tasks"),
        (PromptType.STRUCTURED, "Structured Output", "📋", "yellow",
         "Get responses in specific formats (JSON, etc.)"),
        (PromptType.REACT, "ReAct", "⚡", "red",
         "Reasoning + Acting for multi-step problem solving"),
        (PromptType.TREE_OF_THOUGHTS, "Tree of Thoughts", "🌳", "blue",
         "Explore multiple solution paths systematically"),
        (PromptType.SELF_CONSISTENCY, "Self-Consistency", "🔄", "white",
         "Multiple solutions for verification & consensus"),
    ]

    def __init__(self, verbose: bool = False):
        self.builder = PromptBuilder()
        self.token_counter = TokenCounter()
        self.preview_mode = False
        self.verbose = verbose
        
        # Core services needed for prompt building
        self.api_config = APIConfig()
        self.llm_client = LLMClient(self.api_config)
        self.context_manager = ContextManager()
        
        # History and analytics are core services used across the app
        self.history = HistoryService()
        self.analytics = PromptAnalytics()
        
        # Initialize the feature registry at startup (Requirements: 3.1, 3.3)
        self.registry = get_registry()
        
        # Initialize CLI integration for discovered features
        self.cli_integration = CLIIntegration(
            console=console,
            llm_client=self.llm_client,
            history=self.history,
            config=self.api_config,
            analytics=self.analytics,
            prompt_builder=self.builder,
            registry=self.registry,
        )
        
        if not RICH_AVAILABLE:
            print("[yellow]Install 'rich' for the best experience: pip install rich[/]")

    def run(self):
        """Run the interactive prompt builder."""
        self._show_header()
        
        # Show discovery errors/warnings at startup if verbose (Requirements: 10.3, 10.4)
        if self.verbose and self.cli_integration.has_discovery_issues():
            self.cli_integration.show_discovery_errors()

        while True:
            action = self._show_main_menu()
            
            if action == "quit":
                self._show_goodbye()
                break
            elif action == "new":
                self._create_new_prompt()
            elif action == "combine":
                self._combine_techniques()
            elif action == "templates":
                self._use_custom_template()
            elif action == "history":
                self._browse_history()
            elif action == "favorites":
                self._browse_favorites()
            elif action == "search":
                self._search_prompts()
            elif action == "preview":
                self._toggle_preview_mode()
            elif action == "ai":
                self._ai_features_menu()
            elif action == "settings":
                self._settings_menu()

    def _use_custom_template(self) -> None:
        """Use a custom template to create a prompt via the discovery system."""
        # Get the templates feature from the registry
        templates_feature = self.registry.get("templates")
        if templates_feature is None:
            if RICH_AVAILABLE:
                console.print("[red]Templates feature not available[/]")
            else:
                print("Templates feature not available")
            return
        
        # Execute the templates feature through the discovery system
        result = self.cli_integration.execute_feature_sync(templates_feature)
        
        if not result.success and result.error:
            if RICH_AVAILABLE:
                console.print(f"[red]Error: {result.error}[/]")
            else:
                print(f"Error: {result.error}")

    def _show_main_menu(self) -> str:
        """Show main menu and return selected action."""
        has_ai = self.api_config.has_any_provider()
        ai_indicator = "●" if has_ai else "○"
        preview_status = "ON" if self.preview_mode else "OFF"
        
        menu_options = [
            "✨ New Prompt         - Create a new prompt manually",
            "🔗 Combine            - Chain multiple techniques",
            "📦 Templates          - Use custom templates",
            "📜 History            - Browse recent prompts",
            "⭐ Favorites          - View favorite prompts",
            "🔍 Search             - Search saved prompts",
            f"👁️  Preview Mode [{preview_status}]  - Live prompt preview",
            f"🤖 AI Features [{ai_indicator}]    - Optimize, generate, test, chains",
            "⚙️  Settings           - API keys & configuration",
            "🚪 Quit               - Exit the builder",
        ]
        
        actions = ["new", "combine", "templates", "history", "favorites", 
                   "search", "preview", "ai", "settings", "quit"]
        
        if RICH_AVAILABLE:
            console.print("\n[bold]Main Menu[/] [dim](↑↓ to navigate, Enter to select)[/]\n")
        
        idx = interactive_select(menu_options, title="")
        
        if idx is not None and 0 <= idx < len(actions):
            return actions[idx]
        return "new"

    def _create_new_prompt(self):
        """Create a new prompt flow."""
        prompt_type, color = self._select_prompt_type()
        if prompt_type is None:
            return

        config = self._gather_config(prompt_type, color)
        result = self.builder.build(prompt_type, config)

        self._display_result(result, color)
        
        # Auto-save to history
        tags = self._ask_tags()
        prompt_id = self.history.save(
            technique=prompt_type.value,
            task=config.task,
            prompt=result,
            tags=tags
        )
        
        if RICH_AVAILABLE:
            console.print(f"[dim]💾 Auto-saved to history (ID: {prompt_id})[/]")
        
        # Offer additional actions
        self._prompt_actions(prompt_id, result, color)

    def _combine_techniques(self):
        """Combine multiple techniques into a mega-prompt."""
        if RICH_AVAILABLE:
            console.print(Panel(
                "[bold]🔗 Prompt Combiner[/]\n[dim]Chain multiple techniques into one powerful prompt[/]",
                border_style="bright_cyan",
                box=box.ROUNDED
            ))
            console.print("[dim]Select techniques to combine (enter numbers separated by spaces)[/]\n")
        else:
            print("\n🔗 Prompt Combiner")
            print("Select techniques to combine (enter numbers separated by spaces)\n")
        
        # Show technique options
        if RICH_AVAILABLE:
            table = Table(box=box.ROUNDED, border_style="dim", show_header=False, padding=(0, 2))
            table.add_column("Key", style="bold bright_white", width=5)
            table.add_column("Technique", width=22)
            table.add_column("Adds", style="dim")
            
            combo_info = [
                ("Role-Based", "Expert persona context"),
                ("Chain of Thought", "Step-by-step reasoning"),
                ("Few-Shot", "Learning examples"),
                ("Structured", "Output format requirements"),
                ("ReAct", "Reasoning + action framework"),
                ("Tree of Thoughts", "Multi-path exploration"),
                ("Self-Consistency", "Verification approach"),
            ]
            for i, (ptype, name, icon, color, _) in enumerate(self.TECHNIQUES, 1):
                table.add_row(f"[{color}]{i}[/]", f"{icon} [{color}]{name}[/]", combo_info[i-1][1])
            console.print(table)
            console.print()
            choices = Prompt.ask("[bold]Techniques to combine[/] [dim](e.g., 3 1 4)[/]", default="3 1")
        else:
            for i, (_, name, icon, _, _) in enumerate(self.TECHNIQUES, 1):
                print(f"  [{i}] {icon} {name}")
            choices = input("\nTechniques to combine (e.g., 3 1 4): ").strip()
        
        # Parse selections
        try:
            indices = [int(x) - 1 for x in choices.split()]
            selected = [(self.TECHNIQUES[i][0], self.TECHNIQUES[i][1], self.TECHNIQUES[i][3]) 
                       for i in indices if 0 <= i < len(self.TECHNIQUES)]
        except (ValueError, IndexError):
            if RICH_AVAILABLE:
                console.print("[red]Invalid selection[/]")
            return
        
        if len(selected) < 2:
            if RICH_AVAILABLE:
                console.print("[yellow]Select at least 2 techniques to combine[/]")
            return
        
        # Get the task
        if RICH_AVAILABLE:
            selected_names = " + ".join([f"[{c}]{n}[/]" for _, n, c in selected])
            console.print(f"\n[bold]Combining:[/] {selected_names}\n")
            task = Prompt.ask("[bold cyan]📝 What is your task/question?[/]")
            context = Prompt.ask("[bold blue]📖 Context[/] [dim](optional)[/]", default="")
        else:
            print(f"\nCombining: {' + '.join([n for _, n, _ in selected])}\n")
            task = input("📝 What is your task/question?\n> ").strip()
            context = input("\n📖 Context (optional):\n> ").strip()
        
        # Build combined prompt
        combined_parts = []
        combined_parts.append("=" * 50)
        combined_parts.append("COMBINED PROMPT - Multiple Techniques")
        combined_parts.append("=" * 50)
        
        if context:
            combined_parts.append(f"\nContext: {context}")
        combined_parts.append(f"\nTask: {task}")
        combined_parts.append("\n" + "-" * 50)
        
        for ptype, name, _ in selected:
            config = PromptConfig(task=task, context=context)
            section = self.builder.build(ptype, config)
            combined_parts.append(f"\n## {name.upper()} APPROACH ##\n")
            combined_parts.append(section)
            combined_parts.append("\n" + "-" * 50)
        
        combined_parts.append("\nSynthesize insights from all approaches above to provide a comprehensive answer.")
        
        result = "\n".join(combined_parts)
        
        self._display_result(result, "bright_cyan")
        
        # Save to history
        tags = self._ask_tags()
        technique_names = "+".join([p.value for p, _, _ in selected])
        prompt_id = self.history.save(
            technique=f"combined:{technique_names}",
            task=task,
            prompt=result,
            tags=tags
        )
        
        if RICH_AVAILABLE:
            console.print(f"[dim]💾 Auto-saved to history (ID: {prompt_id})[/]")
        
        self._prompt_actions(prompt_id, result, "bright_cyan")

    def _ask_tags(self) -> list[str]:
        """Ask for optional tags."""
        if RICH_AVAILABLE:
            tags_input = Prompt.ask("\n[bold]🏷️  Tags[/] [dim](comma-separated, Enter to skip)[/]", default="")
        else:
            tags_input = input("\n🏷️  Tags (comma-separated, Enter to skip): ").strip()
        
        if tags_input:
            return [t.strip() for t in tags_input.split(",") if t.strip()]
        return []

    def _prompt_actions(self, prompt_id: int, prompt: str, color: str):
        """Offer actions after prompt creation."""
        # Auto-copy to clipboard
        if is_clipboard_available():
            if copy_to_clipboard(prompt):
                if RICH_AVAILABLE:
                    console.print("[green]📋 Copied to clipboard![/]")
                else:
                    print("📋 Copied to clipboard!")
        
        while True:
            if RICH_AVAILABLE:
                console.print("\n[bold]Actions:[/] [cyan]c[/]=copy [yellow]f[/]=favorite [green]s[/]=save file [dim]Enter[/]=continue")
                action = Prompt.ask("[bold]Action[/]", default="")
            else:
                print("\nActions: [c]=copy [f]=favorite [s]=save file [Enter]=continue")
                action = input("Action: ").strip().lower()

            if action == "c":
                if copy_to_clipboard(prompt):
                    if RICH_AVAILABLE:
                        console.print("[green]📋 Copied to clipboard![/]")
                    else:
                        print("📋 Copied to clipboard!")
                else:
                    if RICH_AVAILABLE:
                        console.print("[red]Could not copy to clipboard[/]")
            elif action == "f":
                is_fav = self.history.toggle_favorite(prompt_id)
                if RICH_AVAILABLE:
                    status = "[yellow]⭐ Added to favorites[/]" if is_fav else "[dim]Removed from favorites[/]"
                    console.print(status)
                else:
                    print("⭐ Toggled favorite status")
            elif action == "s":
                self._save_to_file(prompt)
            else:
                break

    def _browse_history(self) -> None:
        """Browse recent prompts via the discovery system."""
        # Get the history feature from the registry
        history_feature = self.registry.get("history")
        if history_feature is None:
            # Fallback to direct history access
            prompts = self.history.list_recent(15)
            if not prompts:
                if RICH_AVAILABLE:
                    console.print("[dim]No prompts in history yet.[/]\n")
                else:
                    print("No prompts in history yet.\n")
                return
            self._display_prompt_list(prompts, "📜 Recent Prompts")
            self._select_from_list(prompts)
            return
        
        # Execute the history feature through the discovery system
        result = self.cli_integration.execute_feature_sync(history_feature)
        
        if not result.success and result.error:
            if RICH_AVAILABLE:
                console.print(f"[red]Error: {result.error}[/]")
            else:
                print(f"Error: {result.error}")

    def _browse_favorites(self) -> None:
        """Browse favorite prompts."""
        # Use direct history access for favorites (quick access)
        prompts = self.history.list_favorites()
        if not prompts:
            if RICH_AVAILABLE:
                console.print("[dim]No favorites yet. Create prompts and mark them as favorites![/]\n")
            else:
                print("No favorites yet.\n")
            return
        
        self._display_prompt_list(prompts, "⭐ Favorite Prompts")
        self._select_from_list(prompts)

    def _search_prompts(self) -> None:
        """Search saved prompts."""
        if RICH_AVAILABLE:
            query = Prompt.ask("[bold magenta]🔍 Search[/]")
        else:
            query = input("🔍 Search: ").strip()
        
        prompts = self.history.search(query)
        if not prompts:
            if RICH_AVAILABLE:
                console.print(f"[dim]No prompts found for '{query}'[/]\n")
            else:
                print(f"No prompts found for '{query}'\n")
            return
        
        self._display_prompt_list(prompts, f"🔍 Results for '{query}'")
        self._select_from_list(prompts)

    def _display_prompt_list(self, prompts: list[SavedPrompt], title: str):
        """Display a list of prompts."""
        if RICH_AVAILABLE:
            table = Table(title=title, box=box.ROUNDED, border_style="dim")
            table.add_column("#", style="bold", width=4)
            table.add_column("Technique", width=12)
            table.add_column("Task", width=35)
            table.add_column("Tags", style="dim", width=15)
            table.add_column("⭐", width=3)
            
            for i, p in enumerate(prompts, 1):
                fav = "⭐" if p.is_favorite else ""
                task_preview = p.task[:32] + "..." if len(p.task) > 35 else p.task
                tags = ", ".join(p.tags[:3]) if p.tags else ""
                table.add_row(str(i), p.technique, task_preview, tags, fav)
            
            console.print(table)
        else:
            print(f"\n{title}\n" + "-" * 50)
            for i, p in enumerate(prompts, 1):
                fav = "⭐" if p.is_favorite else "  "
                task_preview = p.task[:40] + "..." if len(p.task) > 40 else p.task
                print(f"{i}. {fav} [{p.technique}] {task_preview}")

    def _select_from_list(self, prompts: list[SavedPrompt]) -> None:
        """Let user select a prompt from the list."""
        if RICH_AVAILABLE:
            choice = Prompt.ask("\n[bold]Select #[/] [dim](or Enter to go back)[/]", default="")
        else:
            choice = input("\nSelect # (or Enter to go back): ").strip()
        
        if not choice:
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(prompts):
                self._view_prompt(prompts[idx])
        except ValueError:
            pass

    def _view_prompt(self, saved: SavedPrompt) -> None:
        """View a saved prompt with actions."""
        color = "cyan"
        for ptype, _, _, c, _ in self.TECHNIQUES:
            if ptype.value == saved.technique:
                color = c
                break
        
        if RICH_AVAILABLE:
            console.print(Panel(
                saved.prompt,
                title=f"[bold]{saved.technique.upper()}[/] - {saved.task[:40]}",
                subtitle=f"[dim]ID: {saved.id} | Created: {saved.created_at.strftime('%Y-%m-%d %H:%M')}[/]",
                border_style=color,
                box=box.DOUBLE,
                padding=(1, 2)
            ))
        else:
            print(f"\n{'=' * 50}")
            print(f"[{saved.technique}] {saved.task}")
            print(f"{'=' * 50}")
            print(saved.prompt)
            print(f"{'=' * 50}")
        
        # Actions
        while True:
            if RICH_AVAILABLE:
                console.print("\n[bold]Actions:[/] [cyan]c[/]=copy [yellow]f[/]=toggle favorite [green]s[/]=save file [red]d[/]=delete [dim]b[/]=back")
                action = Prompt.ask("[bold]Action[/]", default="b")
            else:
                print("\nActions: [c]=copy [f]=favorite [s]=save [d]=delete [b]=back")
                action = input("Action: ").strip().lower()

            if action == "c":
                if copy_to_clipboard(saved.prompt):
                    if RICH_AVAILABLE:
                        console.print("[green]📋 Copied to clipboard![/]")
                    else:
                        print("📋 Copied to clipboard!")
            elif action == "f":
                is_fav = self.history.toggle_favorite(saved.id)
                if RICH_AVAILABLE:
                    console.print("[yellow]⭐ Favorite toggled[/]" if is_fav else "[dim]Removed from favorites[/]")
            elif action == "s":
                self._save_to_file(saved.prompt)
            elif action == "d":
                if self._confirm("[red]Delete this prompt?[/]"):
                    self.history.delete(saved.id)
                    if RICH_AVAILABLE:
                        console.print("[red]🗑️  Deleted[/]")
                    break
            elif action == "b":
                break

    def _save_to_file(self, prompt: str, technique: str = "unknown", task: str = "") -> None:
        """Save prompt to file with format selection."""
        # Show format options
        if RICH_AVAILABLE:
            console.print("\n[bold]Export Formats:[/]")
            table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
            table.add_column("Key", style="cyan", width=4)
            table.add_column("Format", width=20)
            
            format_keys = list(EXPORT_FORMATS.keys())
            for i, key in enumerate(format_keys, 1):
                name, ext = EXPORT_FORMATS[key]
                table.add_row(str(i), f"{name} ({ext})")
            console.print(table)
            
            choice = Prompt.ask("[bold]Format[/]", default="1")
        else:
            print("\nExport Formats:")
            format_keys = list(EXPORT_FORMATS.keys())
            for i, key in enumerate(format_keys, 1):
                name, ext = EXPORT_FORMATS[key]
                print(f"  [{i}] {name} ({ext})")
            choice = input("Format (1): ").strip() or "1"
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(format_keys):
                format_key = format_keys[idx]
            else:
                format_key = "txt"
        except ValueError:
            format_key = "txt"
        
        # Create metadata
        metadata = PromptMetadata(
            technique=technique,
            task=task[:50] if task else "prompt",
            created_at=datetime.now().isoformat()
        )
        
        # Export
        content, extension = export_prompt(prompt, format_key, metadata)
        
        # Get filename
        default_name = f"prompt{extension}"
        if RICH_AVAILABLE:
            filename = Prompt.ask("[dim]Filename[/]", default=default_name)
        else:
            filename = input(f"Filename ({default_name}): ").strip() or default_name
        
        with open(filename, 'w') as f:
            f.write(content)
        
        if RICH_AVAILABLE:
            console.print(f"[bold green]✅ Exported to {filename}[/]")
        else:
            print(f"✅ Exported to {filename}")

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

    def _show_goodbye(self) -> None:
        """Display goodbye message."""
        if RICH_AVAILABLE:
            console.print(Panel(
                "[bold green]Happy prompting! 🎯[/]\n[dim]May your tokens be ever efficient.[/]",
                border_style="green",
                box=box.ROUNDED
            ))
        else:
            print("\nGoodbye! Happy prompting! 🎯")

    def _select_prompt_type(self) -> tuple[Optional[PromptType], str]:
        """Let user select a prompt engineering technique."""
        # Build menu options
        menu_options = []
        for _, name, icon, _, desc in self.TECHNIQUES:
            menu_options.append(f"{icon} {name:<20} - {desc}")
        menu_options.append("🚪 Back to Main Menu")
        
        if RICH_AVAILABLE:
            console.print("\n[bold]Select a technique[/] [dim](↑↓ to navigate, Enter to select)[/]\n")
        
        idx = interactive_select(menu_options, title="")
        
        if idx is None or idx == len(self.TECHNIQUES):  # Back/Quit
            return None, ""
        
        if 0 <= idx < len(self.TECHNIQUES):
            ptype, name, icon, color, _ = self.TECHNIQUES[idx]
            if RICH_AVAILABLE:
                console.print(f"\n[{color}]✓ Selected: {icon} {name}[/]\n")
            else:
                print(f"\n✓ Selected: {icon} {name}\n")
            return ptype, color
        
        return None, ""

    def _gather_config(self, prompt_type: PromptType, color: str) -> PromptConfig:
        """Gather configuration based on prompt type with optional live preview."""
        if RICH_AVAILABLE:
            console.print(Panel(
                f"[bold]Configure your prompt[/]" + (" [dim](Preview Mode ON)[/]" if self.preview_mode else ""),
                border_style=color,
                box=box.ROUNDED
            ))
            task = Prompt.ask("\n[bold cyan]📝 What is your task/question?[/]")
            context = Prompt.ask("[bold blue]📖 Context[/] [dim](optional, Enter to skip)[/]", default="")
        else:
            print(f"\n--- Configure {prompt_type.name} ---\n")
            task = input("📝 What is your task/question?\n> ").strip()
            context = input("\n📖 Context (optional, Enter to skip):\n> ").strip()

        config = PromptConfig(task=task, context=context)
        
        # Show preview after basic config
        if self.preview_mode:
            self._show_live_preview(prompt_type, config, color)

        # Type-specific configuration
        if prompt_type == PromptType.FEW_SHOT:
            config.examples = self._gather_examples()
            if self.preview_mode:
                self._show_live_preview(prompt_type, config, color)
        elif prompt_type == PromptType.ROLE_BASED:
            config.role = self._ask("[bold magenta]🎭 Role/Persona[/]", 
                                    "e.g., 'senior Python developer'")
            if self.preview_mode:
                self._show_live_preview(prompt_type, config, color)
        elif prompt_type == PromptType.STRUCTURED:
            config.output_format = self._ask("[bold yellow]📋 Output format[/]",
                                             "e.g., JSON, Markdown, Table")
            if self.preview_mode:
                self._show_live_preview(prompt_type, config, color)

        # Optional constraints
        if self._confirm("[bold]Add constraints?[/]"):
            config.constraints = self._gather_constraints()
            if self.preview_mode:
                self._show_live_preview(prompt_type, config, color)

        return config

    def _show_live_preview(self, prompt_type: PromptType, config: PromptConfig, color: str) -> None:
        """Show a live preview of the prompt being built."""
        preview = self.builder.build(prompt_type, config)
        token_count = self.token_counter.count_tokens(preview)
        
        if RICH_AVAILABLE:
            # Truncate for preview
            preview_text = preview[:500] + "..." if len(preview) > 500 else preview
            console.print()
            console.print(Panel(
                f"[dim]{preview_text}[/]",
                title=f"[dim]👁️ Preview ({token_count} tokens)[/]",
                border_style="dim",
                box=box.ROUNDED,
                padding=(0, 1)
            ))
        else:
            preview_text = preview[:300] + "..." if len(preview) > 300 else preview
            print(f"\n--- Preview ({token_count} tokens) ---")
            print(preview_text)
            print("---")

    def _toggle_preview_mode(self) -> None:
        """Toggle live preview mode."""
        self.preview_mode = not self.preview_mode
        status = "ON" if self.preview_mode else "OFF"
        if RICH_AVAILABLE:
            console.print(f"[bold]👁️ Preview Mode: [{'green' if self.preview_mode else 'red'}]{status}[/]")
        else:
            print(f"👁️ Preview Mode: {status}")

    def _ask(self, label: str, hint: str = "") -> str:
        """Ask for input with rich formatting."""
        if RICH_AVAILABLE:
            hint_text = f" [dim]({hint})[/]" if hint else ""
            return Prompt.ask(f"{label}{hint_text}", default="")
        else:
            hint_text = f" ({hint})" if hint else ""
            return input(f"{label}{hint_text}: ").strip()

    def _confirm(self, message: str) -> bool:
        """Ask for confirmation."""
        if RICH_AVAILABLE:
            return Confirm.ask(message, default=False)
        else:
            return input(f"{message} (y/n): ").strip().lower() == 'y'

    def _gather_examples(self) -> list[dict]:
        """Gather few-shot examples from user."""
        examples = []
        if RICH_AVAILABLE:
            console.print("\n[bold green]📚 Provide examples[/] [dim](type 'done' when finished)[/]\n")
        else:
            print("\nProvide examples (type 'done' when finished):\n")

        while True:
            num = len(examples) + 1
            if RICH_AVAILABLE:
                console.print(f"[bold]Example {num}[/]")
                inp = Prompt.ask("  [cyan]Input[/] [dim](or 'done')[/]")
            else:
                inp = input(f"Example {num} - Input (or 'done'): ").strip()

            if inp.lower() == 'done':
                break

            if RICH_AVAILABLE:
                out = Prompt.ask("  [green]Output[/]")
            else:
                out = input(f"Example {num} - Output: ").strip()

            examples.append({"input": inp, "output": out})
            if RICH_AVAILABLE:
                console.print(f"  [dim]✓ Added[/]\n")

        return examples

    def _gather_constraints(self) -> list[str]:
        """Gather constraints from user."""
        constraints = []
        if RICH_AVAILABLE:
            console.print("\n[bold yellow]⚠️  Enter constraints[/] [dim](type 'done' when finished)[/]\n")
        else:
            print("\nEnter constraints (type 'done' when finished):\n")

        while True:
            num = len(constraints) + 1
            if RICH_AVAILABLE:
                c = Prompt.ask(f"  [yellow]Constraint {num}[/] [dim](or 'done')[/]")
            else:
                c = input(f"Constraint {num} (or 'done'): ").strip()

            if c.lower() == 'done':
                break
            constraints.append(c)

        return constraints

    def _display_result(self, prompt: str, color: str) -> None:
        """Display the generated prompt with token estimates."""
        if RICH_AVAILABLE:
            console.print()
            console.print(Panel(
                prompt,
                title="[bold bright_white]📝 Generated Prompt[/]",
                border_style=color,
                box=box.DOUBLE,
                padding=(1, 2)
            ))
            # Show token estimates
            self._show_token_estimates(prompt)
        else:
            print("\n" + "=" * 50)
            print("📝 GENERATED PROMPT:")
            print("=" * 50)
            print(prompt)
            print("=" * 50)
            self._show_token_estimates(prompt)

    def _show_token_estimates(self, prompt: str) -> None:
        """Display token count and cost estimates for available providers only."""
        available_providers = self.api_config.get_available_providers()
        
        if not available_providers:
            # No API keys configured - show a simple token count
            token_count = self.token_counter.count_tokens(prompt)
            if RICH_AVAILABLE:
                console.print(f"\n[dim]📊 Token count: ~{token_count} tokens[/]")
                console.print("[dim]Configure API keys in Settings to see cost estimates[/]")
            else:
                print(f"\n📊 Token count: ~{token_count} tokens")
                print("Configure API keys in Settings to see cost estimates")
            return
        
        estimates = self.token_counter.estimate_for_providers(prompt, available_providers)
        
        if not estimates:
            return
        
        if RICH_AVAILABLE:
            table = Table(box=box.SIMPLE, border_style="dim", show_header=True, padding=(0, 1))
            table.add_column("Model", style="cyan", width=28)
            table.add_column("Tokens", justify="right", width=8)
            table.add_column("Input Cost", justify="right", style="green", width=10)
            
            for est in estimates:
                # Shorten model name for display
                display_name = est.model
                if len(display_name) > 26:
                    display_name = display_name[:24] + ".."
                table.add_row(
                    display_name,
                    str(est.token_count),
                    est.formatted_cost,
                )
            
            console.print(Panel(table, title="[dim]💰 Token Estimates[/]", border_style="dim", box=box.ROUNDED))
        else:
            print("\n💰 Token Estimates:")
            for est in estimates:
                print(f"  {est.model:<28} {est.token_count:>6} tokens  {est.formatted_cost}")

    def _continue_prompt(self) -> bool:
        """Ask if user wants to create another prompt."""
        if RICH_AVAILABLE:
            console.print()
        return self._confirm("[bold]Create another prompt?[/]")

    # ==================== AI FEATURES ====================

    def _select_model_for_feature(self, feature_name: str = "this feature") -> tuple[Optional[str], Optional[str]]:
        """Prompt user to select a model if multiple providers are available.
        
        Args:
            feature_name: Name of the feature for display purposes
            
        Returns:
            Tuple of (provider, model) or (None, None) if no providers available
        """
        # If only one provider or no multiple providers, use default
        if not self.api_config.has_multiple_providers():
            return self.api_config.get_default_model()
        
        available_models = self.api_config.get_available_models()
        default_provider, default_model = self.api_config.get_default_model()
        
        # Build menu options
        menu_options = []
        for provider, model in available_models:
            is_default = provider == default_provider and model == default_model
            marker = " (default)" if is_default else ""
            menu_options.append(f"{provider}: {model}{marker}")
        
        if RICH_AVAILABLE:
            console.print(f"\n[dim]Select model for {feature_name}:[/]")
        else:
            print(f"\nSelect model for {feature_name}:")
        
        idx = interactive_select(menu_options, title="")
        
        if idx is not None and 0 <= idx < len(available_models):
            return available_models[idx]
        
        return default_provider, default_model

    def _ai_features_menu(self) -> None:
        """Show AI-powered features menu using the discovery system.
        
        Requirements: 5.1, 5.4
        """
        has_api_key = self.api_config.has_any_provider()
        
        if not has_api_key:
            if RICH_AVAILABLE:
                console.print(Panel(
                    "[yellow]No API keys configured![/]\n\n"
                    "AI features require at least one LLM provider.\n"
                    "Go to [bold]Settings[/] to add your API keys.",
                    title="[yellow]⚠️ API Keys Required[/]",
                    border_style="yellow"
                ))
            else:
                print("\n⚠️ No API keys configured! Go to Settings to add your keys.\n")
            return

        # Get AI features from the registry
        ai_features = self.registry.list_by_category(FeatureCategory.AI)
        
        while True:
            if RICH_AVAILABLE:
                console.print("\n[bold]🤖 AI Features[/] [dim](↑↓ to navigate, Enter to select)[/]\n")
                
                # Use CLIIntegration to render the AI features menu
                self.cli_integration.render_feature_menu(
                    title="AI Features",
                    category=FeatureCategory.AI,
                    has_api_key=has_api_key,
                )
                console.print()
            
            # Build menu options from discovered features
            menu_options = []
            for feature in ai_features:
                m = feature.manifest
                menu_options.append(f"{m.icon} {m.display_name:<24} - {m.description}")
            menu_options.append("🔙 Back                       - Return to main menu")
            
            idx = interactive_select(menu_options, title="")
            
            if idx is None or idx == len(ai_features):  # Back
                break
            
            if idx is not None and 0 <= idx < len(ai_features):
                # Execute the selected feature using CLIIntegration
                selected_feature = ai_features[idx]
                result = self.cli_integration.execute_feature_sync(selected_feature)
                
                if not result.success and result.error:
                    if RICH_AVAILABLE:
                        console.print(f"[red]Error: {result.error}[/]")
                    else:
                        print(f"Error: {result.error}")

    # ==================== SETTINGS ====================

    def _settings_menu(self) -> None:
        """Settings and configuration menu."""
        while True:
            default_provider, default_model = self.api_config.get_default_model()
            
            # Build status display
            status_lines = []
            for name, provider in self.api_config.providers.items():
                status = "✓" if provider.is_available else "✗"
                status_lines.append(f"{name.capitalize()}: {status}")
            
            default_display = f"{default_provider}/{default_model}" if default_provider else "Not set"
            
            if RICH_AVAILABLE:
                console.print("\n[bold]⚙️ Settings[/]\n")
                console.print(f"API Keys: {' | '.join(status_lines)}")
                console.print(f"Default Model: {default_display}\n")
            else:
                print("\n⚙️ Settings\n")
                print(f"API Keys: {' | '.join(status_lines)}")
                print(f"Default Model: {default_display}\n")
            
            menu_options = [
                "🔑 Set OpenAI API Key",
                "🔑 Set Anthropic API Key", 
                "🔑 Set Google API Key",
                "🎯 Set Default Model",
                "🔙 Back",
            ]
            
            idx = interactive_select(menu_options, title="")
            
            if idx is None or idx == 4:  # Back
                break
            elif idx == 0:
                self._set_api_key("openai")
            elif idx == 1:
                self._set_api_key("anthropic")
            elif idx == 2:
                self._set_api_key("google")
            elif idx == 3:
                self._set_default_model()

    def _set_default_model(self) -> None:
        """Set the default model for AI features."""
        available_models = self.api_config.get_available_models()
        
        if not available_models:
            if RICH_AVAILABLE:
                console.print("[yellow]No API keys configured. Add keys first.[/]")
            else:
                print("No API keys configured. Add keys first.")
            return
        
        model_info = {
            # OpenAI
            "gpt-4.1": "Flagship, 1M context",
            "gpt-4.1-mini": "Balanced",
            "gpt-4.1-nano": "Cheapest, fast",
            "o4-mini": "Reasoning model",
            "gpt-4o": "Legacy",
            # Anthropic
            "claude-sonnet-4-5-20250929": "Best balance",
            "claude-opus-4-5-20251124": "Most capable",
            "claude-haiku-4-5-20251015": "Cheapest, fast",
            # Google
            "gemini-2.5-pro": "Most capable",
            "gemini-2.5-flash": "Fast, balanced",
            "gemini-2.5-flash-lite": "Cheapest, fast",
        }
        
        # Build menu options
        menu_options = []
        for provider, model in available_models:
            info = model_info.get(model, "")
            info_str = f" ({info})" if info else ""
            menu_options.append(f"{provider}: {model}{info_str}")
        
        if RICH_AVAILABLE:
            console.print("\n[bold]Select Default Model[/]\n")
        
        idx = interactive_select(menu_options, title="")
        
        if idx is not None and 0 <= idx < len(available_models):
            provider, model = available_models[idx]
            self.api_config.set_default_model(provider, model)
            # Reinitialize LLM client with new config
            self.llm_client = LLMClient(self.api_config)
            # Update CLI integration context
            self.cli_integration.context.llm_client = self.llm_client
            
            if RICH_AVAILABLE:
                console.print(f"\n[green]✓ Default set to {provider} / {model}[/]")
            else:
                print(f"\n✓ Default set to {provider} / {model}")

    def _set_api_key(self, provider: str) -> None:
        """Set API key for a provider."""
        if RICH_AVAILABLE:
            key = Prompt.ask(f"[bold]Enter {provider.capitalize()} API key[/]", password=True)
        else:
            key = input(f"Enter {provider.capitalize()} API key: ").strip()
        
        if key:
            self.api_config.set_api_key(provider, key)
            # Reinitialize LLM client with new config
            self.llm_client = LLMClient(self.api_config)
            # Update CLI integration context
            self.cli_integration.context.llm_client = self.llm_client
            
            if RICH_AVAILABLE:
                console.print(f"[green]✓ {provider.capitalize()} API key saved[/]")
            else:
                print(f"✓ {provider.capitalize()} API key saved")


def quick_build(
    technique: str,
    task: str,
    context: str = "",
    role: str = "",
    examples: list[dict] = None,
    output_format: str = "",
    constraints: list[str] = None
) -> str:
    """
    Quick function to build prompts programmatically.

    Args:
        technique: One of 'cot', 'few_shot', 'role', 'structured', 'react', 'tot', 'self_consistency'
        task: The main task or question
        context: Optional background context
        role: Role/persona (for role-based prompts)
        examples: List of {"input": ..., "output": ...} dicts (for few-shot)
        output_format: Desired format (for structured prompts)
        constraints: List of constraints to include

    Returns:
        Generated prompt string
    """
    builder = PromptBuilder()
    prompt_type = PromptType(technique)
    config = PromptConfig(
        task=task,
        context=context,
        role=role,
        examples=examples or [],
        output_format=output_format,
        constraints=constraints or []
    )
    return builder.build(prompt_type, config)


if __name__ == "__main__":
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
    app = InteractivePromptBuilder(verbose=args.verbose)
    app.run()
