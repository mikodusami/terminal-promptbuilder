"""
Template Manager - Custom prompt templates from YAML configuration.
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@dataclass
class CustomTemplate:
    name: str
    description: str
    icon: str
    color: str
    template: str
    variables: list[str]


DEFAULT_TEMPLATES_YAML = """
# Custom Prompt Templates
# Add your own templates below

templates:
  code_review:
    name: "Code Review"
    description: "Thorough code review with best practices"
    icon: "🔍"
    color: "cyan"
    template: |
      You are a senior software engineer conducting a code review.
      
      Context: {context}
      
      Review the following code for:
      1. Code quality and readability
      2. Potential bugs or edge cases
      3. Performance considerations
      4. Security vulnerabilities
      5. Best practices and patterns
      
      Code to review:
      {task}
      
      Provide specific, actionable feedback with code examples where helpful.
    variables:
      - task
      - context

  explain_like_5:
    name: "Explain Like I'm 5"
    description: "Simple explanations for complex topics"
    icon: "👶"
    color: "green"
    template: |
      Explain this concept in the simplest possible terms, as if explaining to a 5-year-old:
      
      Topic: {task}
      
      Use:
      - Simple words and short sentences
      - Relatable analogies and examples
      - No jargon or technical terms
      - A friendly, encouraging tone
    variables:
      - task

  debug_helper:
    name: "Debug Helper"
    description: "Systematic debugging assistance"
    icon: "🐛"
    color: "red"
    template: |
      Help me debug this issue systematically.
      
      Problem: {task}
      
      Context/Error message: {context}
      
      Please:
      1. Identify potential root causes
      2. Suggest diagnostic steps to isolate the issue
      3. Propose solutions in order of likelihood
      4. Explain how to prevent this in the future
    variables:
      - task
      - context

  refactor:
    name: "Refactor Code"
    description: "Improve code structure and quality"
    icon: "♻️"
    color: "yellow"
    template: |
      Refactor the following code to improve its quality.
      
      Code: {task}
      
      Focus on: {context}
      
      Apply these principles:
      - DRY (Don't Repeat Yourself)
      - Single Responsibility
      - Clear naming conventions
      - Appropriate abstractions
      
      Show the refactored code with explanations for each change.
    variables:
      - task
      - context

  api_design:
    name: "API Design"
    description: "Design RESTful APIs"
    icon: "🔌"
    color: "magenta"
    template: |
      Design a RESTful API for the following requirement:
      
      Requirement: {task}
      
      Additional context: {context}
      
      Include:
      1. Endpoint definitions (method, path, description)
      2. Request/response schemas
      3. Error handling approach
      4. Authentication considerations
      5. Example requests and responses
    variables:
      - task
      - context
"""


class TemplateManager:
    """Manage custom prompt templates."""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_dir = Path.home() / ".promptbuilder"
            config_dir.mkdir(exist_ok=True)
            config_path = str(config_dir / "templates.yaml")
        
        self.config_path = config_path
        self._ensure_config_exists()
        self.templates = self._load_templates()

    def _ensure_config_exists(self):
        """Create default config if it doesn't exist."""
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as f:
                f.write(DEFAULT_TEMPLATES_YAML)

    def _load_templates(self) -> dict[str, CustomTemplate]:
        """Load templates from YAML config."""
        if not YAML_AVAILABLE:
            return {}
        
        try:
            with open(self.config_path, 'r') as f:
                data = yaml.safe_load(f)
            
            templates = {}
            for key, config in data.get('templates', {}).items():
                templates[key] = CustomTemplate(
                    name=config.get('name', key),
                    description=config.get('description', ''),
                    icon=config.get('icon', '📝'),
                    color=config.get('color', 'white'),
                    template=config.get('template', ''),
                    variables=config.get('variables', [])
                )
            return templates
        except Exception as e:
            print(f"Warning: Could not load templates: {e}")
            return {}

    def reload(self):
        """Reload templates from config file."""
        self.templates = self._load_templates()

    def list_templates(self) -> list[CustomTemplate]:
        """List all available custom templates."""
        return list(self.templates.values())

    def get_template(self, key: str) -> Optional[CustomTemplate]:
        """Get a template by key."""
        return self.templates.get(key)

    def build_prompt(self, key: str, variables: dict[str, str]) -> str:
        """Build a prompt from a template with variables."""
        template = self.templates.get(key)
        if not template:
            raise ValueError(f"Template '{key}' not found")
        
        prompt = template.template
        for var in template.variables:
            value = variables.get(var, '')
            prompt = prompt.replace(f"{{{var}}}", value)
        
        return prompt.strip()

    def add_template(self, key: str, template: CustomTemplate) -> bool:
        """Add a new template to the config file."""
        if not YAML_AVAILABLE:
            return False
        
        try:
            with open(self.config_path, 'r') as f:
                data = yaml.safe_load(f) or {'templates': {}}
            
            data['templates'][key] = {
                'name': template.name,
                'description': template.description,
                'icon': template.icon,
                'color': template.color,
                'template': template.template,
                'variables': template.variables
            }
            
            with open(self.config_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            
            self.templates[key] = template
            return True
        except Exception as e:
            print(f"Error saving template: {e}")
            return False

    def get_config_path(self) -> str:
        """Return the config file path."""
        return self.config_path
