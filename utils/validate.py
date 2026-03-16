"""Validation utilities."""

import os
from utils.paths import abspath


def validate_materials_dir(materials_dir: str) -> tuple[bool, str]:
    """Validate that materials directory exists and is readable."""
    abs_path = abspath(materials_dir)
    
    if not os.path.isdir(abs_path):
        return False, abs_path
    
    if not os.access(abs_path, os.R_OK):
        return False, abs_path
    
    return True, abs_path


def validate_query(query: str) -> bool:
    """Validate search query."""
    return bool(query and query.strip())


def validate_topic(topic: str) -> bool:
    """Validate topic name."""
    return bool(topic and topic.strip())


def validate_topics(topic1: str, topic2: str) -> bool:
    """Validate two topics."""
    return validate_topic(topic1) and validate_topic(topic2)


def validate_file_extension(filename: str, allowed_extensions: list[str]) -> bool:
    """Validate file extension."""
    _, ext = os.path.splitext(filename)
    ext = ext.lstrip('.').lower()
    return ext in [e.lower() for e in allowed_extensions]
