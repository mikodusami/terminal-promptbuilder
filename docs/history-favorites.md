# History & Favorites

All prompts you create are automatically saved to a local SQLite database for easy retrieval.

## Browsing History

Press `h` from the main menu to browse recent prompts.

```
📜 Recent Prompts
┌────┬────────────┬───────────────────────────────────┬───────────────┬────┐
│ #  │ Technique  │ Task                              │ Tags          │ ⭐ │
├────┼────────────┼───────────────────────────────────┼───────────────┼────┤
│ 1  │ role       │ Explain neural networks for be... │ ml, tutorial  │    │
│ 2  │ cot        │ Debug this Python function        │ python, debug │ ⭐ │
│ 3  │ structured │ Generate API documentation        │ api, docs     │    │
│ 4  │ few_shot   │ Classify customer feedback        │ nlp           │ ⭐ │
│ 5  │ combined   │ Design a microservices archit... │ architecture  │    │
└────┴────────────┴───────────────────────────────────┴───────────────┴────┘

Select # (or Enter to go back):
```

## Viewing a Saved Prompt

Select a prompt by number to view its full content:

```
╔══════════════════════════════════════════════════════════════════════════╗
║ ROLE - Explain neural networks for beginners                             ║
╠══════════════════════════════════════════════════════════════════════════╣
║ You are a machine learning researcher with 10 years experience.          ║
║                                                                          ║
║ Background: For a blog post targeting beginners with no ML background    ║
║                                                                          ║
║ Your task: Explain how neural networks learn                             ║
║ ...                                                                      ║
╠══════════════════════════════════════════════════════════════════════════╣
║ ID: 42 | Created: 2024-01-15 14:30                                       ║
╚══════════════════════════════════════════════════════════════════════════╝

Actions: [c]=copy [f]=toggle favorite [s]=save file [d]=delete [b]=back
Action:
```

### Available Actions

| Key | Action   | Description              |
| --- | -------- | ------------------------ |
| `c` | Copy     | Copy prompt to clipboard |
| `f` | Favorite | Toggle favorite status   |
| `s` | Save     | Export to file           |
| `d` | Delete   | Remove from history      |
| `b` | Back     | Return to list           |

## Favorites

Press `f` from the main menu to view only your favorite prompts.

### Adding to Favorites

You can add a prompt to favorites:

1. After creating a new prompt (press `f` in actions)
2. When viewing a saved prompt (press `f`)
3. From the history list (select prompt, then `f`)

### Removing from Favorites

Press `f` again on a favorited prompt to remove it from favorites.

## Searching Prompts

Press `s` from the main menu to search your saved prompts.

```
🔍 Search: neural network

🔍 Results for 'neural network'
┌────┬────────────┬───────────────────────────────────┬───────────────┬────┐
│ #  │ Technique  │ Task                              │ Tags          │ ⭐ │
├────┼────────────┼───────────────────────────────────┼───────────────┼────┤
│ 1  │ role       │ Explain neural networks for be... │ ml, tutorial  │    │
│ 2  │ cot        │ How do neural networks backpro... │ ml, math      │ ⭐ │
└────┴────────────┴───────────────────────────────────┴───────────────┴────┘
```

### Search Scope

Search looks in:

- Task/question text
- Tags
- Prompt content

## Tags

Tags help organize and find your prompts.

### Adding Tags

When creating a prompt, you're asked for tags:

```
🏷️ Tags (comma-separated, Enter to skip): python, debugging, async
```

### Tag Best Practices

- Use lowercase for consistency
- Keep tags short and descriptive
- Use common categories: `python`, `javascript`, `api`, `debug`, `tutorial`
- Add project-specific tags: `project-x`, `client-abc`

## Data Storage

History is stored in SQLite at:

```
~/.promptbuilder/history.db
```

### Database Schema

```sql
CREATE TABLE prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    technique TEXT NOT NULL,
    task TEXT NOT NULL,
    prompt TEXT NOT NULL,
    tags TEXT DEFAULT '',
    is_favorite INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
```

## Backup & Restore

### Backup

```bash
cp ~/.promptbuilder/history.db ~/.promptbuilder/history.db.backup
```

### Restore

```bash
cp ~/.promptbuilder/history.db.backup ~/.promptbuilder/history.db
```

## Clearing History

To clear all history, delete the database file:

```bash
rm ~/.promptbuilder/history.db
```

A new database will be created on next launch.
