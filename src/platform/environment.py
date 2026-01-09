"""
Environment utilities - paths, directories, environment variables.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


APP_NAME = "promptbuilder"


def get_config_dir() -> Path:
    """Get the configuration directory path."""
    config_dir = Path.home() / f".{APP_NAME}"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_data_dir() -> Path:
    """Get the data directory path."""
    return get_config_dir()


def get_plugins_dir() -> Path:
    """Get the plugins directory path."""
    plugins_dir = get_config_dir() / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    return plugins_dir


def get_env(key: str, default: str = None) -> str | None:
    """Get environment variable."""
    return os.getenv(key, default)
