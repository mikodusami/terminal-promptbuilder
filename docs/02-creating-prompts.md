# Creating Prompts

## New Prompt Flow

### Step 1: Select a Technique

From the main menu, press `n` to create a new prompt. You'll see the technique selection:

```
Select a technique:

  [1] 🧠 Chain of Thought    - Step-by-step reasoning for complex problems
  [2] 📚 Few-Shot Learning   - Learn patterns from examples you provide
  [3] 🎭 Role-Based          - Assign expert persona for domain-specific tasks
  [4] 📋 Structured Output   - Get responses in specific formats (JSON, etc.)
  [5] ⚡ ReAct               - Reasoning + Acting for multi-step problem solving
  [6] 🌳 Tree of Thoughts    - Explore multiple solution paths systematically
  [7] 🔄 Self-Consistency    - Multiple solutions for verification & consensus
  [q] 🚪 Quit
```

### Step 2: Enter Your Task

After selecting a technique, enter your main task or question:

```
📝 What is your task/question?
> Explain how neural networks learn
```

### Step 3: Add Context (Optional)

Provide additional background information:

```
📖 Context (optional, Enter to skip):
> For a blog post targeting beginners with no ML background
```

### Step 4: Technique-Specific Configuration

Depending on your chosen technique, you may be asked for additional inputs:

**Few-Shot Learning:**

```
📚 Provide examples (type 'done' when finished)

Example 1
  Input (or 'done'): What is Python?
  Output: Python is a high-level programming language...
  ✓ Added

Example 2
  Input (or 'done'): done
```

**Role-Based:**

```
🎭 Role/Persona (e.g., 'senior Python developer'):
> machine learning researcher with 10 years experience
```

**Structured Output:**

```
📋 Output format (e.g., JSON, Markdown, Table):
> JSON with sections for introduction, key concepts, and examples
```

### Step 5: Add Constraints (Optional)

```
Add constraints? (y/n): y

⚠️ Enter constraints (type 'done' when finished)

  Constraint 1 (or 'done'): Keep explanations under 500 words
  Constraint 2 (or 'done'): Avoid technical jargon
  Constraint 3 (or 'done'): done
```

### Step 6: View Generated Prompt

Your prompt is displayed with token estimates:

```
╔══════════════════════════════════════════════════════════════╗
║ 📝 Generated Prompt                                          ║
╠══════════════════════════════════════════════════════════════╣
║ You are a machine learning researcher with 10 years          ║
║ experience.                                                  ║
║                                                              ║
║ Background: For a blog post targeting beginners with no ML   ║
║ background                                                   ║
║                                                              ║
║ Your task: Explain how neural networks learn                 ║
║ ...                                                          ║
╚══════════════════════════════════════════════════════════════╝

💰 Token Estimates
┌──────────────────┬────────┬──────────┬──────────┐
│ Model            │ Tokens │ Input    │ Output/1K│
├──────────────────┼────────┼──────────┼──────────┤
│ gpt-4o           │    156 │ $0.0004  │ $0.0100  │
│ gpt-4o-mini      │    156 │ $0.0000  │ $0.0006  │
│ claude-3.5-sonnet│    156 │ $0.0005  │ $0.0150  │
└──────────────────┴────────┴──────────┴──────────┘
```

### Step 7: Post-Creation Actions

After generation, the prompt is automatically copied to clipboard. Additional actions:

```
📋 Copied to clipboard!

Actions: [c]=copy [f]=favorite [s]=save file [Enter]=continue
Action:
```

- `c` - Copy to clipboard again
- `f` - Add to favorites
- `s` - Save to file (with format selection)
- `Enter` - Return to main menu

### Step 8: Add Tags

Before returning to the menu, you can add tags:

```
🏷️ Tags (comma-separated, Enter to skip): ml, tutorial, beginner
```

## Preview Mode

Enable Preview Mode (`p` from main menu) to see your prompt build in real-time as you enter information. This is helpful for understanding how each input affects the final prompt.

```
👁️ Preview Mode: ON

--- Preview (156 tokens) ---
You are a machine learning researcher...
---
```

## Combining Techniques

Press `m` from the main menu to combine multiple techniques into a single mega-prompt.

1. Select techniques by entering numbers separated by spaces:

```
Techniques to combine (e.g., 3 1 4): 3 1 4
```

2. Enter your task and context
3. The builder creates a combined prompt with sections for each technique

This is powerful for complex tasks that benefit from multiple approaches.
