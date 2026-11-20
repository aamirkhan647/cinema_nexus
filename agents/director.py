"""
CinemaNexus - Director Orchestrator Agent
=========================================
Root orchestrator agent governing workflow delegation, system-wide guardrails,
and global interaction standards.
"""

from google.adk.agents import Agent

try:
    from ..config import MODEL_NAME
    from ..safety import input_guardrail, output_guardrail
except (ImportError, ValueError):
    from config import MODEL_NAME
    from safety import input_guardrail, output_guardrail

from .critic import critic_agent
from .recommender import recommender_agent
from .watchlist import watchlist_agent

director_agent = Agent(
    name="CinemaNexusDirector",
    model=MODEL_NAME,
    description="Orchestrator for the cinema_nexus multi-agent movie intelligence system.",
    global_instruction=(
        "You are part of cinema_nexus, a movie intelligence system. "
        "Always respond in well-formatted Markdown. Be concise and helpful. "
        "Never discuss topics unrelated to movies or TV shows."
    ),
    instruction="""You are the director of cinema_nexus, a multi-agent movie
intelligence system. You do not answer movie questions yourself – you delegate
to your team.

Your team:
- CriticAgent: Reviews, ratings, critical analysis of specific titles.
  Fetches real review content from the web via MCP.
- RecommenderAgent: Movie recommendations, "what to watch next", comparisons.
  Fetches real data from movie sites via MCP.
- WatchlistAgent: Managing the user's watchlist (add/remove/list).

Delegation rules:
- "review X", "is X good?", "how was X?" -> CriticAgent
- "recommend", "suggest", "what should I watch", "compare X vs Y" -> RecommenderAgent
- "add to watchlist", "my list", "save for later" -> WatchlistAgent

On the first message, briefly introduce yourself (one short paragraph) and
list what you can help with. If a query spans multiple agents, delegate to
each in sequence. If the query is unrelated to movies/TV, politely redirect.
""",
    sub_agents=[critic_agent, recommender_agent, watchlist_agent],
    before_model_callback=input_guardrail,
    after_model_callback=output_guardrail,
)

# Alias for backwards compatibility / root agent conventions
root_agent = director_agent
