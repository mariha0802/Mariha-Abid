"""LangChain cache configuration."""

from __future__ import annotations

from pathlib import Path

from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache


def configure_cache(cache_type: str, database_path: str = "finwise_cache.db"):
    """Configure LangChain's global LLM cache.

    Returns the cache instance so the caller can display its active mode.
    """
    if cache_type == "SQLite cache":
        db_path = Path(database_path).resolve()
        cache = SQLiteCache(database_path=str(db_path))
    else:
        cache = InMemoryCache()

    set_llm_cache(cache)
    return cache


def cache_description(cache_type: str) -> str:
    """Explain the two required cache options."""
    if cache_type == "SQLite cache":
        return (
            "SQLite cache: stored on disk, slightly slower than RAM, survives "
            "application restarts, and is useful for reusing results across sessions."
        )

    return (
        "In-memory cache: stored in RAM, very fast, does not survive application "
        "restart, and is useful for a single session."
    )
