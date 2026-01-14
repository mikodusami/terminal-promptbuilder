# Getting Started

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/promptbuilder.git
cd promptbuilder
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## First Launch

When you first launch Prompt Builder, you'll see the main menu:

```
⚡ PROMPT BUILDER ⚡
Modern Prompt Engineering Techniques

Main Menu:

  [n] ✨ New Prompt    - Create a new prompt
  [m] 🔗 Combine       - Chain multiple techniques
  [t] 📦 Templates     - Use custom templates
  [h] 📜 History       - Browse recent prompts
  [f] ⭐ Favorites     - View favorite prompts
  [s] 🔍 Search        - Search saved prompts
  [p] 👁️  Preview Mode  - OFF - Live prompt preview
  [a] 🤖 AI Features ○ - Optimize, generate, test, chains
  [c] ⚙️  Settings      - API keys & configuration
  [q] 🚪 Quit          - Exit the builder
```

## Setting Up API Keys (Optional)

AI features require at least one LLM provider API key. You can set these up in Settings (`c`):

1. Press `c` to open Settings
2. Choose a provider:
   - `o` for OpenAI
   - `a` for Anthropic
   - `g` for Google
3. Enter your API key

Alternatively, set environment variables:

```bash
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
export GOOGLE_API_KEY="your-key-here"
```

## Basic Workflow

1. Press `n` to create a new prompt
2. Select a technique (1-7)
3. Enter your task/question
4. Add optional context
5. Configure technique-specific options
6. View the generated prompt
7. Copy to clipboard, save to file, or add to favorites

## Tips

- Enable Preview Mode (`p`) to see your prompt build in real-time
- All prompts are automatically saved to history
- Use tags to organize your prompts for easy searching
- The green dot (●) next to AI Features indicates API keys are configured
