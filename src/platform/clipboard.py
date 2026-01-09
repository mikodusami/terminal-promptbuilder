"""
Clipboard utilities for cross-platform clipboard access.
"""

import subprocess
import platform

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to clipboard.
    Tries pyperclip first, falls back to OS-specific methods.
    Returns True if successful.
    """
    if PYPERCLIP_AVAILABLE:
        try:
            pyperclip.copy(text)
            return True
        except Exception:
            pass
    
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            process = subprocess.Popen(
                ["pbcopy"],
                stdin=subprocess.PIPE,
                close_fds=True
            )
            process.communicate(input=text.encode("utf-8"))
            return process.returncode == 0
        
        elif system == "Linux":
            for cmd in [["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]]:
                try:
                    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, close_fds=True)
                    process.communicate(input=text.encode("utf-8"))
                    if process.returncode == 0:
                        return True
                except FileNotFoundError:
                    continue
            return False
        
        elif system == "Windows":
            process = subprocess.Popen(["clip"], stdin=subprocess.PIPE, close_fds=True)
            process.communicate(input=text.encode("utf-16"))
            return process.returncode == 0
        
    except Exception:
        pass
    
    return False


def is_clipboard_available() -> bool:
    """Check if clipboard functionality is available."""
    if PYPERCLIP_AVAILABLE:
        return True
    
    system = platform.system()
    
    if system == "Darwin":
        return True
    elif system == "Linux":
        for cmd in ["xclip", "xsel"]:
            try:
                subprocess.run([cmd, "--version"], capture_output=True)
                return True
            except FileNotFoundError:
                continue
        return False
    elif system == "Windows":
        return True
    
    return False
