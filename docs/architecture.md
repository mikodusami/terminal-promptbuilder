# Architecture Documentation

## Overview

Prompt Builder is a command-line tool for creating exceptional prompts using modern prompt engineering techniques. The codebase follows a modular architecture with clear separation of concerns between core functionality, platform abstractions, services, and feature contributions.

## Project Structure

```
prompt-builder/
├── main.py                    # CLI entry point and interactive interface
├── src/                       # Source code root
│   ├── core/                  # Core prompt building logic
│   ├── platform/              # Platform abstractions (OS, clipboard, storage)
│   ├── services/              # Shared services (tokens, export, LLM)
│   └── contrib/               # Feature contributions (modular features)
├── tests/                     # Test suite
├── docs/                      # Documentation
└── files/                     # Example files and outputs
```

## Architecture Layers

### 1. Core Layer (`src/core/`)

The foundation of the prompt building system. Contains the essential business logic for creating prompts using various techniques.

**Files:**

- `types.py` - Core type definitions and enums (PromptType, etc.)
- `config.py` - Configuration classes for prompt building
- `builder.py` - Main PromptBuilder class that orchestrates prompt generation
- `__init__.py` - Public API exports

**Responsibilities:**

- Define prompt engineering techniques (Chain of Thought, Few-Shot, Role-Based, etc.)
- Implement prompt generation algorithms
- Provide the core API for building prompts

**Dependencies:** None (self-contained)

### 2. Platform Layer (`src/platform/`)

Abstracts platform-specific functionality to ensure cross-platform compatibility.

**Files:**

- `clipboard.py` - Clipboard operations (copy/paste)
- `environment.py` - Environment variable handling
- `storage.py` - File system and data persistence abstractions

**Responsibilities:**

- Handle OS-specific operations
- Provide unified interfaces for platform features
- Manage file I/O and storage paths

**Dependencies:** Standard library only

### 3. Services Layer (`src/services/`)

Shared services that provide functionality across multiple features.

**Files:**

- `token_counter.py` - Token counting and cost estimation for LLM models
- `export.py` - Export prompts to various formats (JSON, Markdown, LangChain, etc.)
- `context.py` - Context window management for LLMs
- `llm/` - LLM provider integration
  - `config.py` - API key and provider configuration
  - `client.py` - Unified client for OpenAI, Anthropic, Google

**Responsibilities:**

- Token counting and cost calculation
- Format conversion and export
- LLM API communication
- Context management

**Dependencies:** Core layer, external libraries (tiktoken, openai, anthropic, google-generativeai)

### 4. Contrib Layer (`src/contrib/`)

Modular feature contributions inspired by VS Code's architecture. Each feature is self-contained and can be developed independently.

**Structure Pattern:**
Each contrib module follows a consistent pattern:

```
contrib/<feature>/
├── __init__.py      # Public exports
├── common.py        # Types, dataclasses, constants
└── service.py       # Business logic and implementation
```

**Features:**

#### `analytics/`

- Track usage statistics, costs, and performance metrics
- Generate analytics dashboards
- Dependencies: Services layer

#### `chains/`

- Multi-step prompt workflows
- Chain execution with output passing between steps
- Built-in chain templates
- Dependencies: Core, Services (LLM)

#### `history/`

- SQLite-backed prompt storage
- Search, tagging, and favorites
- Prompt versioning
- Dependencies: Platform (storage)

#### `nlgen/` (Natural Language Generation)

- Convert plain English descriptions to optimized prompts
- Technique recommendation
- Dependencies: Services (LLM)

#### `optimizer/`

- AI-powered prompt analysis and improvement
- Scoring (clarity, specificity, effectiveness)
- Suggestion generation
- Dependencies: Services (LLM)

#### `templates/`

- YAML-based custom template system
- Variable interpolation
- Template library management
- Dependencies: Platform (storage)

#### `testing/`

- Multi-model prompt testing
- Compare outputs across providers
- Test case management
- Dependencies: Services (LLM)

#### `variables/`

- Variable interpolation in prompts
- Dynamic value substitution
- Dependencies: Core

**Design Principles:**

- Each feature is independently testable
- Minimal coupling between features
- Clear service boundaries
- Shared types in `common.py`, logic in `service.py`

### 5. Tests Layer (`tests/`)

Mirrors the source structure for easy navigation.

```
tests/
├── test_core/           # Core layer tests
│   └── test_builder.py
└── test_services/       # Services layer tests
    ├── test_export.py
    └── test_token_counter.py
```

**Testing Strategy:**

- Unit tests for core logic
- Integration tests for services
- Mock external dependencies (LLM APIs)

## Data Flow

### Prompt Creation Flow

```
User Input (main.py)
    ↓
Core Builder (src/core/builder.py)
    ↓
Prompt Generation
    ↓
Services (token counting, export)
    ↓
Contrib Features (history, analytics)
    ↓
Output (clipboard, file, display)
```

### AI Feature Flow

```
User Request (main.py)
    ↓
Contrib Feature (optimizer/nlgen/testing)
    ↓
Services (LLM client)
    ↓
External API (OpenAI/Anthropic/Google)
    ↓
Response Processing
    ↓
Display Results
```

## Key Design Patterns

### 1. Service Pattern

Each major feature is encapsulated in a service class with clear responsibilities:

- `PromptBuilder` - Core prompt generation
- `HistoryService` - Prompt storage and retrieval
- `TemplateService` - Template management
- `OptimizerService` - Prompt optimization
- `TestingService` - Multi-model testing

### 2. Configuration Objects

Immutable configuration objects passed to services:

- `PromptConfig` - Prompt building parameters
- `LLMConfig` - API keys and model settings
- `ExportMetadata` - Export context

### 3. Type Safety

Strong typing throughout with:

- Enums for technique types
- Dataclasses for structured data
- Type hints for all public APIs

### 4. Dependency Injection

Services receive dependencies through constructors:

```python
optimizer = OptimizerService(llm_client)
test_suite = TestingService(llm_client)
```

## Extension Points

### Adding a New Prompt Technique

1. Add enum to `src/core/types.py`
2. Implement builder method in `src/core/builder.py`
3. Add UI option in `main.py`

### Adding a New Contrib Feature

1. Create `src/contrib/<feature>/` directory
2. Add `common.py` with types
3. Add `service.py` with business logic
4. Register in `src/contrib/__init__.py`
5. Integrate in `main.py`

### Adding a New Export Format

1. Add format handler in `src/services/export.py`
2. Register in `FORMAT_INFO` dictionary
3. Update UI in `main.py`

## Configuration Management

### Environment Variables

- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `GOOGLE_API_KEY` - Google AI API key

### Configuration Files

- `.env` - Environment variables (not committed)
- `~/.promptbuilder/templates.yaml` - Custom templates
- `~/.promptbuilder/prompts.db` - SQLite history database

## Dependencies

### Core Dependencies (Required)

- `rich` - Terminal UI and formatting
- `pyyaml` - Template parsing
- `tiktoken` - Token counting

### Optional Dependencies (AI Features)

- `openai` - OpenAI API client
- `anthropic` - Anthropic API client
- `google-generativeai` - Google AI client

### Development Dependencies

- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting

## Performance Considerations

- **Lazy Loading**: AI features only loaded when needed
- **Caching**: Token counts cached per model
- **Database Indexing**: History searches use indexed queries
- **Async Support**: LLM calls can be parallelized (future enhancement)

## Security Considerations

- API keys stored in environment variables or `.env` (gitignored)
- No sensitive data in prompt history by default
- User confirmation for destructive operations
- Input sanitization for file operations

## Future Architecture Enhancements

1. **Plugin System**: Dynamic feature loading from external packages
2. **Async/Await**: Non-blocking LLM API calls
3. **Streaming**: Real-time response streaming for long outputs
4. **Multi-User**: Support for team collaboration features
5. **Web Interface**: Optional web UI alongside CLI
6. **API Server**: REST API for programmatic access

## Conclusion

The Prompt Builder architecture prioritizes:

- **Modularity**: Clear separation of concerns
- **Extensibility**: Easy to add new features
- **Testability**: Isolated components with clear interfaces
- **Maintainability**: Consistent patterns and structure
- **User Experience**: Rich CLI with optional AI features
