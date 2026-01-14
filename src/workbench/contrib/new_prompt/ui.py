"""UI components for the new prompt feature."""

from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box

from src.core import PromptType, PromptConfig
from src.platform.clipboard import copy_to_clipboard, is_clipboard_available
from .common import TECHNIQUES

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


def select_technique(console: Console) -> tuple[Optional[PromptType], str]:
    """Let user select a prompt engineering technique."""
    menu_options = []
    for _, name, icon, _, desc in TECHNIQUES:
        menu_options.append(f"{icon} {name:<20} - {desc}")
    menu_options.append("🔙 Back to Main Menu")
    
    console.print("\n[bold]Select a technique[/] [dim](↑↓ to navigate, Enter to select)[/]\n")
    
    idx = interactive_select(menu_options, title="")
    
    if idx is None or idx == len(TECHNIQUES):
        return None, ""
    
    if 0 <= idx < len(TECHNIQUES):
        ptype, name, icon, color, _ = TECHNIQUES[idx]
        console.print(f"\n[{color}]✓ Selected: {icon} {name}[/]\n")
        return ptype, color
    
    return None, ""


def gather_config(console: Console, prompt_type: PromptType, color: str, 
                  builder, token_counter, preview_mode: bool) -> PromptConfig:
    """Gather configuration based on prompt type."""
    console.print(Panel(
        f"[bold]Configure your prompt[/]" + (" [dim](Preview Mode ON)[/]" if preview_mode else ""),
        border_style=color,
        box=box.ROUNDED
    ))
    
    task = Prompt.ask("\n[bold cyan]📝 What is your task/question?[/]")
    context = Prompt.ask("[bold blue]📖 Context[/] [dim](optional, Enter to skip)[/]", default="")
    
    config = PromptConfig(task=task, context=context)
    
    if preview_mode:
        show_preview(console, builder, token_counter, prompt_type, config, color)
    
    # Type-specific configuration
    if prompt_type == PromptType.FEW_SHOT:
        config.examples = gather_examples(console)
        if preview_mode:
            show_preview(console, builder, token_counter, prompt_type, config, color)
    elif prompt_type == PromptType.ROLE_BASED:
        config.role = Prompt.ask("[bold magenta]🎭 Role/Persona[/] [dim](e.g., 'senior Python developer')[/]", default="")
        if preview_mode:
            show_preview(console, builder, token_counter, prompt_type, config, color)
    elif prompt_type == PromptType.STRUCTURED:
        config.output_format = Prompt.ask("[bold yellow]📋 Output format[/] [dim](e.g., JSON, Markdown, Table)[/]", default="")
        if preview_mode:
            show_preview(console, builder, token_counter, prompt_type, config, color)
    
    if Confirm.ask("[bold]Add constraints?[/]", default=False):
        config.constraints = gather_constraints(console)
        if preview_mode:
            show_preview(console, builder, token_counter, prompt_type, config, color)
    
    return config


def gather_examples(console: Console) -> list[dict]:
    """Gather few-shot examples from user."""
    examples = []
    console.print("\n[bold green]📚 Provide examples[/] [dim](type 'done' when finished)[/]\n")
    
    while True:
        num = len(examples) + 1
        console.print(f"[bold]Example {num}[/]")
        inp = Prompt.ask("  [cyan]Input[/] [dim](or 'done')[/]")
        
        if inp.lower() == 'done':
            break
        
        out = Prompt.ask("  [green]Output[/]")
        examples.append({"input": inp, "output": out})
        console.print(f"  [dim]✓ Added[/]\n")
    
    return examples


def gather_constraints(console: Console) -> list[str]:
    """Gather constraints from user."""
    constraints = []
    console.print("\n[bold yellow]⚠️  Enter constraints[/] [dim](type 'done' when finished)[/]\n")
    
    while True:
        num = len(constraints) + 1
        c = Prompt.ask(f"  [yellow]Constraint {num}[/] [dim](or 'done')[/]")
        
        if c.lower() == 'done':
            break
        constraints.append(c)
    
    return constraints


def show_preview(console: Console, builder, token_counter, prompt_type: PromptType, 
                 config: PromptConfig, color: str) -> None:
    """Show a live preview of the prompt being built."""
    preview = builder.build(prompt_type, config)
    token_count = token_counter.count_tokens(preview)
    
    preview_text = preview[:500] + "..." if len(preview) > 500 else preview
    console.print()
    console.print(Panel(
        f"[dim]{preview_text}[/]",
        title=f"[dim]👁️ Preview ({token_count} tokens)[/]",
        border_style="dim",
        box=box.ROUNDED,
        padding=(0, 1)
    ))


def display_result(console: Console, prompt: str, color: str, token_counter, config) -> None:
    """Display the generated prompt with token estimates."""
    console.print()
    console.print(Panel(
        prompt,
        title="[bold bright_white]📝 Generated Prompt[/]",
        border_style=color,
        box=box.DOUBLE,
        padding=(1, 2)
    ))
    
    # Show token count
    token_count = token_counter.count_tokens(prompt)
    console.print(f"\n[dim]📊 Token count: ~{token_count} tokens[/]")


def ask_tags(console: Console) -> list[str]:
    """Ask for optional tags."""
    tags_input = Prompt.ask("\n[bold]🏷️  Tags[/] [dim](comma-separated, Enter to skip)[/]", default="")
    if tags_input:
        return [t.strip() for t in tags_input.split(",") if t.strip()]
    return []


def prompt_actions(console: Console, prompt_id: int, prompt: str, history) -> None:
    """Offer actions after prompt creation."""
    if is_clipboard_available():
        if copy_to_clipboard(prompt):
            console.print("[green]📋 Copied to clipboard![/]")
    
    while True:
        console.print("\n[bold]Actions:[/] [cyan]c[/]=copy [yellow]f[/]=favorite [dim]Enter[/]=continue")
        action = Prompt.ask("[bold]Action[/]", default="")
        
        if action == "c":
            if copy_to_clipboard(prompt):
                console.print("[green]📋 Copied to clipboard![/]")
            else:
                console.print("[red]Could not copy to clipboard[/]")
        elif action == "f":
            is_fav = history.toggle_favorite(prompt_id)
            status = "[yellow]⭐ Added to favorites[/]" if is_fav else "[dim]Removed from favorites[/]"
            console.print(status)
        else:
            break
