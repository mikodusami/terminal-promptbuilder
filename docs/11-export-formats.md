# Export Formats

Save prompts in various formats for different use cases.

## Accessing Export

When viewing a prompt, press `s` to save to file:

```
Actions: [c]=copy [f]=favorite [s]=save file [Enter]=continue
Action: s

Export Formats:
  [1] JSON (API) (.json)
  [2] OpenAI Format (.json)
  [3] Anthropic Format (.json)
  [4] Markdown (.md)
  [5] LangChain (.json)
  [6] LlamaIndex (.json)
  [7] Prompt File (.prompt)
  [8] Plain Text (.txt)

Format: 1
Filename (prompt.json): my_prompt.json
✅ Exported to my_prompt.json
```

## Available Formats

### 1. JSON (API)

Generic JSON format with metadata.

```json
{
  "messages": [{ "role": "user", "content": "Your prompt here..." }],
  "metadata": {
    "technique": "role",
    "task": "Code review",
    "created_at": "2024-01-15T10:30:00",
    "tags": ["python", "review"]
  }
}
```

**Use case:** General purpose, custom integrations

---

### 2. OpenAI Format

Ready for OpenAI API calls.

```json
{
  "messages": [{ "role": "user", "content": "Your prompt here..." }]
}
```

**Use case:** Direct use with OpenAI API

```python
import openai
import json

with open("prompt.json") as f:
    data = json.load(f)

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=data["messages"]
)
```

---

### 3. Anthropic Format

Ready for Anthropic API calls.

```json
{
  "messages": [{ "role": "user", "content": "Your prompt here..." }]
}
```

**Use case:** Direct use with Anthropic API

```python
import anthropic
import json

with open("prompt.json") as f:
    data = json.load(f)

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=data["messages"]
)
```

---

### 4. Markdown

Human-readable documentation format.

```markdown
# Code review

**Technique:** role
**Created:** 2024-01-15T10:30:00
**Tags:** python, review

---

## Prompt
```

You are a senior software engineer conducting a code review.

Your task: Review this Python function for best practices...

```

```

**Use case:** Documentation, sharing, version control

---

### 5. LangChain

Compatible with LangChain PromptTemplate.

```json
{
  "_type": "prompt",
  "input_variables": [],
  "template": "Your prompt here with {{escaped}} braces..."
}
```

**Use case:** LangChain applications

```python
from langchain.prompts import load_prompt

prompt = load_prompt("prompt.json")
result = prompt.format()
```

---

### 6. LlamaIndex

Compatible with LlamaIndex prompts.

```json
{
  "prompt_type": "custom",
  "prompt_template": "Your prompt here..."
}
```

**Use case:** LlamaIndex applications

---

### 7. Prompt File

Simple structured text format.

```
---
technique: role
task: Code review
created: 2024-01-15T10:30:00
tags: python, review
---

You are a senior software engineer conducting a code review.

Your task: Review this Python function for best practices...
```

**Use case:** Simple storage, easy editing

---

### 8. Plain Text

Just the prompt content.

```
You are a senior software engineer conducting a code review.

Your task: Review this Python function for best practices...
```

**Use case:** Quick copy, simple use

## Programmatic Export

```python
from src.services.export import ExportService, ExportFormat, ExportMetadata

# Create metadata
metadata = ExportMetadata(
    technique="role",
    task="Code review",
    created_at="2024-01-15T10:30:00",
    tags=["python", "review"]
)

# Export in different formats
prompt = "Your prompt here..."

# JSON
content, ext = ExportService.export(prompt, ExportFormat.JSON, metadata)

# Markdown
content, ext = ExportService.export(prompt, ExportFormat.MARKDOWN, metadata)

# OpenAI
content, ext = ExportService.export(prompt, ExportFormat.OPENAI, metadata)

# Save to file
with open(f"prompt{ext}", "w") as f:
    f.write(content)
```

## Using export_prompt Function

```python
from src.services.export import export_prompt, ExportMetadata

metadata = ExportMetadata(
    technique="cot",
    task="Math problem",
    created_at="2024-01-15T10:30:00"
)

# Export by format key
content, extension = export_prompt(
    prompt="Your prompt...",
    format_key="markdown",  # or "json", "openai", "txt", etc.
    metadata=metadata
)

print(f"Extension: {extension}")
print(content)
```

## Format Selection Guide

| Use Case                  | Recommended Format      |
| ------------------------- | ----------------------- |
| OpenAI API integration    | OpenAI Format           |
| Anthropic API integration | Anthropic Format        |
| Documentation             | Markdown                |
| LangChain project         | LangChain               |
| LlamaIndex project        | LlamaIndex              |
| Version control           | Prompt File or Markdown |
| Quick sharing             | Plain Text              |
| Custom integration        | JSON (API)              |

## Batch Export

Export multiple prompts programmatically:

```python
from src.contrib.history.service import HistoryService
from src.services.export import export_prompt, ExportMetadata

history = HistoryService()
prompts = history.list_recent(50)

for p in prompts:
    metadata = ExportMetadata(
        technique=p.technique,
        task=p.task,
        created_at=p.created_at.isoformat(),
        tags=p.tags
    )

    content, ext = export_prompt(p.prompt, "markdown", metadata)

    filename = f"prompts/{p.id}_{p.technique}{ext}"
    with open(filename, "w") as f:
        f.write(content)
```
