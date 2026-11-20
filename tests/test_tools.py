"""Non-mock unit tests for cinema_nexus tools using real ADK sessions and contexts."""

import pytest
from google.adk.agents import Agent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.sessions.session import Session
from google.adk.tools import ToolContext

from tools.watchlist_ops import WATCHLIST_STATE_KEY, manage_watchlist


def _build_real_tool_context(initial_watchlist: list[str] | None = None) -> ToolContext:
    """Constructs a real ToolContext backed by an actual InMemorySessionService and Session."""
    session_service = InMemorySessionService()
    state = {}
    if initial_watchlist is not None:
        state[WATCHLIST_STATE_KEY] = list(initial_watchlist)

    session = Session(
        id="test_session_001",
        app_name="cinema_nexus",
        user_id="test_reviewer",
        state=state,
    )
    agent = Agent(name="test_curator_agent")
    inv_context = InvocationContext(
        session_service=session_service,
        session=session,
        invocation_id="test_inv_001",
        agent=agent,
    )
    return ToolContext(inv_context)


class TestManageWatchlistOperations:
    def test_add_movie_success(self):
        ctx = _build_real_tool_context()
        result = manage_watchlist(action="add", title="Interstellar", tool_context=ctx)

        assert result["status"] == "added"
        assert result["title"] == "Interstellar"
        assert result["count"] == 1
        assert "Interstellar" in ctx.state[WATCHLIST_STATE_KEY]

    def test_add_duplicate_movie(self):
        ctx = _build_real_tool_context(initial_watchlist=["Interstellar"])
        result = manage_watchlist(action="add", title="Interstellar", tool_context=ctx)

        assert result["status"] == "already_exists"
        assert result["count"] == 1
        assert ctx.state[WATCHLIST_STATE_KEY] == ["Interstellar"]

    def test_list_empty_watchlist(self):
        ctx = _build_real_tool_context()
        result = manage_watchlist(action="list", tool_context=ctx)

        assert result["status"] == "listed"
        assert result["count"] == 0
        assert result["watchlist"] == []
        assert "empty" in result["message"].lower()

    def test_list_populated_watchlist(self):
        ctx = _build_real_tool_context(initial_watchlist=["Arrival", "Blade Runner 2049"])
        result = manage_watchlist(action="list", tool_context=ctx)

        assert result["status"] == "listed"
        assert result["count"] == 2
        assert result["watchlist"] == ["Arrival", "Blade Runner 2049"]

    def test_remove_existing_movie(self):
        ctx = _build_real_tool_context(initial_watchlist=["Arrival", "Oppenheimer"])
        result = manage_watchlist(action="remove", title="Arrival", tool_context=ctx)

        assert result["status"] == "removed"
        assert result["title"] == "Arrival"
        assert result["count"] == 1
        assert ctx.state[WATCHLIST_STATE_KEY] == ["Oppenheimer"]

    def test_remove_nonexistent_movie(self):
        ctx = _build_real_tool_context(initial_watchlist=["Oppenheimer"])
        result = manage_watchlist(action="remove", title="Dune", tool_context=ctx)

        assert result["status"] == "not_found"
        assert result["title"] == "Dune"
        assert result["count"] == 1
        assert ctx.state[WATCHLIST_STATE_KEY] == ["Oppenheimer"]

    def test_empty_title_on_add_or_remove(self):
        ctx = _build_real_tool_context()
        res_add = manage_watchlist(action="add", title="   ", tool_context=ctx)
        assert res_add["status"] == "error"
        assert "required" in res_add["message"].lower()

        res_rem = manage_watchlist(action="remove", title="", tool_context=ctx)
        assert res_rem["status"] == "error"
        assert "required" in res_rem["message"].lower()

    def test_unknown_action(self):
        ctx = _build_real_tool_context()
        result = manage_watchlist(action="destroy", title="Alien", tool_context=ctx)
        assert result["status"] == "error"
        assert "unknown action" in result["message"].lower()

    def test_manage_watchlist_without_context(self):
        # Tool execution when tool_context is None (standalone execution)
        result = manage_watchlist(action="list", tool_context=None)
        assert result["status"] == "listed"
        assert result["count"] == 0
