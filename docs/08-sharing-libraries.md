# Sharing & Libraries

Share your prompts with others and import prompt collections.

## Accessing Sharing

From AI Features menu (`a`), press `s` for Share & Import.

```
📤 Share & Import

  [e] 📦 Export library
  [i] 📥 Import from code
  [l] 📚 List libraries
  [b] 🔙 Back
```

## Exporting a Library

Create a shareable library from your saved prompts.

### How to Export

1. Press `e` from Share & Import menu
2. Enter a library name
3. Add a description
4. Library is created from your recent prompts

```
Library name: My Best Prompts
Description: Collection of prompts for code review and debugging

✓ Exported to /Users/you/.promptbuilder/libraries/my_best_prompts.json

Share code:
pb://H4sIAAAAAAAAA6tWKkktLlGyUlAqS8wpTtVRSs7PS...
```

### What Gets Exported

- Up to 20 most recent prompts
- Prompt content
- Technique used
- Tags
- Task description

## Share Codes

Share codes are compressed, encoded strings that contain an entire library.

### Format

```
pb://[base64-encoded-gzip-compressed-json]
```

### Sharing

1. Copy the share code
2. Send via email, chat, or any text medium
3. Recipient imports using the code

### Benefits

- No file transfer needed
- Works in any text medium
- Compressed for efficiency
- Self-contained

## Importing a Library

Import prompts from a share code.

### How to Import

1. Press `i` from Share & Import menu
2. Paste the share code
3. Library is imported and saved locally

```
Paste share code: pb://H4sIAAAAAAAAA6tWKkktLlGyUlAqS8wpTtVRSs7PS...

✓ Imported 'Code Review Prompts' with 15 prompts
```

### After Import

- Library is saved to your local libraries folder
- Prompts are available for browsing
- Can be re-exported with modifications

## Listing Libraries

View all locally saved libraries.

```
📚 Local Libraries
┌─────────────────────────┬─────────┐
│ Name                    │ Prompts │
├─────────────────────────┼─────────┤
│ my_best_prompts         │ 20      │
│ code_review_prompts     │ 15      │
│ writing_templates       │ 8       │
└─────────────────────────┴─────────┘
```

## Library Storage

Libraries are stored as JSON files:

```
~/.promptbuilder/libraries/
├── my_best_prompts.json
├── code_review_prompts.json
└── writing_templates.json
```

### Library JSON Structure

```json
{
  "name": "My Best Prompts",
  "description": "Collection of prompts for code review",
  "version": "1.0.0",
  "author": "Your Name",
  "created_at": "2024-01-15T10:30:00",
  "prompts": [
    {
      "id": "abc123",
      "name": "Python Code Review",
      "technique": "role",
      "prompt": "You are a senior Python developer...",
      "description": "Thorough Python code review",
      "tags": ["python", "review"],
      "author": "",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

## Merging Libraries

Programmatically merge multiple libraries:

```python
from src.contrib.sharing.service import SharingService

sharing = SharingService()

lib1 = sharing.load_local_library("code_review")
lib2 = sharing.load_local_library("debugging")

merged = sharing.merge_libraries([lib1, lib2], "Combined Library")
sharing.export_library(merged)
```

## Use Cases

### Team Sharing

1. Create a library of team-approved prompts
2. Export and share the code
3. Team members import to get started quickly

### Backup

1. Export your best prompts periodically
2. Save the JSON files or share codes
3. Import to restore on new machines

### Community Sharing

1. Create libraries for specific domains
2. Share codes on forums, GitHub, etc.
3. Build a collection of community prompts

## Best Practices

1. **Curate before sharing** - Only include high-quality prompts
2. **Add descriptions** - Help others understand the library's purpose
3. **Use meaningful names** - Make libraries easy to identify
4. **Version your libraries** - Track changes over time
5. **Test imported prompts** - Verify they work in your context
