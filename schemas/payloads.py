"""
CinemaNexus - Payload Schemas
=============================
Structured Pydantic data schemas for tool responses and security reports.
"""

from pydantic import BaseModel, Field


class WatchlistResult(BaseModel):
    """Structured result from a watchlist operation."""

    status: str = Field(description="Operation result: added, removed, listed, error")
    title: str | None = Field(default=None, description="Movie title acted upon")
    watchlist: list[str] = Field(
        default_factory=list, description="Current watchlist contents"
    )
    count: int = Field(default=0, description="Number of items in watchlist")
    message: str | None = Field(default=None, description="Human-readable detail")


class GuardrailResult(BaseModel):
    """Outcome of a security guardrail check."""

    passed: bool = Field(description="Whether the check passed")
    reason: str | None = Field(
        default=None, description="Why it was blocked, if applicable"
    )
    patterns_matched: list[str] = Field(
        default_factory=list, description="Patterns that triggered"
    )
