"""Manifest for the Quit feature."""

from src.workbench.contract import (
    FeatureManifest,
    FeatureCategory,
    FeatureContext,
    FeatureResult,
)

MANIFEST = FeatureManifest(
    name="quit",
    display_name="Quit",
    description="Exit the builder",
    icon="🚪",
    color="red",
    category=FeatureCategory.SYSTEM,
    requires_api_key=False,
    menu_order=99,
)


def run(ctx: FeatureContext) -> FeatureResult:
    """Exit the application."""
    from rich.panel import Panel
    from rich import box
    
    ctx.console.print(Panel(
        "[bold green]Happy prompting! 🎯[/]\n[dim]May your tokens be ever efficient.[/]",
        border_style="green",
        box=box.ROUNDED
    ))
    
    # Signal to exit
    return FeatureResult(success=True, data={"action": "quit"})
