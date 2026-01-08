#!/usr/bin/env python3
"""
Prompt Builder - Create exceptional prompts using modern prompt engineering techniques.

Techniques included:
- Chain of Thought (CoT)
- Few-Shot Learning
- Role-Based Prompting
- Structured Output
- Self-Consistency
- Tree of Thoughts
- ReAct (Reasoning + Acting)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich.text import Text
    from rich.markdown import Markdown
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


class PromptType(Enum):
    CHAIN_OF_THOUGHT = "cot"
    FEW_SHOT = "few_shot"
    ROLE_BASED = "role"
    STRUCTURED = "structured"
    REACT = "react"
    TREE_OF_THOUGHTS = "tot"
    SELF_CONSISTENCY = "self_consistency"


@dataclass
class PromptConfig:
    task: str
    context: str = ""
    examples: list[dict] = field(default_factory=list)
    role: str = ""
    output_format: str = ""
    constraints: list[str] = field(default_factory=list)
    temperature_hint: str = "balanced"


class PromptBuilder:
    """Build prompts using various prompt engineering techniques."""

    def __init__(self):
        self.templates = {
            PromptType.CHAIN_OF_THOUGHT: self._build_cot,
            PromptType.FEW_SHOT: self._build_few_shot,
            PromptType.ROLE_BASED: self._build_role_based,
            PromptType.STRUCTURED: self._build_structured,
            PromptType.REACT: self._build_react,
            PromptType.TREE_OF_THOUGHTS: self._build_tot,
            PromptType.SELF_CONSISTENCY: self._build_self_consistency,
        }

    def build(self, prompt_type: PromptType, config: PromptConfig) -> str:
        """Build a prompt using the specified technique."""
        builder = self.templates.get(prompt_type)
        if not builder:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
        return builder(config)

    def _build_cot(self, config: PromptConfig) -> str:
        """Chain of Thought - encourages step-by-step reasoning."""
        prompt = []
        if config.context:
            prompt.append(f"Context: {config.context}\n")
        prompt.append(f"Task: {config.task}\n")
        prompt.append("Think through this step-by-step:")
        prompt.append("1. First, identify the key elements of the problem")
        prompt.append("2. Break down the problem into smaller parts")
        prompt.append("3. Solve each part systematically")
        prompt.append("4. Combine the solutions and verify the result")
        prompt.append("\nLet's work through this carefully:")
        if config.constraints:
            prompt.append("\nConstraints to consider:")
            for c in config.constraints:
                prompt.append(f"- {c}")
        return "\n".join(prompt)

    def _build_few_shot(self, config: PromptConfig) -> str:
        """Few-Shot Learning - provides examples to guide the model."""
        prompt = []
        if config.context:
            prompt.append(f"Context: {config.context}\n")
        prompt.append(f"Task: {config.task}\n")
        if config.examples:
            prompt.append("Here are some examples:\n")
            for i, ex in enumerate(config.examples, 1):
                prompt.append(f"Example {i}:")
                prompt.append(f"Input: {ex.get('input', '')}")
                prompt.append(f"Output: {ex.get('output', '')}\n")
        prompt.append("Now, apply the same pattern to solve the following:")
        return "\n".join(prompt)

    def _build_role_based(self, config: PromptConfig) -> str:
        """Role-Based - assigns a specific persona to the model."""
        prompt = []
        role = config.role or "expert assistant"
        prompt.append(f"You are a {role}.\n")
        if config.context:
            prompt.append(f"Background: {config.context}\n")
        prompt.append(f"Your task: {config.task}\n")
        prompt.append("Approach this with your expertise, providing:")
        prompt.append("- Professional insights")
        prompt.append("- Practical recommendations")
        prompt.append("- Clear explanations")
        if config.constraints:
            prompt.append("\nKeep in mind:")
            for c in config.constraints:
                prompt.append(f"- {c}")
        return "\n".join(prompt)

    def _build_structured(self, config: PromptConfig) -> str:
        """Structured Output - requests specific format."""
        prompt = []
        if config.context:
            prompt.append(f"Context: {config.context}\n")
        prompt.append(f"Task: {config.task}\n")
        output_format = config.output_format or "JSON"
        prompt.append(f"Provide your response in {output_format} format.\n")
        prompt.append("Structure your response with:")
        prompt.append("- Clear sections/fields")
        prompt.append("- Consistent formatting")
        prompt.append("- Complete information")
        if config.constraints:
            prompt.append("\nRequirements:")
            for c in config.constraints:
                prompt.append(f"- {c}")
        return "\n".join(prompt)

    def _build_react(self, config: PromptConfig) -> str:
        """ReAct - combines reasoning and acting."""
        prompt = []
        if config.context:
            prompt.append(f"Context: {config.context}\n")
        prompt.append(f"Task: {config.task}\n")
        prompt.append("Use the ReAct framework to solve this:\n")
        prompt.append("For each step, follow this pattern:")
        prompt.append("Thought: [Your reasoning about what to do next]")
        prompt.append("Action: [The action you decide to take]")
        prompt.append("Observation: [What you observe from the action]")
        prompt.append("... (repeat until solved)")
        prompt.append("Final Answer: [Your conclusion]\n")
        prompt.append("Begin your analysis:")
        return "\n".join(prompt)

    def _build_tot(self, config: PromptConfig) -> str:
        """Tree of Thoughts - explores multiple reasoning paths."""
        prompt = []
        if config.context:
            prompt.append(f"Context: {config.context}\n")
        prompt.append(f"Task: {config.task}\n")
        prompt.append("Explore this problem using Tree of Thoughts:\n")
        prompt.append("1. Generate 3 different initial approaches")
        prompt.append("2. For each approach, evaluate:")
        prompt.append("   - Feasibility (1-10)")
        prompt.append("   - Potential issues")
        prompt.append("   - Expected outcome")
        prompt.append("3. Select the most promising path")
        prompt.append("4. Develop it further, backtracking if needed")
        prompt.append("5. Present your final solution with reasoning\n")
        prompt.append("Start by listing your three approaches:")
        return "\n".join(prompt)

    def _build_self_consistency(self, config: PromptConfig) -> str:
        """Self-Consistency - generates multiple solutions and finds consensus."""
        prompt = []
        if config.context:
            prompt.append(f"Context: {config.context}\n")
        prompt.append(f"Task: {config.task}\n")
        prompt.append("Apply self-consistency checking:\n")
        prompt.append("1. Solve this problem 3 different ways")
        prompt.append("2. For each solution, show your work")
        prompt.append("3. Compare all solutions")
        prompt.append("4. Identify the most consistent/reliable answer")
        prompt.append("5. Explain why this answer is most trustworthy\n")
        prompt.append("Solution 1:")
        return "\n".join(prompt)


class InteractivePromptBuilder:
    """Interactive CLI for building prompts with rich formatting."""

    TECHNIQUES = [
        (PromptType.CHAIN_OF_THOUGHT, "Chain of Thought", "🧠", "cyan", 
         "Step-by-step reasoning for complex problems"),
        (PromptType.FEW_SHOT, "Few-Shot Learning", "📚", "green",
         "Learn patterns from examples you provide"),
        (PromptType.ROLE_BASED, "Role-Based", "🎭", "magenta",
         "Assign expert persona for domain-specific tasks"),
        (PromptType.STRUCTURED, "Structured Output", "📋", "yellow",
         "Get responses in specific formats (JSON, etc.)"),
        (PromptType.REACT, "ReAct", "⚡", "red",
         "Reasoning + Acting for multi-step problem solving"),
        (PromptType.TREE_OF_THOUGHTS, "Tree of Thoughts", "🌳", "blue",
         "Explore multiple solution paths systematically"),
        (PromptType.SELF_CONSISTENCY, "Self-Consistency", "🔄", "white",
         "Multiple solutions for verification & consensus"),
    ]

    def __init__(self):
        self.builder = PromptBuilder()
        if not RICH_AVAILABLE:
            console_print("[yellow]Install 'rich' for the best experience: pip install rich[/]")

    def run(self):
        """Run the interactive prompt builder."""
        self._show_header()

        while True:
            prompt_type, color = self._select_prompt_type()
            if prompt_type is None:
                self._show_goodbye()
                break

            config = self._gather_config(prompt_type, color)
            result = self.builder.build(prompt_type, config)

            self._display_result(result, color)
            self._offer_save_option(result)

            if not self._continue_prompt():
                self._show_goodbye()
                break

    def _show_header(self):
        """Display the application header."""
        if RICH_AVAILABLE:
            header = Text()
            header.append("⚡ PROMPT BUILDER ⚡\n", style="bold bright_white")
            header.append("Modern Prompt Engineering Techniques", style="dim")
            console.print(Panel(header, border_style="bright_blue", box=box.DOUBLE))
            console.print()
        else:
            print("\n" + "=" * 50)
            print("⚡ PROMPT BUILDER - Prompt Engineering Techniques")
            print("=" * 50 + "\n")

    def _show_goodbye(self):
        """Display goodbye message."""
        if RICH_AVAILABLE:
            console.print(Panel(
                "[bold green]Happy prompting! 🎯[/]\n[dim]May your tokens be ever efficient.[/]",
                border_style="green",
                box=box.ROUNDED
            ))
        else:
            print("\nGoodbye! Happy prompting! 🎯")

    def _select_prompt_type(self) -> tuple[Optional[PromptType], str]:
        """Let user select a prompt engineering technique."""
        if RICH_AVAILABLE:
            console.print("[bold bright_white]Select a technique:[/]\n")
            
            table = Table(box=box.ROUNDED, border_style="dim", show_header=False, padding=(0, 2))
            table.add_column("Key", style="bold bright_white", width=5)
            table.add_column("Technique", width=22)
            table.add_column("Description", style="dim")

            for i, (_, name, icon, color, desc) in enumerate(self.TECHNIQUES, 1):
                table.add_row(
                    f"[{color}]{i}[/]",
                    f"{icon} [{color}]{name}[/]",
                    desc
                )
            table.add_row("[red]q[/]", "🚪 [red]Quit[/]", "Exit the builder")
            
            console.print(table)
            console.print()
            
            choice = Prompt.ask("[bold]Your choice[/]", default="1")
        else:
            print("Select a technique:\n")
            for i, (_, name, icon, _, desc) in enumerate(self.TECHNIQUES, 1):
                print(f"  [{i}] {icon} {name:<20} - {desc}")
            print("  [q] 🚪 Quit")
            choice = input("\nYour choice: ").strip()

        if choice.lower() == 'q':
            return None, ""

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.TECHNIQUES):
                ptype, name, icon, color, _ = self.TECHNIQUES[idx]
                if RICH_AVAILABLE:
                    console.print(f"\n[{color}]✓ Selected: {icon} {name}[/]\n")
                return ptype, color
        except ValueError:
            pass

        if RICH_AVAILABLE:
            console.print("[red]Invalid choice, try again.[/]\n")
        else:
            print("Invalid choice, try again.\n")
        return self._select_prompt_type()

    def _gather_config(self, prompt_type: PromptType, color: str) -> PromptConfig:
        """Gather configuration based on prompt type."""
        if RICH_AVAILABLE:
            console.print(Panel(
                f"[bold]Configure your prompt[/]",
                border_style=color,
                box=box.ROUNDED
            ))
            task = Prompt.ask("\n[bold cyan]📝 What is your task/question?[/]")
            context = Prompt.ask("[bold blue]📖 Context[/] [dim](optional, Enter to skip)[/]", default="")
        else:
            print(f"\n--- Configure {prompt_type.name} ---\n")
            task = input("📝 What is your task/question?\n> ").strip()
            context = input("\n📖 Context (optional, Enter to skip):\n> ").strip()

        config = PromptConfig(task=task, context=context)

        # Type-specific configuration
        if prompt_type == PromptType.FEW_SHOT:
            config.examples = self._gather_examples()
        elif prompt_type == PromptType.ROLE_BASED:
            config.role = self._ask("[bold magenta]🎭 Role/Persona[/]", 
                                    "e.g., 'senior Python developer'")
        elif prompt_type == PromptType.STRUCTURED:
            config.output_format = self._ask("[bold yellow]📋 Output format[/]",
                                             "e.g., JSON, Markdown, Table")

        # Optional constraints
        if self._confirm("[bold]Add constraints?[/]"):
            config.constraints = self._gather_constraints()

        return config

    def _ask(self, label: str, hint: str = "") -> str:
        """Ask for input with rich formatting."""
        if RICH_AVAILABLE:
            hint_text = f" [dim]({hint})[/]" if hint else ""
            return Prompt.ask(f"{label}{hint_text}", default="")
        else:
            hint_text = f" ({hint})" if hint else ""
            return input(f"{label}{hint_text}: ").strip()

    def _confirm(self, message: str) -> bool:
        """Ask for confirmation."""
        if RICH_AVAILABLE:
            return Confirm.ask(message, default=False)
        else:
            return input(f"{message} (y/n): ").strip().lower() == 'y'

    def _gather_examples(self) -> list[dict]:
        """Gather few-shot examples from user."""
        examples = []
        if RICH_AVAILABLE:
            console.print("\n[bold green]📚 Provide examples[/] [dim](type 'done' when finished)[/]\n")
        else:
            print("\nProvide examples (type 'done' when finished):\n")

        while True:
            num = len(examples) + 1
            if RICH_AVAILABLE:
                console.print(f"[bold]Example {num}[/]")
                inp = Prompt.ask("  [cyan]Input[/] [dim](or 'done')[/]")
            else:
                inp = input(f"Example {num} - Input (or 'done'): ").strip()

            if inp.lower() == 'done':
                break

            if RICH_AVAILABLE:
                out = Prompt.ask("  [green]Output[/]")
            else:
                out = input(f"Example {num} - Output: ").strip()

            examples.append({"input": inp, "output": out})
            if RICH_AVAILABLE:
                console.print(f"  [dim]✓ Added[/]\n")

        return examples

    def _gather_constraints(self) -> list[str]:
        """Gather constraints from user."""
        constraints = []
        if RICH_AVAILABLE:
            console.print("\n[bold yellow]⚠️  Enter constraints[/] [dim](type 'done' when finished)[/]\n")
        else:
            print("\nEnter constraints (type 'done' when finished):\n")

        while True:
            num = len(constraints) + 1
            if RICH_AVAILABLE:
                c = Prompt.ask(f"  [yellow]Constraint {num}[/] [dim](or 'done')[/]")
            else:
                c = input(f"Constraint {num} (or 'done'): ").strip()

            if c.lower() == 'done':
                break
            constraints.append(c)

        return constraints

    def _display_result(self, prompt: str, color: str):
        """Display the generated prompt."""
        if RICH_AVAILABLE:
            console.print()
            console.print(Panel(
                prompt,
                title="[bold bright_white]📝 Generated Prompt[/]",
                border_style=color,
                box=box.DOUBLE,
                padding=(1, 2)
            ))
        else:
            print("\n" + "=" * 50)
            print("📝 GENERATED PROMPT:")
            print("=" * 50)
            print(prompt)
            print("=" * 50)

    def _offer_save_option(self, prompt: str):
        """Offer to save the prompt to a file."""
        if self._confirm("\n[bold]💾 Save to file?[/]"):
            if RICH_AVAILABLE:
                filename = Prompt.ask("[dim]Filename[/]", default="prompt.txt")
            else:
                filename = input("Filename (default: prompt.txt): ").strip() or "prompt.txt"

            with open(filename, 'w') as f:
                f.write(prompt)

            if RICH_AVAILABLE:
                console.print(f"[bold green]✅ Saved to {filename}[/]")
            else:
                print(f"✅ Saved to {filename}")

    def _continue_prompt(self) -> bool:
        """Ask if user wants to create another prompt."""
        if RICH_AVAILABLE:
            console.print()
        return self._confirm("[bold]Create another prompt?[/]")


def quick_build(
    technique: str,
    task: str,
    context: str = "",
    role: str = "",
    examples: list[dict] = None,
    output_format: str = "",
    constraints: list[str] = None
) -> str:
    """
    Quick function to build prompts programmatically.

    Args:
        technique: One of 'cot', 'few_shot', 'role', 'structured', 'react', 'tot', 'self_consistency'
        task: The main task or question
        context: Optional background context
        role: Role/persona (for role-based prompts)
        examples: List of {"input": ..., "output": ...} dicts (for few-shot)
        output_format: Desired format (for structured prompts)
        constraints: List of constraints to include

    Returns:
        Generated prompt string
    """
    builder = PromptBuilder()
    prompt_type = PromptType(technique)
    config = PromptConfig(
        task=task,
        context=context,
        role=role,
        examples=examples or [],
        output_format=output_format,
        constraints=constraints or []
    )
    return builder.build(prompt_type, config)


if __name__ == "__main__":
    if not RICH_AVAILABLE:
        print("💡 Tip: Install 'rich' for a better experience: pip install rich\n")
    app = InteractivePromptBuilder()
    app.run()
