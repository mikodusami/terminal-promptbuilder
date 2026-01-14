"""UI components for the combine feature."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

from src.core import PromptType, PromptConfig
from src.platform.clipboard import copy_to_clipboard, is_clipboard_available
from src.workbench.contrib.new_prompt.common import TECHNIQUES


def show_technique_table(console: Console) -> None:
    """Display technique options in a table."""
    table = Table(box=box.ROUNDED, border_style="dim", show_header=False, padding=(0, 2))
    table.add_column("Key", style="bold bright_white", width=5)
    table.add_column("Technique", width=22)
    table.add_column("Adds", style="dim")
    
    combo_info = [
        "Step-by-step reasoning",
        "Learning examples",
        "Expert persona context",
        "Output format requirements",
        "Reasoning + action framework",
        "Multi-path exploration",
        "Verification approach",
    ]
    
    for i, (ptype, name, icon, color, _) in enumerate(TECHNIQUES, 1):
        table.add_row(f"[{color}]{i}[/]", f"{icon} [{color}]{name}[/]", combo_info[i-1])
    
    console.print(table)


def gather_technique_selection(console: Console) -> list[tuple]:
    """Get user's technique selections."""
    console.print()
    choices = Prompt.ask("[bold]Techniques to combine[/] [dim](e.g., 3 1 4)[/]", default="3 1")
    
    try:
        indices = [int(x) - 1 for x in choices.split()]
        selected = [(TECHNIQUES[i][0], TECHNIQUES[i][1], TECHNIQUES[i][3]) 
                   for i in indices if 0 <= i < len(TECHNIQUES)]
        return selected
    except (ValueError, IndexError):
        return []


def gather_task_context(console: Console, selected: list[tuple]) -> tuple[str, str]:
    """Get task and context from user."""
    selected_names = " + ".join([f"[{c}]{n}[/]" for _, n, c in selected])
    console.print(f"\n[bold]Combining:[/] {selected_names}\n")
    
    task = Prompt.ask("[bold cyan]📝 What is your task/question?[/]")
    context = Prompt.ask("[bold blue]📖 Context[/] [dim](optional)[/]", default="")
    
    return task, context


def build_combined_prompt(builder, selected: list[tuple], task: str, context: str) -> str:
    """Build the combined prompt from multiple techniques."""
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
        section = builder.build(ptype, config)
        combined_parts.append(f"\n## {name.upper()} APPROACH ##\n")
        combined_parts.append(section)
        combined_parts.append("\n" + "-" * 50)
    
    combined_parts.append("\nSynthesize insights from all approaches above to provide a comprehensive answer.")
    
    return "\n".join(combined_parts)


def display_result(console: Console, prompt: str, token_counter) -> None:
    """Display the combined prompt."""
    console.print()
    console.print(Panel(
        prompt,
        title="[bold bright_white]📝 Combined Prompt[/]",
        border_style="bright_cyan",
        box=box.DOUBLE,
        padding=(1, 2)
    ))
    
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
        elif action == "f":
            is_fav = history.toggle_favorite(prompt_id)
            status = "[yellow]⭐ Added to favorites[/]" if is_fav else "[dim]Removed from favorites[/]"
            console.print(status)
        else:
            break
