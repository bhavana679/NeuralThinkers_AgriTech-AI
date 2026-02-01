"""
Configuration Module - API Key Loading

This module handles loading of API keys from environment variables.
"""

import os


# Default timeout for API requests in seconds
DEFAULT_API_TIMEOUT = 10


def get_api_timeout() -> int:
    """
    Get API timeout from environment variable or use default.
    
    Returns:
        int: Timeout in seconds for API requests
    """
    timeout_str = os.environ.get("API_TIMEOUT")
    if timeout_str:
        try:
            timeout = int(timeout_str)
            if timeout > 0:
                return timeout
        except ValueError:
            pass
    return DEFAULT_API_TIMEOUT


def get_openweather_api_key() -> str:
    """Get OpenWeatherMap API key or None."""
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        print("Warning: OPENWEATHER_API_KEY not found. App will use Mock Data.")
        return None
    return api_key


def get_ambee_api_key() -> str:
    """Get Ambee API key or None."""
    api_key = os.environ.get("AMBEE_API_KEY")
    if not api_key:
        print("Warning: AMBEE_API_KEY not found. App will use Mock Data.")
        return None
    return api_key

