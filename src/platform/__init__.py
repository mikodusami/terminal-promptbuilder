"""
Platform module - OS-level services and abstractions.
"""

from .environment import get_config_dir, get_data_dir
from .clipboard import copy_to_clipboard, is_clipboard_available
from .storage import BaseStorage

__all__ = [
    "get_config_dir",
    "get_data_dir", 
    "copy_to_clipboard",
    "is_clipboard_available",
    "BaseStorage"
]
