"""
CinemaNexus - Recommender Agent
===============================
Specialized discovery agent for personalized movie recommendations and comparisons.
"""

from google.adk.agents import Agent
from google.genai import types

try:
    from ..config import (
        MODEL_NAME,
        RECOMMENDER_MAX_TOKENS,
        RECOMMENDER_TEMPERATURE,
    )
    from ..tools import fetch_toolset
except (ImportError, ValueError):
    from config import (
        MODEL_NAME,
        RECOMMENDER_MAX_TOKENS,
        RECOMMENDER_TEMPERATURE,
    )
    from tools import fetch_toolset

recommender_agent = Agent(
    name="RecommenderAgent",
    model=MODEL_NAME,
    description=(
        "Recommends movies based on user preferences, compares titles, and "
        "suggests what to watch next. Delegates here for recommendations, "
        "'what should I watch', or comparisons between movies."
    ),
    instruction="""You help users discover movies and decide what to watch.

The user's current watchlist: {user_watchlist?}
Do not recommend movies already on their watchlist.

Workflow:
1. Use the fetch tool to look up movie info from trusted sites.
   Good URLs:
   - https://en.wikipedia.org/wiki/MOVIE_NAME_(film)
   - https://www.rottentomatoes.com/m/MOVIE_NAME
2. Personalize suggestions based on what the user says they like.

Output format (Markdown):

    ## If You Liked [Title], Try These

    | # | Movie | Why |
    |---|-------|-----|
    | 1 | [Title] | [Brief reason] |
    | 2 | [Title] | [Brief reason] |
    | 3 | [Title] | [Brief reason] |

    **Top pick:** [Title] - [Why]
    
Rules:
- Explain why each recommendation fits the user's taste.
- Use real data from fetched content. Do not make up scores.
- Keep responses concise.
""",
    tools=[fetch_toolset],
    generate_content_config=types.GenerateContentConfig(
        temperature=RECOMMENDER_TEMPERATURE,
        max_output_tokens=RECOMMENDER_MAX_TOKENS,
    ),
)
