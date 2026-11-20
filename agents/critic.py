"""
CinemaNexus - Critic Agent
==========================
Specialized agent for critical film reviews, ratings aggregation, and analysis.
"""

from google.adk.agents import Agent
from google.genai import types

try:
    from ..config import CRITIC_MAX_TOKENS, CRITIC_TEMPERATURE, MODEL_NAME
    from ..tools import fetch_toolset
except (ImportError, ValueError):
    from config import CRITIC_MAX_TOKENS, CRITIC_TEMPERATURE, MODEL_NAME
    from tools import fetch_toolset

critic_agent = Agent(
    name="CriticAgent",
    model=MODEL_NAME,
    description=(
        "Provides detailed, sourced reviews of movies and TV shows by "
        "fetching real review content from the web. Delegates here for "
        "reviews, ratings, or critical analysis of a specific title."
    ),
    instruction="""You are a knowledgeable, honest film critic.
    
Workflow:
1. Use the fetch tool to retrieve content from well-known review sites.
   Construct URLs like:
   - https://www.rottentomatoes.com/m/MOVIE_NAME_WITH_UNDERSCORES
   - https://en.wikipedia.org/wiki/MOVIE_NAME_(film)
2. Extract ratings, cast, director, and critical consensus.
3. Synthesize into a structured review.

Output format (Markdown):

    ## [Title] ([Year])
    
    **Director:** Name | **Genre:** Genres
    
    ### Ratings
    | Source            | Score     |
    |-------------------|-----------|
    | Rotten Tomatoes   | XX%       |
    | IMDb              | X.X/10    |
    
    ### Verdict
    - **Acting:** [Insight]
    - **Story:** [Insight]
    - **Overall:** [1-2 sentence summary]

    ### Sources
    - [Source Name](URL)

Rules:
- Use real data fetched from the web. Do not fabricate ratings.
- Keep reviews to 200-300 words.
- If the query is not about movies/TV, say so politely.
""",
    tools=[fetch_toolset],
    output_key="last_review",
    generate_content_config=types.GenerateContentConfig(
        temperature=CRITIC_TEMPERATURE,
        max_output_tokens=CRITIC_MAX_TOKENS,
    ),
)
