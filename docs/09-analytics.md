# Analytics

Track your prompt usage, costs, and patterns over time.

## Accessing Analytics

From AI Features menu (`a`), press `a` for Analytics.

```
📊 Analytics (Last 30 Days)

┌─────────────────┬──────────────┐
│ Metric          │ Value        │
├─────────────────┼──────────────┤
│ Total Prompts   │ 156          │
│ Total Tokens    │ 45,230       │
│ Total Cost      │ $2.34        │
│ Avg Latency     │ 1,245ms      │
│ Success Rate    │ 98.5%        │
└─────────────────┴──────────────┘

Top Techniques:
  role: 45
  cot: 32
  few_shot: 28
  structured: 25
  generated: 15

Cost by Provider:
  openai: $1.89
  anthropic: $0.45
```

## Metrics Explained

### Total Prompts

Number of prompts created and executed through AI features.

### Total Tokens

Combined input and output tokens across all API calls.

### Total Cost

Estimated cost based on token usage and model pricing.

### Avg Latency

Average response time for API calls in milliseconds.

### Success Rate

Percentage of API calls that completed without errors.

## Top Techniques

Shows which prompt engineering techniques you use most:

| Technique    | Description          |
| ------------ | -------------------- |
| `role`       | Role-based prompts   |
| `cot`        | Chain of Thought     |
| `few_shot`   | Few-Shot Learning    |
| `structured` | Structured Output    |
| `generated`  | AI-generated prompts |
| `optimized`  | Optimized prompts    |
| `combined`   | Combined techniques  |

## Cost by Provider

Breakdown of spending across LLM providers:

- **OpenAI** - GPT-4, GPT-4o, GPT-3.5
- **Anthropic** - Claude models
- **Google** - Gemini models

## Data Storage

Analytics are stored in SQLite:

```
~/.promptbuilder/analytics.db
```

### Database Schema

```sql
CREATE TABLE usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    technique TEXT,
    provider TEXT,
    model TEXT,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    cost REAL DEFAULT 0,
    latency_ms INTEGER DEFAULT 0,
    success INTEGER DEFAULT 1,
    tags TEXT DEFAULT ''
)
```

## Programmatic Access

Access analytics data programmatically:

```python
from src.contrib.analytics.service import PromptAnalytics

analytics = PromptAnalytics()

# Get summary for last 30 days
summary = analytics.get_summary(days=30)
print(f"Total prompts: {summary.total_prompts}")
print(f"Total cost: ${summary.total_cost:.2f}")

# Get stats for specific technique
stats = analytics.get_technique_stats("role", days=30)
print(f"Role-based usage: {stats['usage_count']}")

# Get cost breakdown
costs = analytics.get_cost_breakdown(days=30)
for provider, data in costs['by_provider'].items():
    print(f"{provider}: ${data['cost']:.2f} ({data['count']} calls)")

# Get recent usage records
recent = analytics.get_recent_usage(limit=10)
for record in recent:
    print(f"{record.timestamp}: {record.technique} - {record.model}")

# Export data as JSON
json_data = analytics.export_data(days=30)
```

## Recording Usage

Usage is automatically recorded when using AI features. You can also record manually:

```python
analytics.record_usage(
    technique="custom",
    provider="openai",
    model="gpt-4o",
    input_tokens=150,
    output_tokens=500,
    cost=0.0065,
    latency_ms=1234,
    success=True,
    tags=["project-x", "experiment"]
)
```

## Data Management

### Export Data

```python
# Export last 30 days as JSON
json_data = analytics.export_data(days=30)
with open("analytics_export.json", "w") as f:
    f.write(json_data)
```

### Clear Old Data

```python
# Remove data older than 90 days
deleted = analytics.clear_old_data(days=90)
print(f"Deleted {deleted} old records")
```

### Backup

```bash
cp ~/.promptbuilder/analytics.db ~/.promptbuilder/analytics.db.backup
```

## Cost Optimization Tips

Based on your analytics:

1. **Use cheaper models for simple tasks**

   - gpt-4o-mini instead of gpt-4o
   - claude-3-haiku instead of claude-3-opus

2. **Optimize prompt length**

   - Shorter prompts = fewer input tokens
   - Be concise but clear

3. **Limit output tokens**

   - Set max_tokens appropriately
   - Request concise responses

4. **Batch similar requests**

   - Use prompt chains efficiently
   - Avoid redundant API calls

5. **Monitor technique efficiency**
   - Some techniques use more tokens
   - Choose based on task requirements
