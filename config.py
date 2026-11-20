"""
CinemaNexus - Central Configuration
===================================
Application settings, model configurations, and runtime parameters.
"""

# Backward compatibility shim for pydantic >= 2.14 with mcp <= 1.12.2
try:
    import pydantic._internal._typing_extra as _pe

    if not hasattr(_pe, "eval_type_backport"):
        _pe.eval_type_backport = getattr(_pe, "eval_type", None)
except Exception:
    pass

PROJECT_NAME = "cinema_nexus"
MODEL_NAME = "gemini-3-flash-preview"

# Sub-agent generation profiles
CRITIC_TEMPERATURE = 0.3
CRITIC_MAX_TOKENS = 1024

RECOMMENDER_TEMPERATURE = 0.5
RECOMMENDER_MAX_TOKENS = 1024

WATCHLIST_TEMPERATURE = 0.1
WATCHLIST_MAX_TOKENS = 512

# Network / MCP parameters
MCP_FETCH_TIMEOUT = 30.0
