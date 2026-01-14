"""Manifest for the Combine feature."""

from src.workbench.contract import (
    FeatureManifest,
    FeatureCategory,
    FeatureContext,
    FeatureResult,
)

MANIFEST = FeatureManifest(
    name="combine",
    display_name="Combine Techniques",
    description="Chain multiple techniques into one powerful prompt",
    icon="🔗",
    color="bright_cyan",
    category=FeatureCategory.CORE,
    requires_api_key=False,
    menu_order=11,
)


def run(ctx: FeatureContext) -> FeatureResult:
    """Combine multiple techniques into a mega-prompt."""
    from rich.panel import Panel
    from rich import box
    from .ui import (
        show_technique_table, gather_technique_selection,
        gather_task_context, build_combined_prompt,
        display_result, ask_tags, prompt_actions
    )
    
    ctx.console.print(Panel(
        "[bold]🔗 Prompt Combiner[/]\n[dim]Chain multiple techniques into one powerful prompt[/]",
        border_style="bright_cyan",
        box=box.ROUNDED
    ))
    ctx.console.print("[dim]Select techniques to combine (enter numbers separated by spaces)[/]\n")
    
    # Show technique options
    show_technique_table(ctx.console)
    
    # Get selections
    selected = gather_technique_selection(ctx.console)
    
    if len(selected) < 2:
        ctx.console.print("[yellow]Select at least 2 techniques to combine[/]")
        return FeatureResult(success=False, error="Not enough techniques selected")
    
    # Get task and context
    task, context = gather_task_context(ctx.console, selected)
    
    # Build combined prompt
    result = build_combined_prompt(ctx.prompt_builder, selected, task, context)
    
    # Display result
    display_result(ctx.console, result, ctx.token_counter)
    
    # Save to history
    tags = ask_tags(ctx.console)
    technique_names = "+".join([p.value for p, _, _ in selected])
    prompt_id = ctx.history.save(
        technique=f"combined:{technique_names}",
        task=task,
        prompt=result,
        tags=tags
    )
    ctx.console.print(f"[dim]💾 Auto-saved to history (ID: {prompt_id})[/]")
    
    # Offer actions
    prompt_actions(ctx.console, prompt_id, result, ctx.history)
    
    return FeatureResult(success=True, data={"prompt_id": prompt_id})
