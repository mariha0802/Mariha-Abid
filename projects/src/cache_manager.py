"""
Caching functionality for MediGuide AI.

This file provides:
1. InMemoryCache
2. SQLiteCache
"""

from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache
from langchain_community.cache import SQLiteCache


def use_memory_cache():
    """
    Enable in-memory caching.

    The cache is stored in RAM and is lost
    when the application is restarted.
    """

    cache = InMemoryCache()

    set_llm_cache(cache)

    return cache


def use_sqlite_cache():
    """
    Enable SQLite caching.

    The cache is stored in a SQLite database file
    and can remain available after restarting the application.
    """

    cache = SQLiteCache(database_path=".langchain.db")

    set_llm_cache(cache)

    return cache