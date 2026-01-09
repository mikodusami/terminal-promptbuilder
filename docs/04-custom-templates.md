# Custom Templates

Custom templates allow you to create reusable prompt patterns with variables.

## Accessing Templates

From the main menu, press `t` to access custom templates.

## Default Templates

Prompt Builder comes with built-in templates:

### Code Review 🔍

Thorough code review with best practices analysis.

### Explain Like I'm 5 👶

Simple explanations for complex topics.

### Debug Helper 🐛

Systematic debugging assistance.

### Refactor ♻️

Improve code structure and quality.

### API Design 🔌

Design RESTful APIs with schemas.

## Using a Template

1. Press `t` from main menu
2. Select a template by number
3. Fill in the required variables
4. View and use the generated prompt

```
Custom Templates:

  [1] 🔍 Code Review         - Thorough code review with best practices
  [2] 👶 Explain Like I'm 5  - Simple explanations for complex topics
  [3] 🐛 Debug Helper        - Systematic debugging assistance
  [4] ♻️  Refactor            - Improve code structure and quality
  [5] 🔌 API Design          - Design RESTful APIs
  [b] 🔙 Back

Select template: 1

╭─ Code Review ─────────────────────────────────────────╮
│ Thorough code review with best practices              │
╰───────────────────────────────────────────────────────╯

task: [paste your code here]
context: Python web application using FastAPI
```

## Creating Custom Templates

Templates are stored in YAML format at:

```
~/.promptbuilder/templates.yaml
```

### Template Structure

```yaml
templates:
  my_template:
    name: "My Template Name"
    description: "What this template does"
    icon: "🎯"
    color: "cyan"
    template: |
      Your prompt template here.

      Use {variable_name} for placeholders.

      Task: {task}
      Context: {context}
    variables:
      - task
      - context
```

### Example: Bug Report Template

```yaml
templates:
  bug_report:
    name: "Bug Report Analysis"
    description: "Analyze and suggest fixes for bug reports"
    icon: "🐞"
    color: "red"
    template: |
      Analyze this bug report and provide:
      1. Root cause analysis
      2. Potential fixes
      3. Prevention strategies

      Bug Description: {bug_description}

      Error Message: {error_message}

      Steps to Reproduce: {steps}

      Environment: {environment}

      Please provide a detailed analysis with code examples where applicable.
    variables:
      - bug_description
      - error_message
      - steps
      - environment
```

### Example: Meeting Summary Template

```yaml
templates:
  meeting_summary:
    name: "Meeting Summary"
    description: "Generate structured meeting summaries"
    icon: "📝"
    color: "blue"
    template: |
      Create a structured summary of this meeting.

      Meeting Notes:
      {notes}

      Attendees: {attendees}

      Please provide:
      1. Key Discussion Points
      2. Decisions Made
      3. Action Items (with owners and deadlines)
      4. Follow-up Required

      Format the output in Markdown.
    variables:
      - notes
      - attendees
```

## Template Variables

Variables use the `{variable_name}` syntax:

- Variables are listed in the `variables` array
- Each variable prompts the user for input
- Variables can be used multiple times in the template

### Variable Best Practices

1. Use descriptive names: `{code_snippet}` not `{c}`
2. Keep variables focused: one concept per variable
3. Order variables logically in the array
4. Consider which variables are truly needed

## Template Colors

Available colors for the `color` field:

- `cyan`
- `green`
- `magenta`
- `yellow`
- `red`
- `blue`
- `white`

## Template Icons

Use any emoji for the `icon` field. Common choices:

- 🔍 Analysis/Review
- 🐛 Debugging
- 📝 Writing
- 🎯 Goals/Tasks
- 💡 Ideas
- ⚡ Performance
- 🔒 Security
- 📊 Data

## Reloading Templates

Templates are loaded when the application starts. To reload after editing:

1. Exit the application (`q`)
2. Restart with `python main.py`

## Sharing Templates

Share your templates by:

1. Copying your `templates.yaml` file
2. Sharing the YAML content
3. Others paste into their `~/.promptbuilder/templates.yaml`
