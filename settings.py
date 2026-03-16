"""Configuration settings."""

import os

# Directories
MATERIALS_DIR = os.getenv("MATERIALS_DIR", "study_materials")
CACHE_DIR = os.getenv("CACHE_DIR", "cache")

# Server settings
SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

# Document processing
SUPPORTED_FORMATS = ["txt", "pdf", "md"]
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
MAX_SNIPPETS = 3

# Search settings
DEFAULT_TOP_K = 5
MAX_TOP_K = 20

# Importance ranking
IMPORTANCE_THRESHOLD = 0.5

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
