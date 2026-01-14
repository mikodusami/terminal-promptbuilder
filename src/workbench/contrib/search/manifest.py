"""Manifest for the Search feature."""

from src.workbench.contract import (
    FeatureManifest,
    FeatureCategory,
    FeatureContext,
    FeatureResult,
)

MANIFEST = FeatureManifest(
    name="search",
    display_name="Search",
    description="Search saved prompts",
    icon="🔍",
    color="magenta",
    category=FeatureCategory.STORAGE,
    requires_api_key=False,
    menu_order=32,
)


def run(ctx: FeatureContext) -> FeatureResult:
    """Search saved prompts."""
    from rich.prompt import Prompt
    from src.workbench.contrib.favorites.ui import display_prompt_list, select_from_list, view_prompt
    
    query = Prompt.ask("[bold magenta]🔍 Search[/]")
    
    prompts = ctx.history.search(query)
    
    if not prompts:
        ctx.console.print(f"[dim]No prompts found for '{query}'[/]\n")
        return FeatureResult(success=True, message="No results")
    
    display_prompt_list(ctx.console, prompts, f"🔍 Results for '{query}'")
    
    selected = select_from_list(ctx.console, prompts)
    if selected:
        view_prompt(ctx.console, selected, ctx.history)
    
    return FeatureResult(success=True, data={"count": len(prompts)})
