"""Manifest for the New Prompt feature."""

from src.workbench.contract import (
    FeatureManifest,
    FeatureCategory,
    FeatureContext,
    FeatureResult,
)

MANIFEST = FeatureManifest(
    name="new_prompt",
    display_name="New Prompt",
    description="Create a new prompt using any technique",
    icon="✨",
    color="cyan",
    category=FeatureCategory.CORE,
    requires_api_key=False,
    menu_order=10,
)


def run(ctx: FeatureContext) -> FeatureResult:
    """Create a new prompt using selected technique."""
    from .ui import (
        select_technique, gather_config, display_result,
        ask_tags, prompt_actions
    )
    
    # Select technique
    prompt_type, color = select_technique(ctx.console)
    if prompt_type is None:
        return FeatureResult(success=True, message="Cancelled")
    
    # Gather configuration
    config = gather_config(
        ctx.console, prompt_type, color,
        ctx.prompt_builder, ctx.token_counter,
        ctx.preview_mode
    )
    
    # Build the prompt
    result = ctx.prompt_builder.build(prompt_type, config)
    
    # Display result
    display_result(ctx.console, result, color, ctx.token_counter, ctx.config)
    
    # Save to history
    tags = ask_tags(ctx.console)
    prompt_id = ctx.history.save(
        technique=prompt_type.value,
        task=config.task,
        prompt=result,
        tags=tags
    )
    ctx.console.print(f"[dim]💾 Auto-saved to history (ID: {prompt_id})[/]")
    
    # Offer actions
    prompt_actions(ctx.console, prompt_id, result, ctx.history)
    
    return FeatureResult(success=True, data={"prompt_id": prompt_id, "prompt": result})
