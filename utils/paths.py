"""Path utility functions."""

import os
from pathlib import Path


def abspath(path: str) -> str:
    """Get absolute path, resolving ~ and relative paths."""
    expanded = os.path.expanduser(path)
    return os.path.abspath(expanded)


def is_file_readable(path: str) -> bool:
    """Check if a file exists and is readable."""
    try:
        return os.path.isfile(path) and os.access(path, os.R_OK)
    except Exception:
        return False


def is_dir_empty(path: str) -> bool:
    """Check if a directory is empty."""
    try:
        return len(os.listdir(path)) == 0
    except Exception:
        return True


def get_file_extension(path: str) -> str:
    """Get file extension without the dot."""
    return os.path.splitext(path)[1].lstrip('.')


def ensure_dir_exists(path: str) -> bool:
    """Create directory if it doesn't exist."""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception:
        return False
