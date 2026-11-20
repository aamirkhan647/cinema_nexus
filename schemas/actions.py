"""
CinemaNexus - Action Schemas
============================
Enumerations defining valid operational actions across agents.
"""

from enum import Enum


class WatchlistAction(str, Enum):
    """Valid watchlist operations."""

    ADD = "add"
    REMOVE = "remove"
    LIST = "list"
