"""Common types for the new prompt feature."""

from src.core import PromptType

# Technique definitions with metadata
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
