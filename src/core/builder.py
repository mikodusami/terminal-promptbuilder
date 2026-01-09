"""
Core prompt builder - constructs prompts using various techniques.
"""

from .types import PromptType
from .config import PromptConfig


class PromptBuilder:
    """Build prompts using various prompt engineering techniques."""

    def __init__(self):
        self._templates = {
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
        builder = self._templates.get(prompt_type)
        if not builder:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
        return builder(config)

    def _build_cot(self, config: PromptConfig) -> str:
        """Chain of Thought - encourages step-by-step reasoning."""
        lines = []
        if config.context:
            lines.append(f"Context: {config.context}\n")
        lines.append(f"Task: {config.task}\n")
        lines.append("Think through this step-by-step:")
        lines.append("1. First, identify the key elements of the problem")
        lines.append("2. Break down the problem into smaller parts")
        lines.append("3. Solve each part systematically")
        lines.append("4. Combine the solutions and verify the result")
        lines.append("\nLet's work through this carefully:")
        if config.constraints:
            lines.append("\nConstraints to consider:")
            for c in config.constraints:
                lines.append(f"- {c}")
        return "\n".join(lines)

    def _build_few_shot(self, config: PromptConfig) -> str:
        """Few-Shot Learning - provides examples to guide the model."""
        lines = []
        if config.context:
            lines.append(f"Context: {config.context}\n")
        lines.append(f"Task: {config.task}\n")
        if config.examples:
            lines.append("Here are some examples:\n")
            for i, ex in enumerate(config.examples, 1):
                lines.append(f"Example {i}:")
                lines.append(f"Input: {ex.get('input', '')}")
                lines.append(f"Output: {ex.get('output', '')}\n")
        lines.append("Now, apply the same pattern to solve the following:")
        return "\n".join(lines)

    def _build_role_based(self, config: PromptConfig) -> str:
        """Role-Based - assigns a specific persona to the model."""
        lines = []
        role = config.role or "expert assistant"
        lines.append(f"You are a {role}.\n")
        if config.context:
            lines.append(f"Background: {config.context}\n")
        lines.append(f"Your task: {config.task}\n")
        lines.append("Approach this with your expertise, providing:")
        lines.append("- Professional insights")
        lines.append("- Practical recommendations")
        lines.append("- Clear explanations")
        if config.constraints:
            lines.append("\nKeep in mind:")
            for c in config.constraints:
                lines.append(f"- {c}")
        return "\n".join(lines)

    def _build_structured(self, config: PromptConfig) -> str:
        """Structured Output - requests specific format."""
        lines = []
        if config.context:
            lines.append(f"Context: {config.context}\n")
        lines.append(f"Task: {config.task}\n")
        output_format = config.output_format or "JSON"
        lines.append(f"Provide your response in {output_format} format.\n")
        lines.append("Structure your response with:")
        lines.append("- Clear sections/fields")
        lines.append("- Consistent formatting")
        lines.append("- Complete information")
        if config.constraints:
            lines.append("\nRequirements:")
            for c in config.constraints:
                lines.append(f"- {c}")
        return "\n".join(lines)

    def _build_react(self, config: PromptConfig) -> str:
        """ReAct - combines reasoning and acting."""
        lines = []
        if config.context:
            lines.append(f"Context: {config.context}\n")
        lines.append(f"Task: {config.task}\n")
        lines.append("Use the ReAct framework to solve this:\n")
        lines.append("For each step, follow this pattern:")
        lines.append("Thought: [Your reasoning about what to do next]")
        lines.append("Action: [The action you decide to take]")
        lines.append("Observation: [What you observe from the action]")
        lines.append("... (repeat until solved)")
        lines.append("Final Answer: [Your conclusion]\n")
        lines.append("Begin your analysis:")
        return "\n".join(lines)

    def _build_tot(self, config: PromptConfig) -> str:
        """Tree of Thoughts - explores multiple reasoning paths."""
        lines = []
        if config.context:
            lines.append(f"Context: {config.context}\n")
        lines.append(f"Task: {config.task}\n")
        lines.append("Explore this problem using Tree of Thoughts:\n")
        lines.append("1. Generate 3 different initial approaches")
        lines.append("2. For each approach, evaluate:")
        lines.append("   - Feasibility (1-10)")
        lines.append("   - Potential issues")
        lines.append("   - Expected outcome")
        lines.append("3. Select the most promising path")
        lines.append("4. Develop it further, backtracking if needed")
        lines.append("5. Present your final solution with reasoning\n")
        lines.append("Start by listing your three approaches:")
        return "\n".join(lines)

    def _build_self_consistency(self, config: PromptConfig) -> str:
        """Self-Consistency - generates multiple solutions and finds consensus."""
        lines = []
        if config.context:
            lines.append(f"Context: {config.context}\n")
        lines.append(f"Task: {config.task}\n")
        lines.append("Apply self-consistency checking:\n")
        lines.append("1. Solve this problem 3 different ways")
        lines.append("2. For each solution, show your work")
        lines.append("3. Compare all solutions")
        lines.append("4. Identify the most consistent/reliable answer")
        lines.append("5. Explain why this answer is most trustworthy\n")
        lines.append("Solution 1:")
        return "\n".join(lines)
