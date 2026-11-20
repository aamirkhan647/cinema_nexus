"""CinemaNexus - Agent Entry Point for Google ADK."""

try:
    from .agents import (
        critic_agent,
        director_agent,
        recommender_agent,
        root_agent,
        watchlist_agent,
    )
except (ImportError, ValueError):
    from agents import (
        critic_agent,
        director_agent,
        recommender_agent,
        root_agent,
        watchlist_agent,
    )

__all__ = [
    "root_agent",
    "director_agent",
    "critic_agent",
    "recommender_agent",
    "watchlist_agent",
]
