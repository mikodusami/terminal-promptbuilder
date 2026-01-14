"""Manifest for the Preview Mode feature."""

from src.workbench.contract import (
    FeatureManifest,
    FeatureCategory,
    FeatureContext,
    FeatureResult,
)

MANIFEST = FeatureManifest(
    name="preview",
    display_name="Preview Mode",
    description="Toggle live prompt preview",
    icon="👁️",
    color="blue",
    category=FeatureCategory.UTILITY,
    requires_api_key=False,
    menu_order=40,
)


def run(ctx: FeatureContext) -> FeatureResult:
    """Toggle live preview mode."""
    if ctx.app_state:
        ctx.app_state.preview_mode = not ctx.app_state.preview_mode
        status = "ON" if ctx.app_state.preview_mode else "OFF"
        color = "green" if ctx.app_state.preview_mode else "red"
        ctx.console.print(f"[bold]👁️ Preview Mode: [{color}]{status}[/]")
        return FeatureResult(success=True, data={"preview_mode": ctx.app_state.preview_mode})
    
    ctx.console.print("[red]Preview mode toggle not available[/]")
    return FeatureResult(success=False, error="App state not available")
