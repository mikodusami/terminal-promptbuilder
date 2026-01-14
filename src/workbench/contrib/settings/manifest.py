"""Manifest for the Settings feature."""

from src.workbench.contract import (
    FeatureManifest,
    FeatureCategory,
    FeatureContext,
    FeatureResult,
)

MANIFEST = FeatureManifest(
    name="settings",
    display_name="Settings",
    description="API keys & configuration",
    icon="⚙️",
    color="white",
    category=FeatureCategory.SYSTEM,
    requires_api_key=False,
    menu_order=90,
)


def run(ctx: FeatureContext) -> FeatureResult:
    """Settings and configuration menu."""
    from .ui import interactive_select, show_status, set_api_key, set_default_model
    
    while True:
        show_status(ctx.console, ctx.config)
        
        menu_options = [
            "🔑 Set OpenAI API Key",
            "🔑 Set Anthropic API Key",
            "🔑 Set Google API Key",
            "🎯 Set Default Model",
            "🔙 Back",
        ]
        
        idx = interactive_select(menu_options, title="")
        
        if idx is None or idx == 4:
            break
        elif idx == 0:
            set_api_key(ctx.console, "openai", ctx.config, ctx.app_state)
        elif idx == 1:
            set_api_key(ctx.console, "anthropic", ctx.config, ctx.app_state)
        elif idx == 2:
            set_api_key(ctx.console, "google", ctx.config, ctx.app_state)
        elif idx == 3:
            set_default_model(ctx.console, ctx.config, ctx.app_state)
    
    return FeatureResult(success=True)
