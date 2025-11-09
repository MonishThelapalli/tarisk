"""Configuration module initialization.

Exports the settings helpers that the rest of the codebase expects. The
settings module was refactored to use Google Gemini and general-purpose
environment variables; this file re-exports the new names for convenience.
"""

from .settings import (
    AI_MODEL_PROVIDER,
    AI_MODEL_NAME,
    GOOGLE_API_KEY,
    DB_CONNECTION_STRING,
    get_database_connection_string,
    create_genai_client,
    STORAGE_PATH,
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    SEARCH_PROVIDER,
    SEARCH_API_KEY,
    APP_ENV,
    LOG_LEVEL,
    PORT
)

__all__ = [
    'GOOGLE_API_KEY',
    'AI_MODEL_PROVIDER',
    'AI_MODEL_NAME',
    'DB_CONNECTION_STRING',
    'STORAGE_PATH',
    'SEARCH_PROVIDER',
    'SEARCH_API_KEY',
    'ensure_storage_path',
    'create_genai_client',
    'is_sqlite_connection'
]