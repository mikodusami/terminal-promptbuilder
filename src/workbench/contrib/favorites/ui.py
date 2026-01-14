"""UI components for the favorites feature."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box

from src.platform.clipboard import copy_to_clipboard


def display_prompt_list(console: Console, prompts: list, title: str) -> None:
    """Display a list of prompts."""
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


def select_from_list(console: Console, prompts: list):
    """Let user select a prompt from the list."""
    choice = Prompt.ask("\n[bold]Select #[/] [dim](or Enter to go back)[/]", default="")
    
    if not choice:
        return None
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(prompts):
            return prompts[idx]
    except ValueError:
        pass
    
    return None


def view_prompt(console: Console, saved, history) -> None:
    """View a saved prompt with actions."""
    console.print(Panel(
        saved.prompt,
        title=f"[bold]{saved.technique.upper()}[/] - {saved.task[:40]}",
        subtitle=f"[dim]ID: {saved.id} | Created: {saved.created_at.strftime('%Y-%m-%d %H:%M')}[/]",
        border_style="yellow",
        box=box.DOUBLE,
        padding=(1, 2)
    ))
    
    while True:
        console.print("\n[bold]Actions:[/] [cyan]c[/]=copy [yellow]f[/]=toggle favorite [red]d[/]=delete [dim]b[/]=back")
        action = Prompt.ask("[bold]Action[/]", default="b")
        
        if action == "c":
            if copy_to_clipboard(saved.prompt):
                console.print("[green]📋 Copied to clipboard![/]")
        elif action == "f":
            is_fav = history.toggle_favorite(saved.id)
            console.print("[yellow]⭐ Favorite toggled[/]" if is_fav else "[dim]Removed from favorites[/]")
        elif action == "d":
            if Confirm.ask("[red]Delete this prompt?[/]", default=False):
                history.delete(saved.id)
                console.print("[red]🗑️  Deleted[/]")
                break
        elif action == "b":
            break
