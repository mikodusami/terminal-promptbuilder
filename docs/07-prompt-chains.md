# Prompt Chains

Prompt chains allow you to create multi-step workflows where the output of one prompt feeds into the next.

## Accessing Chains

From AI Features menu (`a`), press `c` for Prompt Chains.

```
⛓️ Prompt Chains

  [1] ▶️  research_and_summarize - Research a topic and create a summary
  [2] ▶️  code_review_chain      - Multi-step code review
  [n] ➕ Create new chain
  [b] 🔙 Back
```

## Built-in Chains

### Research and Summarize

A 3-step chain for researching topics:

1. **Research** - List 5 key points about the topic
2. **Expand** - Expand on those points with details
3. **Summarize** - Create a concise summary

```
Provide input values:
topic: Machine learning in healthcare

Executing chain...

✓ Success - 3/3 steps
Tokens: 1,245 | Latency: 4,523ms

╭─ Final Output ────────────────────────────────────────────────╮
│ Machine learning is transforming healthcare through...        │
╰───────────────────────────────────────────────────────────────╯
```

### Code Review Chain

A 3-step chain for thorough code review:

1. **Analyze** - Analyze code for potential issues
2. **Suggest** - Suggest specific improvements
3. **Refactor** - Refactor applying the suggestions

## Executing a Chain

1. Select a chain by number
2. Provide required input values
3. Watch the chain execute step by step
4. View the final output

### Input Variables

Chains detect variables from the first step's template. Variables use `{variable_name}` syntax.

```
Provide input values:
code: def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## Creating Custom Chains

Press `n` to create a new chain.

### Step 1: Name and Description

```
Chain name: content_pipeline
Description: Generate and refine blog content
```

### Step 2: Add Steps

```
Add steps (type 'done' when finished)

Step 1 name (or 'done'): outline
Prompt template: Create an outline for a blog post about {topic}
Output variable name: outline

Step 2 name (or 'done'): draft
Prompt template: Write a draft based on this outline: {outline}
Output variable name: draft

Step 3 name (or 'done'): polish
Prompt template: Polish and improve this draft: {draft}
Output variable name: final

Step 4 name (or 'done'): done

✓ Chain 'content_pipeline' created with 3 steps
```

### Variable Flow

Variables flow through the chain:

- `{topic}` - User input
- `{outline}` - Output from step 1
- `{draft}` - Output from step 2
- `{final}` - Output from step 3

## Chain Configuration

### ChainStep Properties

| Property          | Description               | Default          |
| ----------------- | ------------------------- | ---------------- |
| `name`            | Step identifier           | Required         |
| `prompt_template` | The prompt with variables | Required         |
| `output_key`      | Variable name for output  | `step_N_output`  |
| `provider`        | LLM provider to use       | Auto-select      |
| `model`           | Specific model            | Provider default |
| `max_tokens`      | Maximum response tokens   | 4096             |
| `temperature`     | Response randomness       | 0.7              |
| `transform`       | Output transformation     | None             |

### Output Transforms

| Transform    | Description              |
| ------------ | ------------------------ |
| `json`       | Parse output as JSON     |
| `lines`      | Split into list of lines |
| `first_line` | Extract first line only  |

## Chain Storage

Custom chains are saved to:

```
~/.promptbuilder/chains.json
```

### Example chains.json

```json
{
  "content_pipeline": {
    "description": "Generate and refine blog content",
    "steps": [
      {
        "name": "outline",
        "prompt_template": "Create an outline for a blog post about {topic}",
        "output_key": "outline"
      },
      {
        "name": "draft",
        "prompt_template": "Write a draft based on this outline: {outline}",
        "output_key": "draft"
      },
      {
        "name": "polish",
        "prompt_template": "Polish and improve this draft: {draft}",
        "output_key": "final"
      }
    ]
  }
}
```

## Advanced Chain Patterns

### Branching Logic

Use conditions to control flow:

```python
ChainStep(
    name="check",
    prompt_template="Is this code secure? Answer YES or NO: {code}",
    output_key="is_secure",
    condition="'YES' in output"
)
```

### Multi-Model Chains

Use different models for different steps:

```python
ChainStep(
    name="creative",
    prompt_template="Generate creative ideas for {topic}",
    provider="anthropic",
    model="claude-3-opus-20240229",
    temperature=0.9
)
```

### JSON Extraction

Parse structured data between steps:

```python
ChainStep(
    name="extract",
    prompt_template="Extract entities as JSON: {text}",
    transform="json",
    output_key="entities"
)
```

## Best Practices

1. **Keep steps focused** - Each step should do one thing well
2. **Use descriptive output keys** - Makes debugging easier
3. **Test incrementally** - Verify each step before adding more
4. **Handle errors gracefully** - Check for failures in chain results
5. **Monitor token usage** - Chains can consume many tokens
