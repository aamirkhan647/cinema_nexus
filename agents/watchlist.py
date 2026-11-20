"""
CinemaNexus - Watchlist Agent
=============================
Curator agent dedicated to personal user watchlist tracking and persistence.
"""

from google.adk.agents import Agent
from google.genai import types

try:
    from ..config import MODEL_NAME, WATCHLIST_MAX_TOKENS, WATCHLIST_TEMPERATURE
    from ..safety import watchlist_tool_guardrail
    from ..tools import manage_watchlist
except (ImportError, ValueError):
    from config import MODEL_NAME, WATCHLIST_MAX_TOKENS, WATCHLIST_TEMPERATURE
    from safety import watchlist_tool_guardrail
    from tools import manage_watchlist

watchlist_agent = Agent(
    name="WatchlistAgent",
    model=MODEL_NAME,
    description=(
        "Manages the user's movie watchlist. Delegates here when the user "
        "wants to add, remove, or view their watchlist."
    ),
    instruction="""You manage the user's personal movie watchlist.

Use the manage_watchlist tool with action='add', 'remove', or 'list'.
After any change, show the updated watchlist as a numbered Markdown list.
Keep responses short and helpful.
""",
    tools=[manage_watchlist],
    before_tool_callback=watchlist_tool_guardrail,
    generate_content_config=types.GenerateContentConfig(
        temperature=WATCHLIST_TEMPERATURE,
        max_output_tokens=WATCHLIST_MAX_TOKENS,
    ),
)
