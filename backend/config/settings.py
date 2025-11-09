"""Configuration settings for the application.

This module replaces the previous Azure-specific settings with Google Gemini
and general-purpose environment variables. It provides lightweight
compatibility shims so the rest of the codebase can continue to import the
same helpers but now route AI calls through Google GenAI (Gemini) and
search calls through a pluggable provider (default: Serper.dev).

Changes made:
- Removed azure.* imports and logic.
- Added environment variables for GOOGLE_API_KEY, AI_MODEL_PROVIDER, AI_MODEL_NAME,
  DB_CONNECTION_STRING (defaults to sqlite), STORAGE_PATH, SEARCH_PROVIDER,
  SEARCH_API_KEY.
- Added helper to create a google.genai client if GOOGLE_API_KEY is provided.

Note: Full runtime replacement of the semantic_kernel/Azure agent runtime is
non-trivial; this file provides the configuration and client factory helpers
that other modules can use to integrate Gemini. Agent runtime wrappers
(compatibility shims) are implemented in agent_manager.py.
"""

import os
from typing import Optional


from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# AI Model Settings
AI_MODEL_PROVIDER = os.getenv("AI_MODEL_PROVIDER", "google")
AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "gemini-2.5-pro")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Database Settings
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING", "sqlite:///local.db")

# Storage Settings
STORAGE_PATH = os.getenv("STORAGE_PATH", "./uploads")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Search Settings
SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER", "serper")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")

# App Settings
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
PORT = int(os.getenv("PORT", "8000"))

def get_database_connection_string():
    """Get the database connection string from environment variables."""
    return DB_CONNECTION_STRING

def ensure_storage_path():
    """Ensure the configured storage path exists and return it."""
    try:
        os.makedirs(STORAGE_PATH, exist_ok=True)
    except Exception:
        fallback = os.path.join(os.getcwd(), "uploads")
        try:
            os.makedirs(fallback, exist_ok=True)
            return fallback
        except Exception:
            return "."
    return STORAGE_PATH

def create_genai_client():
    """Create and return a google.genai client."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set")
    try:
        import google.generativeai as genai
        return genai.GenerativeModel(model_name=AI_MODEL_NAME)
    except ImportError:
        raise ImportError("Install google-generativeai: pip install google-generativeai")

def is_sqlite_connection(conn_str: Optional[str]) -> bool:
    """Check if connection string is for SQLite."""
    if not conn_str:
        return True
    lower = conn_str.lower()
    return lower.startswith("sqlite:") or lower.endswith(".sqlite") or lower.endswith(".db")
def ensure_storage_path():
    """Ensure the configured storage path exists and return it."""
    try:
        os.makedirs(STORAGE_PATH, exist_ok=True)
    except Exception:
        # Best-effort: if creation fails, fall back to CWD ./uploads
        fallback = os.path.join(os.getcwd(), "uploads")
        try:
            os.makedirs(fallback, exist_ok=True)
            return fallback
        except Exception:
            return "."
    return STORAGE_PATH


def create_genai_client():
    """Create and return a google.genai client configured with GOOGLE_API_KEY.

    Returns a client object or raises ValueError if configuration is missing.

    The actual google.genai package must be installed in the environment for
    this to succeed. We keep this factory lightweight so other modules can
    import and use it. If the package is not available, an informative
    ImportError is raised.
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set in environment variables")

    try:
        # eslint: disable - local import to avoid hard dependency at import time
        import google.genai as genai
    except Exception as e:
        raise ImportError(
            "google.genai package is required to use Gemini. Install it with: pip install google-genai"
        ) from e

    # The google.genai.Client accepts an API key in different forms; keep it
    # simple and provide the common pattern.
    client = genai.Client(api_key=GOOGLE_API_KEY)
    return client


def is_sqlite_connection(conn_str: Optional[str]) -> bool:
    if not conn_str:
        return True
    lower = conn_str.lower()
    return lower.startswith("sqlite:") or lower.endswith(".sqlite") or lower.endswith(".db")
