"""
Contrib module - feature contributions (similar to VS Code's contrib).

Each feature is self-contained with its own:
- service.py: Business logic and types
"""

# Feature registry for dynamic loading
FEATURES = [
    "history",
    "templates",
    "optimizer",
    "testing",
    "chains",
    "sharing",
    "analytics",
    "nlgen",
    "variables",
    "plugins",
]
