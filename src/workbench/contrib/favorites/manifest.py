"""Manifest for the Favorites feature."""

from src.workbench.contract import (
    FeatureManifest,
    FeatureCategory,
    FeatureContext,
    FeatureResult,
)

MANIFEST = FeatureManifest(
    name="favorites",
    display_name="Favorites",
    description="View favorite prompts",
    icon="⭐",
    color="yellow",
    category=FeatureCategory.STORAGE,
    requires_api_key=False,
    menu_order=31,
)


def run(ctx: FeatureContext) -> FeatureResult:
    """Browse favorite prompts."""
    from .ui import display_prompt_list, select_from_list, view_prompt
    
    prompts = ctx.history.list_favorites()
    
    if not prompts:
        ctx.console.print("[dim]No favorites yet. Create prompts and mark them as favorites![/]\n")
        return FeatureResult(success=True, message="No favorites")
    
    display_prompt_list(ctx.console, prompts, "⭐ Favorite Prompts")
    
    selected = select_from_list(ctx.console, prompts)
    if selected:
        view_prompt(ctx.console, selected, ctx.history)
    
    return FeatureResult(success=True)
