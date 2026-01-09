# Settings & Configuration

Configure API keys and application settings.

## Accessing Settings

Press `c` from the main menu to open Settings.

```
⚙️ Settings

API Keys Status:
  Openai: ✓ Configured
  Anthropic: ✓ Configured
  Google: ✗ Not set

  [o] 🔑 Set OpenAI key
  [a] 🔑 Set Anthropic key
  [g] 🔑 Set Google key
  [b] 🔙 Back
```

## Setting API Keys

### Via Settings Menu

1. Press `c` from main menu
2. Select provider (`o`, `a`, or `g`)
3. Enter your API key (input is hidden)
4. Key is saved and validated

```
Enter OpenAI API key: ********
✓ OpenAI API key saved
```

### Via Environment Variables

Set environment variables before running:

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Google
export GOOGLE_API_KEY="AIza..."
```

Or create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
```

### Via Config File

Keys are stored in:

```
~/.promptbuilder/api_config.json
```

```json
{
  "openai": {
    "api_key": "sk-...",
    "base_url": null
  },
  "anthropic": {
    "api_key": "sk-ant-...",
    "base_url": null
  },
  "google": {
    "api_key": "AIza...",
    "base_url": null
  }
}
```

## Priority Order

API keys are loaded in this order (first found wins):

1. Environment variables
2. Config file (`~/.promptbuilder/api_config.json`)

## Supported Providers

### OpenAI

| Model         | Input/1K | Output/1K |
| ------------- | -------- | --------- |
| gpt-4o        | $0.0025  | $0.01     |
| gpt-4o-mini   | $0.00015 | $0.0006   |
| gpt-4-turbo   | $0.01    | $0.03     |
| gpt-3.5-turbo | $0.0005  | $0.0015   |

Get your key: https://platform.openai.com/api-keys

### Anthropic

| Model             | Input/1K | Output/1K |
| ----------------- | -------- | --------- |
| claude-3-5-sonnet | $0.003   | $0.015    |
| claude-3-opus     | $0.015   | $0.075    |
| claude-3-haiku    | $0.00025 | $0.00125  |

Get your key: https://console.anthropic.com/

### Google

| Model            | Input/1K | Output/1K |
| ---------------- | -------- | --------- |
| gemini-1.5-pro   | Varies   | Varies    |
| gemini-1.5-flash | Varies   | Varies    |
| gemini-pro       | Varies   | Varies    |

Get your key: https://makersuite.google.com/app/apikey

## Custom Base URLs

For OpenAI-compatible APIs (Azure, local models):

```json
{
  "openai": {
    "api_key": "your-key",
    "base_url": "https://your-endpoint.openai.azure.com/"
  }
}
```

## Configuration Files

All configuration is stored in:

```
~/.promptbuilder/
├── api_config.json      # API keys
├── history.db           # Prompt history
├── analytics.db         # Usage analytics
├── templates.yaml       # Custom templates
├── chains.json          # Prompt chains
├── variable_templates.json  # Variable templates
└── libraries/           # Shared libraries
    └── *.json
```

## Security Best Practices

1. **Never commit API keys** - Add config files to `.gitignore`
2. **Use environment variables** - Preferred for production
3. **Rotate keys regularly** - Update if compromised
4. **Set spending limits** - Configure in provider dashboards
5. **Monitor usage** - Check analytics regularly

## Troubleshooting

### "No API keys configured"

1. Check Settings menu for status
2. Verify environment variables are set
3. Check config file exists and is valid JSON

### "API key invalid"

1. Verify key is correct (no extra spaces)
2. Check key hasn't expired
3. Ensure key has required permissions

### "Model not available"

1. Verify your API key has access to the model
2. Check provider's model availability
3. Some models require special access

### Connection errors

1. Check internet connection
2. Verify provider's API status
3. Check for firewall/proxy issues

## Resetting Configuration

To reset all configuration:

```bash
rm -rf ~/.promptbuilder
```

A fresh configuration will be created on next launch.

## Programmatic Configuration

```python
from src.services.llm.config import LLMConfig

config = LLMConfig()

# Set API key
config.set_api_key("openai", "sk-...")

# Check available providers
providers = config.get_available_providers()
print(f"Available: {providers}")

# Get available models
models = config.get_available_models()
for provider, model in models:
    print(f"{provider}: {model}")

# Check if any provider is configured
if config.has_any_provider():
    print("AI features available")
```
